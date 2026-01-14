#!/usr/bin/env python3
"""Public MCP validation showcase for Aleatoric.

This script demonstrates a minimal, publicly runnable validation flow:
1) Health check + preset discovery
2) Deterministic config validation (same config -> same hash)
3) Optional cache export to Parquet for downstream inspection

Run:
    export ALEATORIC_API_KEY="your-api-key"
    python validation_showcase.py --symbol BTC --seed 42 --duration 60

Optionally provide a cache key (from prior generation) to download a Parquet
artifact:
    python validation_showcase.py --cache-key my_cached_dataset_key
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path
from typing import Dict, Tuple

import httpx

DEFAULT_BASE_URL = "https://mcp.aleatoric.systems"
OUTPUT_PATH = Path(__file__).parent / "outputs" / "validation_demo.parquet"


def health_check(client: httpx.Client, base_url: str, headers: Dict[str, str]) -> None:
    resp = client.get(f"{base_url}/mcp/health", headers=headers)
    resp.raise_for_status()
    data = resp.json()
    print(f"Health: {data}")


def list_presets(client: httpx.Client, base_url: str, headers: Dict[str, str]) -> None:
    resp = client.get(f"{base_url}/mcp/presets", headers=headers)
    resp.raise_for_status()
    presets = resp.json().get("presets", [])
    print(f"Found {len(presets)} presets. Showing first 3:")
    for preset in presets[:3]:
        name = preset.get("name", "unknown")
        exchange = preset.get("exchange", "n/a")
        ptype = preset.get("type", "n/a")
        print(f"  - {name} (exchange={exchange}, type={ptype})")


def build_config(symbol: str, seed: int, duration: int) -> Dict[str, object]:
    # Minimal SimulationManifest subset for the public validate_config endpoint
    return {
        "symbol": symbol,
        "seed": seed,
        "duration_seconds": duration,
        "tick_size": 0.01,
        "lot_size": 0.001,
        "initial_mid": 50000.0,
        "initial_spread_bps": 1.0,
        "book_depth": 10,
        "volatility": 0.02,
        "drift": 0.0,
        "mean_reversion": 0.1,
    }


def validate_config(
    client: httpx.Client, base_url: str, headers: Dict[str, str], config: Dict[str, object]
) -> Dict[str, object]:
    resp = client.post(f"{base_url}/mcp/config/validate", json={"config": config}, headers=headers)
    resp.raise_for_status()
    return resp.json()


def download_cache(
    client: httpx.Client,
    base_url: str,
    headers: Dict[str, str],
    cache_key: str,
    output_path: Path,
) -> Tuple[Path, str]:
    resp = client.get(f"{base_url}/mcp/caches/export/{cache_key}", headers=headers)
    resp.raise_for_status()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(resp.content)
    sha = hashlib.sha256(resp.content).hexdigest()
    print(f"Saved Parquet to {output_path} (sha256={sha}, bytes={len(resp.content)})")
    return output_path, sha


def main() -> int:
    parser = argparse.ArgumentParser(description="Public MCP validation showcase")
    parser.add_argument("--symbol", default="BTC", help="Symbol (default: BTC)")
    parser.add_argument("--seed", type=int, default=42, help="Seed (default: 42)")
    parser.add_argument("--duration", type=int, default=60, help="Duration seconds (default: 60)")
    parser.add_argument("--cache-key", help="Cache key to export as Parquet")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="MCP base URL")
    parser.add_argument(
        "--skip-presets", action="store_true", help="Skip preset listing for speed"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_PATH,
        help=f"Where to store exported Parquet (default: {OUTPUT_PATH})",
    )
    args = parser.parse_args()

    api_key = os.getenv("ALEATORIC_API_KEY")
    if not api_key:
        print("Error: Set ALEATORIC_API_KEY environment variable", file=sys.stderr)
        return 1

    headers = {"X-API-Key": api_key}

    with httpx.Client(timeout=30) as client:
        health_check(client, args.base_url, headers)
        if not args.skip_presets:
            list_presets(client, args.base_url, headers)

        config = build_config(args.symbol, args.seed, args.duration)
        first = validate_config(client, args.base_url, headers, config)
        second = validate_config(client, args.base_url, headers, config)

        print(f"Validation #1: valid={first.get('valid')} hash={first.get('hash')}")
        print(f"Validation #2: valid={second.get('valid')} hash={second.get('hash')}")
        if first.get("hash") != second.get("hash"):
            print("Warning: Hash mismatch on identical configs (expected deterministic hash)")
        else:
            print("Deterministic hash confirmed for identical configs")

        cache_key = args.cache_key or first.get("cache_key") or first.get("hash")
        if cache_key:
            try:
                download_cache(client, args.base_url, headers, cache_key, args.output)
            except httpx.HTTPError as exc:
                print(f"Cache export failed for key={cache_key}: {exc}")
        else:
            print("No cache key provided or returned; skipping export.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
