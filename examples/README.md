# Examples Quickstart (Public MCP)

All examples assume:
- `ALEATORIC_API_KEY` is set (no keys in code).
- Base URL: `https://mcp.aleatoric.systems`.
- `pip install -r examples/requirements.txt` (adds `httpx`, `matplotlib`, etc.).

Testing your setup:
- `python examples/test_funding_setup.py` — validates dependencies and environment
- `python examples/test_mcp_integration.py` — tests MCP API connectivity with real calls

Recommended order:
1) List presets: `python examples/list_presets.py --manifest`
2) Validate a config (deterministic hash): `python examples/validate_config.py --symbol BTC --seed 42`
3) Batch Generation: `python examples/generate_batch.py --symbol BTC --days 1 --output btc.parquet`
4) Funding simulation: `python examples/funding_simulation.py --exchange binance --periods 24`
5) Validation showcase (hash check + optional Parquet export): `python examples/validation_showcase.py --symbol BTC --seed 42 --duration 60 --cache-key <optional>`
6) **Funding Batch Diagnostics (NEW)**: `python examples/funding_batch_diagnostics.py --symbol BTCUSDT --days 5 --output-dir ./outputs/funding_analysis`
   - Generates 5 days of market data
   - Simulates funding across multiple exchanges (Binance, Hyperliquid, OKX)
   - Produces comprehensive diagnostic plots and analytics
   - Demonstrates complete MCP workflow for institutional-grade analysis

Notebooks:
- `examples/asq_model_analysis.ipynb` — fetch MCP data via `/data/generate`, then run ASQ model. Requires `ALEATORIC_API_KEY`.
- `examples/mcp_vs_historical_comparison.ipynb` — compares MCP synthetic data to historical Hyperliquid data; synthetic side pulled via `/data/generate`. Requires `ALEATORIC_API_KEY`.

Security reminders:
- Never paste real keys into notebooks or scripts; use environment variables.
- Do not commit outputs or large artifacts from notebooks.
