# Examples Quickstart (Public MCP)

All examples assume:
- `ALEATORIC_API_KEY` is set (no keys in code).
- Base URL: `https://mcp.aleatoric.systems`.
- `pip install -r examples/requirements.txt` (adds `httpx`, `matplotlib`, etc.).

Recommended order:
1) List presets: `python examples/list_presets.py --manifest`
2) Validate a config (deterministic hash): `python examples/validate_config.py --symbol BTC --seed 42`
3) Funding simulation: `python examples/funding_simulation.py --exchange binance --periods 24`
4) Validation showcase (hash check + optional Parquet export): `python examples/validation_showcase.py --symbol BTC --seed 42 --duration 60 --cache-key <optional>`

Notebooks:
- `examples/asq_model_analysis.ipynb` — fetch MCP data via `export_cache`, then run ASQ model. Requires `ALEATORIC_API_KEY` (and optionally `ALEATORIC_CACHE_KEY` if validation doesn’t return one).
- `examples/mcp_vs_historical_comparison.ipynb` — compares MCP synthetic data to historical Hyperliquid data; synthetic side pulled via MCP `export_cache`. Requires `ALEATORIC_API_KEY` (and optionally `ALEATORIC_CACHE_KEY`).

Security reminders:
- Never paste real keys into notebooks or scripts; use environment variables.
- Do not commit outputs or large artifacts from notebooks.
