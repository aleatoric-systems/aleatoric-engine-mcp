# Public MCP Validation Showcase

`examples/validation_showcase.py` provides a minimal, no-local-server demo of:

1. MCP health check
2. Preset discovery
3. Deterministic config validation (same config → same hash)
4. Optional cache export to Parquet for inspection

## Run it

```bash
cd public/aleatoric-engine-mcp
pip install -r examples/requirements.txt
export ALEATORIC_API_KEY="your-api-key"
python examples/validation_showcase.py --symbol BTC --seed 42 --duration 60
```

Optional: provide a cache key (from `validate_config` response or `get_cache_stats`) to download a Parquet artifact.

```bash
python examples/validation_showcase.py --cache-key my_cache_key --output /tmp/demo.parquet
```

Expected behavior:
- Health returns JSON with status/version
- Presets list prints first few entries
- validate_config called twice returns identical hashes (determinism check)
- If cache key is available, Parquet is downloaded and sha256 is printed

All calls use the public MCP endpoint `https://mcp.aleatoric.systems`.
