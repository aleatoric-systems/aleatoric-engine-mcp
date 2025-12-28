#!/usr/bin/env python3
"""
Simulate funding rates across exchanges via Aleatoric MCP API.

Demonstrates the `simulate_funding_regime` tool for calculating
venue-specific funding rates, perp prices, and settlement logic.

Usage:
    export ALEATORIC_API_KEY="your-api-key"
    python funding_simulation.py
    python funding_simulation.py --exchange binance --periods 24
"""

from __future__ import annotations

import argparse
import os
import sys

import httpx

BASE_URL = "https://mcp.aleatoric.systems"
EXCHANGES = ["binance", "hyperliquid", "okx", "bybit", "cme", "sgx"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Simulate funding rates")
    parser.add_argument(
        "--exchange",
        choices=EXCHANGES,
        default="hyperliquid",
        help="Exchange (default: hyperliquid)",
    )
    parser.add_argument("--spot", type=float, default=50000.0, help="Spot price")
    parser.add_argument("--mark", type=float, default=50100.0, help="Mark price")
    parser.add_argument("--position", type=float, default=1.0, help="Position size")
    parser.add_argument("--periods", type=int, default=10, help="Funding periods")
    args = parser.parse_args()

    api_key = os.getenv("ALEATORIC_API_KEY")
    if not api_key:
        print("Error: Set ALEATORIC_API_KEY environment variable", file=sys.stderr)
        return 1

    headers = {"X-API-Key": api_key}

    payload = {
        "exchange": args.exchange,
        "spot_price": args.spot,
        "mark_price": args.mark,
        "position_size": args.position,
        "num_periods": args.periods,
    }

    with httpx.Client(timeout=30) as client:
        resp = client.post(
            f"{BASE_URL}/mcp/simulate_funding_regime",
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        result = resp.json()

    print(f"Exchange: {args.exchange.upper()}")
    print(f"Spot: ${args.spot:,.2f} | Mark: ${args.mark:,.2f}")
    print("-" * 60)

    for i, period in enumerate(result.get("periods", []), 1):
        rate = period.get("funding_rate", 0) * 100
        pnl = period.get("pnl", 0)
        print(f"Period {i:2d}: Rate={rate:+.4f}% | PnL=${pnl:+,.2f}")

    total_pnl = sum(p.get("pnl", 0) for p in result.get("periods", []))
    print("-" * 60)
    print(f"Total PnL: ${total_pnl:+,.2f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
