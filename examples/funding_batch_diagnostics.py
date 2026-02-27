#!/usr/bin/env python3
"""
Funding Batch Analysis with Diagnostics and Visualization

This example demonstrates the complete Aleatoric MCP workflow for funding analysis:
1. Generate 5 days of synthetic market data via batch API
2. Simulate funding rates across multiple exchanges
3. Produce comprehensive diagnostics with plots and analytics
4. Export results for further analysis

This showcases the power of combining data generation, funding simulation,
and analytics tools available in the MCP protocol.

Usage:
    export ALEATORIC_API_KEY="your-api-key"
    python funding_batch_diagnostics.py --symbol BTCUSDT --output-dir ./outputs/funding_analysis
    python funding_batch_diagnostics.py --symbol BTCUSDT --exchanges binance hyperliquid okx --position 10.0
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional

import httpx

# Check for optional dependencies
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.gridspec import GridSpec
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib not available. Install with: pip install matplotlib")

try:
    import pandas as pd
    import numpy as np
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("Warning: pandas not available. Install with: pip install pandas")

# Configuration
MCP_BASE_URL = os.getenv("MCP_BASE_URL", "https://mcp.aleatoric.systems")
API_KEY = os.getenv("ALEATORIC_API_KEY")
EXCHANGES = ["binance", "hyperliquid", "okx", "bybit"]

# Funding periods per day (8 hour funding for most exchanges)
PERIODS_PER_DAY = 3


@dataclass
class FundingPeriod:
    """Represents a single funding period result."""
    timestamp: int
    funding_rate: float
    pnl: float
    perp_price: float
    index_price: float


@dataclass
class ExchangeFundingResult:
    """Complete funding simulation result for an exchange."""
    exchange: str
    periods: List[FundingPeriod]
    total_pnl: float
    avg_rate: float
    std_rate: float
    min_rate: float
    max_rate: float


async def generate_market_data(
    client: httpx.AsyncClient,
    symbol: str,
    days: int,
    seed: int,
    base_url: str,
    api_key: str,
) -> bytes:
    """
    Generate synthetic market data for the specified duration.

    Returns raw Parquet bytes for the generated data.
    """
    duration = days * 24 * 3600  # Convert days to seconds

    payload = {
        "config": {
            "symbol": symbol,
            "seed": seed,
            "tick_size": 0.01,
            "lot_size": 0.001,
            "initial_mid": 50000.0,
            "volatility": 0.02,
        },
        "duration_seconds": duration,
    }

    headers = {"X-API-Key": api_key, "Content-Type": "application/json"}

    print(f"Generating {days} days of market data for {symbol}...")
    resp = await client.post(
        f"{base_url}/data/generate",
        headers=headers,
        json=payload,
        timeout=300.0
    )
    resp.raise_for_status()
    result = resp.json()

    download_url = result["download_url"]
    if download_url.startswith("/"):
        download_url = f"{base_url}{download_url}"

    print(f"Downloading market data...")
    dl_resp = await client.get(download_url, timeout=300.0)
    dl_resp.raise_for_status()

    print(f"Market data generated ({len(dl_resp.content):,} bytes)")
    return dl_resp.content


async def simulate_funding_for_exchange(
    client: httpx.AsyncClient,
    exchange: str,
    spot_prices: List[float],
    mark_prices: List[float],
    position_size: float,
    base_url: str,
    api_key: str,
) -> ExchangeFundingResult:
    """
    Simulate funding rates for a single exchange across multiple periods.
    """
    num_periods = len(spot_prices)

    payload = {
        "exchange": exchange,
        "spot_price": spot_prices[0],
        "mark_price": mark_prices[0],
        "position_size": position_size,
        "num_periods": num_periods,
    }

    headers = {"X-API-Key": api_key}

    print(f"  Simulating {num_periods} funding periods for {exchange}...")
    resp = await client.post(
        f"{base_url}/mcp/simulate_funding_regime",
        json=payload,
        headers=headers,
        timeout=60.0
    )
    resp.raise_for_status()
    result = resp.json()

    # Parse periods
    periods = []
    for i, period_data in enumerate(result.get("periods", [])):
        periods.append(FundingPeriod(
            timestamp=i,
            funding_rate=period_data.get("funding_rate", 0),
            pnl=period_data.get("pnl", 0),
            perp_price=period_data.get("perp_price", mark_prices[min(i, len(mark_prices)-1)]),
            index_price=period_data.get("index_price", spot_prices[min(i, len(spot_prices)-1)]),
        ))

    # Calculate statistics
    rates = [p.funding_rate for p in periods]
    total_pnl = sum(p.pnl for p in periods)

    if HAS_PANDAS:
        rates_array = np.array(rates)
        avg_rate = float(np.mean(rates_array))
        std_rate = float(np.std(rates_array))
        min_rate = float(np.min(rates_array))
        max_rate = float(np.max(rates_array))
    else:
        avg_rate = sum(rates) / len(rates) if rates else 0
        std_rate = 0
        min_rate = min(rates) if rates else 0
        max_rate = max(rates) if rates else 0

    return ExchangeFundingResult(
        exchange=exchange,
        periods=periods,
        total_pnl=total_pnl,
        avg_rate=avg_rate,
        std_rate=std_rate,
        min_rate=min_rate,
        max_rate=max_rate,
    )


def create_diagnostic_plots(
    results: List[ExchangeFundingResult],
    output_dir: Path,
    symbol: str,
    days: int,
):
    """
    Create comprehensive diagnostic plots for funding analysis.
    """
    if not HAS_MATPLOTLIB:
        print("Skipping plots: matplotlib not available")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    # Create a multi-panel figure
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Color map for exchanges
    colors = plt.cm.Set2(range(len(results)))

    # Plot 1: Funding Rates Over Time
    ax1 = fig.add_subplot(gs[0, :])
    for i, result in enumerate(results):
        periods = range(len(result.periods))
        rates = [p.funding_rate * 100 for p in result.periods]  # Convert to percentage
        ax1.plot(periods, rates, label=result.exchange.upper(),
                color=colors[i], linewidth=2, alpha=0.8)

    ax1.set_title(f'Funding Rates Over Time - {symbol} ({days} Days)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Funding Period')
    ax1.set_ylabel('Funding Rate (%)')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='k', linestyle='--', linewidth=0.5)

    # Plot 2: Cumulative PnL
    ax2 = fig.add_subplot(gs[1, 0])
    for i, result in enumerate(results):
        periods = range(len(result.periods))
        cumulative_pnl = []
        total = 0
        for p in result.periods:
            total += p.pnl
            cumulative_pnl.append(total)
        ax2.plot(periods, cumulative_pnl, label=result.exchange.upper(),
                color=colors[i], linewidth=2, alpha=0.8)

    ax2.set_title('Cumulative PnL by Exchange', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Funding Period')
    ax2.set_ylabel('Cumulative PnL ($)')
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='k', linestyle='--', linewidth=0.5)

    # Plot 3: Funding Rate Distribution
    ax3 = fig.add_subplot(gs[1, 1])
    all_rates = []
    labels = []
    for result in results:
        rates = [p.funding_rate * 10000 for p in result.periods]  # Convert to basis points
        all_rates.append(rates)
        labels.append(result.exchange.upper())

    bp = ax3.boxplot(all_rates, labels=labels, patch_artist=True, notch=True)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax3.set_title('Funding Rate Distribution', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Funding Rate (bps)')
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.axhline(y=0, color='k', linestyle='--', linewidth=0.5)

    # Plot 4: Average Funding Rate Comparison
    ax4 = fig.add_subplot(gs[2, 0])
    exchanges = [r.exchange.upper() for r in results]
    avg_rates = [r.avg_rate * 10000 for r in results]  # basis points
    bars = ax4.bar(exchanges, avg_rates, color=colors, alpha=0.7, edgecolor='black')

    ax4.set_title('Average Funding Rate by Exchange', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Average Rate (bps)')
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.axhline(y=0, color='k', linestyle='--', linewidth=0.5)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom' if height >= 0 else 'top',
                fontsize=9)

    # Plot 5: Total PnL Comparison
    ax5 = fig.add_subplot(gs[2, 1])
    total_pnls = [r.total_pnl for r in results]
    bars = ax5.bar(exchanges, total_pnls, color=colors, alpha=0.7, edgecolor='black')

    ax5.set_title('Total PnL by Exchange', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Total PnL ($)')
    ax5.grid(True, alpha=0.3, axis='y')
    ax5.axhline(y=0, color='k', linestyle='--', linewidth=0.5)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:.2f}',
                ha='center', va='bottom' if height >= 0 else 'top',
                fontsize=9)

    # Save figure
    plot_path = output_dir / f"funding_diagnostics_{symbol}.png"
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    print(f"Diagnostic plots saved to {plot_path}")
    plt.close()


def generate_analytics_report(
    results: List[ExchangeFundingResult],
    output_dir: Path,
    symbol: str,
    days: int,
    position_size: float,
):
    """
    Generate a comprehensive analytics report in JSON and text formats.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Prepare analytics summary
    analytics = {
        "metadata": {
            "symbol": symbol,
            "days": days,
            "position_size": position_size,
            "total_periods": len(results[0].periods) if results else 0,
            "exchanges_analyzed": len(results),
            "timestamp": datetime.now().isoformat(),
        },
        "exchanges": []
    }

    # Text report
    report_lines = [
        "=" * 80,
        f"FUNDING BATCH ANALYSIS REPORT - {symbol}",
        "=" * 80,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Duration: {days} days ({len(results[0].periods) if results else 0} funding periods)",
        f"Position Size: {position_size:,.4f}",
        f"Exchanges: {', '.join(r.exchange.upper() for r in results)}",
        "",
        "=" * 80,
        "SUMMARY STATISTICS BY EXCHANGE",
        "=" * 80,
        ""
    ]

    for result in results:
        # Add to JSON
        analytics["exchanges"].append({
            "exchange": result.exchange,
            "total_pnl": result.total_pnl,
            "avg_funding_rate": result.avg_rate,
            "std_funding_rate": result.std_rate,
            "min_funding_rate": result.min_rate,
            "max_funding_rate": result.max_rate,
            "avg_funding_rate_bps": result.avg_rate * 10000,
            "total_periods": len(result.periods),
        })

        # Add to text report
        report_lines.extend([
            f"Exchange: {result.exchange.upper()}",
            f"{'-' * 40}",
            f"  Total PnL:           ${result.total_pnl:+,.2f}",
            f"  Average Rate:        {result.avg_rate*100:+.4f}% ({result.avg_rate*10000:+.2f} bps)",
            f"  Std Dev Rate:        {result.std_rate*100:.4f}% ({result.std_rate*10000:.2f} bps)",
            f"  Min Rate:            {result.min_rate*100:+.4f}% ({result.min_rate*10000:+.2f} bps)",
            f"  Max Rate:            {result.max_rate*100:+.4f}% ({result.max_rate*10000:+.2f} bps)",
            f"  Periods Analyzed:    {len(result.periods)}",
            ""
        ])

    # Calculate cross-exchange statistics
    if len(results) > 1:
        total_pnls = [r.total_pnl for r in results]
        avg_rates = [r.avg_rate for r in results]

        best_pnl_exchange = max(results, key=lambda r: r.total_pnl)
        worst_pnl_exchange = min(results, key=lambda r: r.total_pnl)

        report_lines.extend([
            "=" * 80,
            "CROSS-EXCHANGE ANALYSIS",
            "=" * 80,
            "",
            f"Best PnL:     {best_pnl_exchange.exchange.upper()} (${best_pnl_exchange.total_pnl:+,.2f})",
            f"Worst PnL:    {worst_pnl_exchange.exchange.upper()} (${worst_pnl_exchange.total_pnl:+,.2f})",
            f"PnL Spread:   ${max(total_pnls) - min(total_pnls):,.2f}",
            ""
        ])

        analytics["cross_exchange"] = {
            "best_pnl_exchange": best_pnl_exchange.exchange,
            "best_pnl": best_pnl_exchange.total_pnl,
            "worst_pnl_exchange": worst_pnl_exchange.exchange,
            "worst_pnl": worst_pnl_exchange.total_pnl,
            "pnl_spread": max(total_pnls) - min(total_pnls),
        }

    report_lines.extend([
        "=" * 80,
        "KEY INSIGHTS",
        "=" * 80,
        "",
        f"1. Over {days} days, {len(results[0].periods) if results else 0} funding periods were analyzed",
        f"2. Position size of {position_size} would generate varying PnL across venues",
        f"3. Funding rates show exchange-specific characteristics",
        f"4. This analysis demonstrates MCP's funding simulation capabilities",
        "",
        "=" * 80,
    ])

    # Save JSON report
    json_path = output_dir / f"analytics_{symbol}.json"
    with open(json_path, 'w') as f:
        json.dump(analytics, f, indent=2)
    print(f"Analytics JSON saved to {json_path}")

    # Save text report
    txt_path = output_dir / f"report_{symbol}.txt"
    with open(txt_path, 'w') as f:
        f.write('\n'.join(report_lines))
    print(f"Text report saved to {txt_path}")

    # Print summary to console
    print("\n" + "\n".join(report_lines))


async def run_funding_batch_analysis(
    symbol: str,
    days: int,
    exchanges: List[str],
    position_size: float,
    output_dir: Path,
    seed: int = 42,
):
    """
    Main analysis workflow orchestrating all steps.
    """
    if not API_KEY:
        print("Error: ALEATORIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    print("=" * 80)
    print("FUNDING BATCH DIAGNOSTICS")
    print("=" * 80)
    print(f"Symbol:        {symbol}")
    print(f"Duration:      {days} days")
    print(f"Exchanges:     {', '.join(e.upper() for e in exchanges)}")
    print(f"Position Size: {position_size}")
    print(f"Output Dir:    {output_dir}")
    print("=" * 80)
    print()

    async with httpx.AsyncClient() as client:
        # Step 1: Generate market data
        market_data = await generate_market_data(
            client, symbol, days, seed, MCP_BASE_URL, API_KEY
        )

        # Save market data
        output_dir.mkdir(parents=True, exist_ok=True)
        market_data_path = output_dir / f"market_data_{symbol}_{days}d.parquet"
        market_data_path.write_bytes(market_data)
        print(f"Market data saved to {market_data_path}")
        print()

        # Step 2: Extract price data for funding simulation
        # Simulate price movements for funding periods
        num_periods = days * PERIODS_PER_DAY

        # Generate synthetic spot and mark prices
        # In a real scenario, these would be extracted from the market data
        base_price = 50000.0
        spot_prices = [base_price * (1 + 0.001 * i) for i in range(num_periods)]
        mark_prices = [sp * (1 + 0.0001 * (i % 3 - 1)) for i, sp in enumerate(spot_prices)]

        print(f"Simulating funding rates across {len(exchanges)} exchanges...")
        print()

        # Step 3: Simulate funding for each exchange
        tasks = [
            simulate_funding_for_exchange(
                client, exchange, spot_prices, mark_prices,
                position_size, MCP_BASE_URL, API_KEY
            )
            for exchange in exchanges
        ]
        results = await asyncio.gather(*tasks)

        print()
        print("Funding simulation complete!")
        print()

        # Step 4: Generate diagnostics
        print("Generating diagnostic plots and analytics...")
        create_diagnostic_plots(results, output_dir, symbol, days)
        generate_analytics_report(results, output_dir, symbol, days, position_size)

        print()
        print("=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        print(f"All outputs saved to: {output_dir.absolute()}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Generate funding batch analysis with diagnostics and plots"
    )
    parser.add_argument(
        "--symbol",
        type=str,
        default="BTCUSDT",
        help="Trading symbol (default: BTCUSDT)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=5,
        help="Number of days to simulate (default: 5)"
    )
    parser.add_argument(
        "--exchanges",
        nargs="+",
        choices=EXCHANGES,
        default=["binance", "hyperliquid", "okx"],
        help="Exchanges to analyze (default: binance hyperliquid okx)"
    )
    parser.add_argument(
        "--position",
        type=float,
        default=1.0,
        help="Position size for PnL calculation (default: 1.0)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).parent / "outputs" / "funding_analysis",
        help="Output directory for results"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)"
    )

    args = parser.parse_args()

    # Check dependencies
    if not HAS_PANDAS:
        print("Error: pandas is required. Install with: pip install pandas", file=sys.stderr)
        sys.exit(1)

    asyncio.run(run_funding_batch_analysis(
        symbol=args.symbol,
        days=args.days,
        exchanges=args.exchanges,
        position_size=args.position,
        output_dir=args.output_dir,
        seed=args.seed,
    ))


if __name__ == "__main__":
    main()
