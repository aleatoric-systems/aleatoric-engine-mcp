#!/usr/bin/env python3
"""
Generate a batch of synthetic market data via the Aleatoric MCP API.

This script demonstrates the correct workflow for creating large historical datasets:
1. Define a SimulationManifest (config)
2. Call POST /data/generate with duration_seconds
3. Download the resulting Parquet file from the returned URL

Usage:
    python generate_batch.py --symbol BTCUSDT --days 1 --output btc_1day.parquet
"""

import argparse
import asyncio
import os
import sys
import time
from pathlib import Path
from typing import Optional, List

import httpx

# Default configuration
MCP_BASE_URL = os.getenv("MCP_BASE_URL", "https://mcp.aleatoric.systems")
API_KEY = os.getenv("ALEATORIC_API_KEY")


async def generate_chunk(
    client: httpx.AsyncClient,
    symbol: str,
    duration: int,
    seed: int,
    chunk_index: int,
    base_url: str,
    api_key: str,
) -> bytes:
    """Generate and download a single chunk."""
    payload = {
        "config": {
            "symbol": symbol,
            "seed": seed,
        },
        "duration_seconds": duration,
    }
    headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
    
    print(f"  [Chunk {chunk_index}] Requesting generation ({duration}s)...")
    resp = await client.post(f"{base_url}/data/generate", headers=headers, json=payload, timeout=300.0)
    resp.raise_for_status()
    result = resp.json()
    
    download_url = result["download_url"]
    if download_url.startswith("/"):
        download_url = f"{base_url}{download_url}"
        
    print(f"  [Chunk {chunk_index}] Downloading...")
    dl_resp = await client.get(download_url, timeout=300.0)
    dl_resp.raise_for_status()
    
    print(f"  [Chunk {chunk_index}] Complete ({len(dl_resp.content)} bytes)")
    return dl_resp.content


async def generate_batch_parallel(
    symbol: str,
    total_duration: int,
    output_file: str,
    seed: int,
    concurrency: int = 5,
    base_url: str = MCP_BASE_URL,
    api_key: Optional[str] = API_KEY,
):
    if not api_key:
        print("Error: ALEATORIC_API_KEY environment variable not set.")
        sys.exit(1)

    chunk_size = 3600  # 1 hour per chunk
    num_chunks = (total_duration + chunk_size - 1) // chunk_size
    
    print(f"Generating {symbol} for {total_duration}s in {num_chunks} chunks (max {concurrency} parallel)...")
    
    async with httpx.AsyncClient() as client:
        tasks = []
        for i in range(num_chunks):
            chunk_duration = min(chunk_size, total_duration - (i * chunk_size))
            # Vary seed per chunk to ensure continuity (basic approach) or use same seed if engine handles offset
            # For independent chunks, new seeds are safer for now to avoid exact duplicate patterns if stateless
            # Ideally the engine accepts start_time or offset. 
            # We'll use seed + i for variance.
            chunk_seed = seed + i 
            
            tasks.append(
                generate_chunk(client, symbol, chunk_duration, chunk_seed, i, base_url, api_key)
            )
            
        # Run with semaphore
        semaphore = asyncio.Semaphore(concurrency)
        
        async def sem_task(task):
            async with semaphore:
                return await task
                
        results = await asyncio.gather(*(sem_task(t) for t in tasks))
        
    # Merge logic (simplified: sequential write or PyArrow)
    # For this script, we'll try to use Pandas to merge if available, else save individual files
    try:
        import pandas as pd
        from io import BytesIO
        
        print("Merging chunks...")
        dfs = [pd.read_parquet(BytesIO(content)) for content in results]
        full_df = pd.concat(dfs, ignore_index=True)
        full_df.to_parquet(output_file)
        print(f"Successfully saved merged file to {output_file} ({len(full_df)} rows)")
        
    except ImportError:
        print("Pandas not found. Saving individual chunks.")
        base_path = Path(output_file).parent
        stem = Path(output_file).stem
        for i, content in enumerate(results):
            out_path = base_path / f"{stem}_part_{i}.parquet"
            out_path.write_bytes(content)
            print(f"Saved {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic market data batch")
    parser.add_argument("--symbol", type=str, default="BTCUSDT", help="Trading symbol")
    parser.add_argument("--days", type=float, default=1.0, help="Duration in days")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output", type=str, default="synthetic_data.parquet", help="Output file path")
    parser.add_argument("--parallel", type=int, default=5, help="Parallel concurrency")
    
    args = parser.parse_args()
    duration = int(args.days * 24 * 3600)
    
    asyncio.run(generate_batch_parallel(
        symbol=args.symbol,
        total_duration=duration,
        output_file=args.output,
        seed=args.seed,
        concurrency=args.parallel
    ))

if __name__ == "__main__":
    main()
