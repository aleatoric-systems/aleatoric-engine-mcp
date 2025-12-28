#!/usr/bin/env python3
"""
List available presets and venue details via Aleatoric MCP API.

Demonstrates the `get_presets` and `get_venue_details` tools for
discovering simulation profiles and exchange adapter capabilities.

Usage:
    export ALEATORIC_API_KEY="your-api-key"
    python list_presets.py
    python list_presets.py --venue hyperliquid
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import httpx

BASE_URL = "https://mcp.aleatoric.systems"
EXCHANGES = ["binance", "hyperliquid", "okx", "bybit", "cme", "sgx"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Explore presets and venues")
    parser.add_argument("--presets", action="store_true", help="List presets only")
    parser.add_argument("--venue", choices=EXCHANGES, help="Get specific venue details")
    parser.add_argument("--manifest", action="store_true", help="Show MCP manifest")
    args = parser.parse_args()

    api_key = os.getenv("ALEATORIC_API_KEY")
    if not api_key:
        print("Error: Set ALEATORIC_API_KEY environment variable", file=sys.stderr)
        return 1

    headers = {"X-API-Key": api_key}

    with httpx.Client(timeout=30) as client:
        if args.manifest:
            resp = client.get(f"{BASE_URL}/mcp/manifest", headers=headers)
            resp.raise_for_status()
            manifest = resp.json()
            print(f"Server: {manifest['server']['name']} v{manifest['server']['version']}")
            print(f"\nTools ({len(manifest['capabilities']['tools'])}):")
            for name, info in manifest["capabilities"]["tools"].items():
                print(f"  - {name}: {info['description'][:50]}...")
            return 0

        if args.venue:
            resp = client.get(f"{BASE_URL}/mcp/venues/{args.venue}", headers=headers)
            resp.raise_for_status()
            print(json.dumps(resp.json(), indent=2))
            return 0

        # Default: show presets
        resp = client.get(f"{BASE_URL}/mcp/presets", headers=headers)
        resp.raise_for_status()
        presets = resp.json()

        print("Available Presets:")
        print("-" * 50)
        for preset in presets.get("presets", []):
            print(f"\n  {preset['name']}")
            print(f"    Exchange: {preset.get('exchange', 'N/A')}")
            print(f"    Type: {preset.get('type', 'N/A')}")
            print(f"    {preset.get('description', '')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
