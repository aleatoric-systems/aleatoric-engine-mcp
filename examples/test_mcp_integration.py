#!/usr/bin/env python3
"""
MCP Integration Test - Build Test Dataset via API

This script validates the full MCP integration by actually calling the API
to generate a small test dataset and simulating funding rates.

Usage:
    export ALEATORIC_API_KEY="your-api-key"
    python test_mcp_integration.py
"""

import asyncio
import os
import sys
from pathlib import Path

import httpx


# Configuration
MCP_BASE_URL = os.getenv("MCP_BASE_URL", "https://mcp.aleatoric.systems")
API_KEY = os.getenv("ALEATORIC_API_KEY")
OUTPUT_DIR = Path(__file__).parent / "outputs" / "test_integration"


async def test_health_check(client: httpx.AsyncClient) -> bool:
    """Test 1: Health check endpoint."""
    print("Test 1: Health Check")
    print("-" * 60)

    try:
        headers = {"X-API-Key": API_KEY}
        resp = await client.get(f"{MCP_BASE_URL}/mcp/health", headers=headers, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()

        print(f"  ✓ Status: {data.get('status', 'unknown')}")
        print(f"  ✓ Timestamp: {data.get('timestamp', 'unknown')}")
        print(f"  ✓ Health check passed\n")
        return True

    except httpx.HTTPError as e:
        print(f"  ✗ Health check failed: {e}\n")
        return False


async def test_get_presets(client: httpx.AsyncClient) -> bool:
    """Test 2: Get available presets."""
    print("Test 2: List Presets")
    print("-" * 60)

    try:
        headers = {"X-API-Key": API_KEY}
        resp = await client.get(f"{MCP_BASE_URL}/mcp/presets", headers=headers, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()

        presets = data.get("presets", [])
        print(f"  ✓ Found {len(presets)} presets")

        if presets:
            print(f"  ✓ Sample presets:")
            for preset in presets[:3]:
                name = preset.get("name", "unknown")
                exchange = preset.get("exchange", "n/a")
                print(f"    - {name} ({exchange})")

        print()
        return True

    except httpx.HTTPError as e:
        print(f"  ✗ Presets fetch failed: {e}\n")
        return False


async def test_generate_data(client: httpx.AsyncClient) -> tuple[bool, bytes]:
    """Test 3: Generate a small dataset (1 minute)."""
    print("Test 3: Generate Market Data (60 seconds)")
    print("-" * 60)

    try:
        # Request 1 minute of data
        payload = {
            "config": {
                "symbol": "BTCUSDT",
                "seed": 42,
                "tick_size": 0.01,
                "lot_size": 0.001,
                "initial_mid": 50000.0,
            },
            "duration_seconds": 60,
        }

        headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

        print("  → Requesting data generation...")
        resp = await client.post(
            f"{MCP_BASE_URL}/data/generate",
            headers=headers,
            json=payload,
            timeout=60.0
        )
        resp.raise_for_status()
        result = resp.json()

        download_url = result["download_url"]
        if download_url.startswith("/"):
            download_url = f"{MCP_BASE_URL}{download_url}"

        print(f"  ✓ Generation complete")
        print(f"  → Downloading from: {download_url}")

        dl_resp = await client.get(download_url, timeout=60.0)
        dl_resp.raise_for_status()

        data_bytes = dl_resp.content
        print(f"  ✓ Downloaded {len(data_bytes):,} bytes")

        # Save the data
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_file = OUTPUT_DIR / "test_market_data.parquet"
        output_file.write_bytes(data_bytes)
        print(f"  ✓ Saved to: {output_file}")
        print()

        return True, data_bytes

    except httpx.HTTPError as e:
        print(f"  ✗ Data generation failed: {e}\n")
        return False, b""


async def test_simulate_funding(client: httpx.AsyncClient) -> bool:
    """Test 4: Simulate funding rates."""
    print("Test 4: Simulate Funding Rates (Binance)")
    print("-" * 60)

    try:
        # Simulate 3 funding periods
        payload = {
            "exchange": "binance",
            "spot_price": 50000.0,
            "mark_price": 50050.0,
            "position_size": 1.0,
            "num_periods": 3,
        }

        headers = {"X-API-Key": API_KEY}

        print("  → Requesting funding simulation...")
        resp = await client.post(
            f"{MCP_BASE_URL}/mcp/simulate_funding_regime",
            json=payload,
            headers=headers,
            timeout=30.0
        )
        resp.raise_for_status()
        result = resp.json()

        periods = result.get("periods", [])
        print(f"  ✓ Simulated {len(periods)} funding periods")

        for i, period in enumerate(periods, 1):
            rate = period.get("funding_rate", 0) * 10000  # Convert to bps
            pnl = period.get("pnl", 0)
            print(f"    Period {i}: Rate={rate:+.2f} bps, PnL=${pnl:+.2f}")

        total_pnl = sum(p.get("pnl", 0) for p in periods)
        print(f"  ✓ Total PnL: ${total_pnl:+.2f}")
        print()

        return True

    except httpx.HTTPError as e:
        print(f"  ✗ Funding simulation failed: {e}\n")
        return False


async def test_multi_exchange_funding(client: httpx.AsyncClient) -> bool:
    """Test 5: Simulate funding across multiple exchanges."""
    print("Test 5: Multi-Exchange Funding Simulation")
    print("-" * 60)

    exchanges = ["binance", "hyperliquid", "okx"]

    try:
        results = {}

        for exchange in exchanges:
            payload = {
                "exchange": exchange,
                "spot_price": 50000.0,
                "mark_price": 50050.0,
                "position_size": 1.0,
                "num_periods": 5,  # 5 funding periods
            }

            headers = {"X-API-Key": API_KEY}

            print(f"  → Simulating {exchange}...")
            resp = await client.post(
                f"{MCP_BASE_URL}/mcp/simulate_funding_regime",
                json=payload,
                headers=headers,
                timeout=30.0
            )
            resp.raise_for_status()
            result = resp.json()

            periods = result.get("periods", [])
            total_pnl = sum(p.get("pnl", 0) for p in periods)
            avg_rate = sum(p.get("funding_rate", 0) for p in periods) / len(periods) if periods else 0

            results[exchange] = {
                "periods": len(periods),
                "total_pnl": total_pnl,
                "avg_rate_bps": avg_rate * 10000
            }

            print(f"    ✓ {exchange.upper()}: {len(periods)} periods, "
                  f"Avg Rate={avg_rate*10000:+.2f} bps, PnL=${total_pnl:+.2f}")

        print(f"\n  ✓ Multi-exchange simulation complete")
        print(f"  ✓ Tested {len(exchanges)} exchanges")
        print()

        return True

    except httpx.HTTPError as e:
        print(f"  ✗ Multi-exchange simulation failed: {e}\n")
        return False


async def test_data_inspection(data_bytes: bytes) -> bool:
    """Test 6: Inspect the generated Parquet data."""
    print("Test 6: Inspect Generated Data")
    print("-" * 60)

    if not data_bytes:
        print("  ⊘ Skipping (no data available)")
        print()
        return True

    try:
        import pandas as pd
        from io import BytesIO

        print("  → Loading Parquet data...")
        df = pd.read_parquet(BytesIO(data_bytes))

        print(f"  ✓ Loaded {len(df):,} rows")
        print(f"  ✓ Columns: {', '.join(df.columns.tolist()[:5])}...")

        if 'event_type' in df.columns:
            event_counts = df['event_type'].value_counts()
            print(f"  ✓ Event types:")
            for event_type, count in event_counts.items():
                print(f"    - {event_type}: {count:,}")

        print()
        return True

    except ImportError:
        print("  ⊘ Pandas not available, skipping inspection")
        print()
        return True

    except Exception as e:
        print(f"  ✗ Data inspection failed: {e}\n")
        return False


def create_summary_report(results: dict):
    """Create a summary report of test results."""
    print("=" * 70)
    print("MCP INTEGRATION TEST SUMMARY")
    print("=" * 70)

    total_tests = len(results)
    passed_tests = sum(1 for passed in results.values() if passed)

    print(f"\nTests Passed: {passed_tests}/{total_tests}")
    print()

    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}  {test_name}")

    print()

    if passed_tests == total_tests:
        print("✅ ALL TESTS PASSED!")
        print()
        print("Your MCP integration is working correctly.")
        print("You can now run the full funding batch diagnostics example:")
        print("  python funding_batch_diagnostics.py")
    else:
        print("❌ SOME TESTS FAILED")
        print()
        print("Please check the error messages above and verify:")
        print("  • Your API key is valid")
        print("  • You have network connectivity")
        print("  • The MCP service is operational")

    print()
    print("=" * 70)


async def run_integration_tests():
    """Run all integration tests."""
    print()
    print("=" * 70)
    print("MCP INTEGRATION TEST SUITE")
    print("=" * 70)
    print()
    print("This script will test the MCP API by:")
    print("  1. Checking service health")
    print("  2. Listing available presets")
    print("  3. Generating a small test dataset (60 seconds)")
    print("  4. Simulating funding rates")
    print("  5. Testing multi-exchange funding")
    print("  6. Inspecting generated data")
    print()
    print(f"API Endpoint: {MCP_BASE_URL}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print()

    if not API_KEY:
        print("❌ ERROR: ALEATORIC_API_KEY environment variable not set")
        print()
        print("Please set your API key:")
        print("  export ALEATORIC_API_KEY='your-key-here'")
        print()
        return 1

    results = {}
    data_bytes = b""

    async with httpx.AsyncClient() as client:
        # Run tests sequentially
        results["Health Check"] = await test_health_check(client)
        results["List Presets"] = await test_get_presets(client)

        # Generate data (returns both status and data)
        data_success, data_bytes = await test_generate_data(client)
        results["Generate Data"] = data_success

        results["Simulate Funding"] = await test_simulate_funding(client)
        results["Multi-Exchange Funding"] = await test_multi_exchange_funding(client)

    # Data inspection (doesn't need API client)
    results["Data Inspection"] = await test_data_inspection(data_bytes)

    # Print summary
    create_summary_report(results)

    # Return exit code (0 if all passed, 1 if any failed)
    return 0 if all(results.values()) else 1


def main():
    """Main entry point."""
    try:
        return asyncio.run(run_integration_tests())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
