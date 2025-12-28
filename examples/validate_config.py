#!/usr/bin/env python3
"""
Validate a simulation configuration via the Aleatoric MCP API.

Demonstrates the `validate_config` tool which checks SimulationManifest
structure and returns a deterministic hash for reproducibility tracking.

Usage:
    export ALEATORIC_API_KEY="your-api-key"
    python validate_config.py
    python validate_config.py --show-schema
    python validate_config.py --config-file my_config.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import httpx

BASE_URL = "https://mcp.aleatoric.systems"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate simulation config")
    parser.add_argument("--config-file", help="Path to JSON config file")
    parser.add_argument("--show-schema", action="store_true", help="Print JSON Schema")
    parser.add_argument("--symbol", default="BTC", help="Symbol (default: BTC)")
    parser.add_argument("--seed", type=int, default=42, help="Seed (default: 42)")
    args = parser.parse_args()

    api_key = os.getenv("ALEATORIC_API_KEY")
    if not api_key:
        print("Error: Set ALEATORIC_API_KEY environment variable", file=sys.stderr)
        return 1

    headers = {"X-API-Key": api_key}

    with httpx.Client(timeout=30) as client:
        if args.show_schema:
            resp = client.get(f"{BASE_URL}/mcp/config/schema", headers=headers)
            resp.raise_for_status()
            print(json.dumps(resp.json(), indent=2))
            return 0

        if args.config_file:
            with open(args.config_file) as f:
                config = json.load(f)
        else:
            config = {
                "symbol": args.symbol,
                "seed": args.seed,
                "tick_size": 0.01,
                "lot_size": 0.001,
                "initial_mid": 50000.0,
                "initial_spread_bps": 1.0,
                "book_depth": 10,
                "volatility": 0.02,
                "drift": 0.0,
                "mean_reversion": 0.1,
            }

        print(f"Validating: symbol={config.get('symbol')}, seed={config.get('seed')}")

        resp = client.post(
            f"{BASE_URL}/mcp/config/validate",
            json={"config": config},
            headers=headers,
        )
        resp.raise_for_status()
        result = resp.json()

        if result.get("valid"):
            print(f"Valid! Hash: {result.get('hash')}")
            print(json.dumps(result.get("config", {}), indent=2))
        else:
            print(f"Invalid: {result.get('errors', [])}")
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
