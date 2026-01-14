# Examples Quickstart (Public MCP)

All examples assume:
- `ALEATORIC_API_KEY` is set (no keys in code).
- Base URL: `https://mcp.aleatoric.systems`.
- `pip install -r examples/requirements.txt` (adds `httpx`, `matplotlib`, etc.).

Recommended order:
1) List presets: `python examples/list_presets.py --manifest`
2) Validate a config (deterministic hash): `python examples/validate_config.py --symbol BTC --seed 42`
3) Batch Generation: `python examples/generate_batch.py --symbol BTC --days 1 --output btc.parquet`
4) Funding simulation: `python examples/funding_simulation.py --exchange binance --periods 24`
5) Validation showcase (hash check + optional Parquet export): `python examples/validation_showcase.py --symbol BTC --seed 42 --duration 60 --cache-key <optional>`

Notebooks:
- `examples/asq_model_analysis.ipynb` — fetch MCP data via `/data/generate`, then run ASQ model. Requires `ALEATORIC_API_KEY`.
- `examples/mcp_vs_historical_comparison.ipynb` — compares MCP synthetic data to historical Hyperliquid data; synthetic side pulled via `/data/generate`. Requires `ALEATORIC_API_KEY`.

Security reminders:
- Never paste real keys into notebooks or scripts; use environment variables.
- Do not commit outputs or large artifacts from notebooks.
