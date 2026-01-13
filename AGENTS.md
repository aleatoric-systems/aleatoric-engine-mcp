# Repository Guidelines

## Project Structure & Module Organization
- `examples/`: Python reference clients for Aleatoric MCP (config validation, funding simulation, preset discovery, Avellaneda/Stoikov demos). Notebooks write artifacts to `examples/outputs/`.
- `configs/`: Ready-to-drop MCP client configs for Claude Desktop, Cursor, VS Code Copilot, and Cline; copy rather than edit in-place.
- `README.md` and `llms-install.md`: Product overview plus IDE install notes; keep these aligned with code examples.

## Setup, Build, and Development Commands
- Use Python 3.10+; create a venv (`python -m venv .venv && source .venv/bin/activate`).
- Install deps for API scripts: `pip install -r examples/requirements.txt`; for quant sims/notebooks add `pip install numpy pandas matplotlib` as needed.
- Export credentials before hitting the API: `export ALEATORIC_API_KEY=...`.
- Smoke checks (hit live MCP): `python examples/validate_config.py --show-schema`, `python examples/list_presets.py --manifest`, `python examples/funding_simulation.py --exchange hyperliquid`.

## Coding Style & Naming Conventions
- Python: PEP 8, 4-space indent, snake_case for functions/vars, UPPER_SNAKE for constants, type hints for public surfaces.
- Favor dataclasses for configs and keep deterministic seeds surfaced as args/flags.
- HTTP calls: use `httpx.Client` with explicit timeouts and minimal retries; log useful context instead of broad prints.
- Examples should remain copy-pastable; keep CLI flags short and documented in the module docstring.

## Testing Guidelines
- No centralized test runner; treat the example scripts as smoke tests against the production MCP API.
- Run `python examples/validate_config.py` and `python examples/list_presets.py --venue binance` after changing request/response handling.
- For strategy sims (`examples/asq.py`, `examples/asq_test.py`), ensure stochastic components are seeded or documented; capture key metrics (PnL, drawdown) in console output.
- Avoid committing outputs or large artifacts from notebooks; keep `examples/outputs/` light.

## Commit & Pull Request Guidelines
- Follow observed history: short, imperative subject with optional scope (e.g., `docs: add install guide`).
- Describe behavioral impact and affected tools/endpoints; include the commands you ran and their outcomes when touching API flows.
- Link issues or tickets, note any external requirements (API key, env vars), and add before/after snippets for CLI output when relevant.
- Keep secrets out of commits; prefer `.env` or shell exports over checked-in config changes.

## Security & Configuration Tips
- Never commit real API keys; use placeholders in examples and sanitize notebooks.
- When adjusting `configs/*.json`, treat them as templates—document changes in README/llms-install rather than hard-coding credentials.
- Prefer reproducible seeds in simulations and call out any data retained in `examples/outputs/` for cleanup.
