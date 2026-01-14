<p align="center">
  <img src="aleatoric.png" alt="Aleatoric Systems" width="200">
</p>

# Aleatoric MCP Client

[![MCP Version](https://img.shields.io/badge/MCP-1.0.0-blue)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/aleatoric-systems/aleatoric-engine-mcp)](https://github.com/aleatoric-systems/aleatoric-engine-mcp)
[![MCP Badge](https://lobehub.com/badge/mcp/aleatoric-systems-aleatoric-engine-mcp?style=for-the-badge)](https://lobehub.com/mcp/aleatoric-systems-aleatoric-engine-mcp)
[![smithery badge](https://smithery.ai/badge/aleatoric/causal-mcp)](https://smithery.ai/server/aleatoric/causal-mcp)
[![smithery badge](https://smithery.ai/badge/aleatoric/causal-mcp)](https://smithery.ai/server/aleatoric/causal-mcp)

> Official MCP client SDK for [Aleatoric Systems](https://www.aleatoric.systems) — Institutional-grade synthetic market data generation.

**Keywords:** `mcp` `market-data` `synthetic-data` `backtesting` `trading` `fintech` `quantitative-finance` `perpetuals` `futures` `order-book`

## Overview

Aleatoric MCP provides AI assistants with tools to generate deterministic synthetic market data for backtesting, stress testing, and model validation. Connect your AI coding assistant to generate reproducible datasets across 6 major exchanges.

**Supported Exchanges:** Binance, HyperLiquid, OKX, Bybit, CME, SGX

## ⚡ 90-Second Demo

**Run this in your AI assistant (Cursor, Claude, Windsurf):**

> "Generate a 1-hour dataset of BTC/USDT L2 order book updates on Binance. Use seed 123 for reproducibility. Plot the mid-price and spread over time."

**What happens:**
1.  **Agent calls** `validate_config` to lock parameters.
2.  **Server generates** 3,600s of data (approx 14,000 events) with realistic microstructure.
3.  **Agent receives** a signed URL or stream of the data.
4.  **Agent plots** the exact price path defined by `seed=123`.

*Result: A fully reproducible market scenario for your backtest in under 2 minutes.*

### Public Validation Showcase

Run a deterministic hash check and optional Parquet export against the hosted MCP without any local server:

```bash
cd public/aleatoric-engine-mcp
pip install -r examples/requirements.txt
export ALEATORIC_API_KEY="your-api-key"
python examples/validation_showcase.py --symbol BTC --seed 42 --duration 60
```

If you have a cache key, add `--cache-key <key>` to download a Parquet artifact.

## Use Cases

- **Backtesting** — Generate months of realistic order book data in seconds
- **Stress Testing** — Simulate extreme market conditions with reproducible seeds
- **Model Validation** — Test trading algorithms against deterministic synthetic data
- **CI/CD Pipelines** — Automated testing with consistent market scenarios
- **Research** — Explore funding rate dynamics across venues

## Why Deterministic Data?

Random data is useless for engineering. You need:

1.  **Reproducibility:** If a test fails, you must be able to replay the *exact* same market conditions to debug it.
2.  **Control:** Inject specific anomalies (flash crashes, liquidity voids) to test edge cases that might not happen for years in production.
3.  **Compliance:** Prove your algorithm handles known adverse scenarios before deploying capital.
4.  **Speed:** Generate 10 years of tick data in minutes, without expensive subscriptions or rate limits.

## Quick Start

### Installation Methods (Friendly)
- **Zero install** — MCP server is hosted; no local binary to build or run.
- **Drop-in configs** — ready JSONs in `configs/` for Claude Desktop, Cursor, VS Code Copilot, and Cline; replace `YOUR_API_KEY_HERE` with your key.
- **Public Discovery** — endpoints for `health` and `manifest` are publicly accessible to allow easy integration with registries like LobeHub.

```bash
# Public health check (No API Key required)
curl -s https://mcp.aleatoric.systems/mcp/health
```

### Examples
- See `examples/README.md` for the curated flow:
  - List presets: `python examples/list_presets.py --manifest`
  - Validate config (hash): `python examples/validate_config.py --symbol BTC --seed 42`
  - Funding simulation: `python examples/funding_simulation.py --exchange binance`
  - Validation showcase (hash + optional export): `python examples/validation_showcase.py --symbol BTC --seed 42 --duration 60`

### 1. Get an API Key

Sign up at [www.aleatoric.systems](https://www.aleatoric.systems) to obtain your API key.

### 2. Configure Your MCP Client

Add to your MCP client configuration:

<details>
<summary><b>Claude Desktop</b></summary>

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "aleatoric": {
      "url": "https://mcp.aleatoric.systems/mcp",
      "headers": {
        "X-API-Key": "your-api-key-here"
      }
    }
  }
}
```
</details>

<details>
<summary><b>Cursor</b></summary>

Edit `.cursor/mcp.json` in your project or `~/.cursor/mcp.json` globally:

```json
{
  "mcpServers": {
    "aleatoric": {
      "url": "https://mcp.aleatoric.systems/mcp",
      "headers": {
        "X-API-Key": "your-api-key-here"
      }
    }
  }
}
```
</details>

<details>
<summary><b>VS Code (Copilot)</b></summary>

Edit `.vscode/mcp.json`:

```json
{
  "servers": {
    "aleatoric": {
      "type": "http",
      "url": "https://mcp.aleatoric.systems/mcp",
      "headers": {
        "X-API-Key": "your-api-key-here"
      }
    }
  }
}
```
</details>

<details>
<summary><b>Cline</b></summary>

Add via Cline MCP settings:

```json
{
  "aleatoric": {
    "url": "https://mcp.aleatoric.systems/mcp",
    "headers": {
      "X-API-Key": "your-api-key-here"
    }
  }
}
```
</details>

<details>
<summary><b>LobeHub (One-Click)</b></summary>

1. Go to **Settings → Agent → Plugin Settings**.
2. Click **\"Add via JSON\"** and paste:

```json
{
  "name": "Aleatoric Engine",
  "identifier": "aleatoric-engine-mcp",
  "manifest": "https://mcp.aleatoric.systems/mcp/manifest",
  "type": "remote",
  "url": "https://mcp.aleatoric.systems/mcp",
  "headers": {
    "X-API-Key": "YOUR_API_KEY_HERE"
  }
}
```
</details>

### 3. Verify Installation

Test the connection (this endpoint is public for discovery):

```bash
curl -s https://mcp.aleatoric.systems/mcp/health
```

**Expected output:**
```json
{"status": "ok", "version": "0.4.4"}
```

### 4. Start Using

Ask your AI assistant:

> "Generate 1 hour of BTC synthetic order book data with seed 42"

## Available Tools

| Tool | Description |
|------|-------------|
| `validate_config` | Validate simulation configuration and get deterministic hash |
| `get_presets` | List available market simulation profiles |
| `normalize_events` | Normalize raw exchange data to canonical format |
| `simulate_funding_regime` | Calculate venue-specific funding rates and perp prices |
| `get_venue_details` | Get exchange adapter capabilities |
| `get_config_schema` | Get JSON Schema for SimulationManifest |
| `get_cache_stats` | Statistics about cached datasets |
| `stream_cache` | Stream cached events via SSE |
| `export_cache` | Export dataset as Parquet |
| `examples/validation_showcase.py` | Public demo: health/presets, deterministic hash check, optional cache export |

### Prompts & Resources
- **Prompts:** Example asks live in `README.md` (see Example Prompts) and can be reused directly in MCP-capable IDEs.
- **Resources:** The server exposes MCP `resources` for cache inspection/export; attach outputs via `get_cache_stats`, `stream_cache`, or `export_cache` to feed downstream tools.

## Validation Checklist (End-to-End)
- **Health:** `curl -s -H "X-API-Key: $ALEATORIC_API_KEY" https://mcp.aleatoric.systems/mcp/health` → expect `{ "status": "healthy", "version": "0.4.3" }`.
- **Manifest:** `python examples/list_presets.py --manifest` → prints server name/version and tool list.
- **Tool Call:** `python examples/validate_config.py --symbol BTC --seed 42` → expect `Valid! Hash: ...` with normalized config.
- **Resource Flow:** `python examples/funding_simulation.py --exchange hyperliquid` → exercises tool + resource outputs; for cache endpoints, call `get_cache_stats` then `stream_cache`/`export_cache` (attach resource in your MCP client). For a quick public validation demo, run `python examples/validation_showcase.py --symbol BTC --seed 42 --duration 60` to confirm deterministic hashes and optionally export a cached Parquet.
- **Offline sanity (no network):** `python -m compileall examples` after installing deps to ensure scripts parse.

## Example Prompts

```
"Validate this config: symbol BTC, seed 42, volatility 0.02"

"List available presets for perpetual futures"

"Simulate 10 days of funding rates on HyperLiquid with spot=50000 and mark=50100"

"What exchanges does Aleatoric support?"

"Export my cached dataset as Parquet"
```

## Direct API Usage

For programmatic access without an MCP client:

```python
import httpx
import os

api_key = os.getenv("ALEATORIC_API_KEY")
base_url = "https://mcp.aleatoric.systems"

with httpx.Client(timeout=30) as client:
    # Get available presets
    response = client.get(
        f"{base_url}/mcp/presets",
        headers={"X-API-Key": api_key}
    )
    presets = response.json()

    # Validate a configuration
    config = {
        "symbol": "BTC",
        "seed": 42,
        "tick_size": 0.01,
        "lot_size": 0.001,
        "initial_mid": 50000.0,
        "volatility": 0.02,
    }
    response = client.post(
        f"{base_url}/mcp/config/validate",
        json={"config": config},
        headers={"X-API-Key": api_key}
    )
    result = response.json()
    print(f"Valid: {result['valid']}, Hash: {result['hash']}")
```

See [examples/](examples/) for more complete examples.

## API Reference

Full API documentation: [www.aleatoric.systems](https://www.aleatoric.systems)

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mcp/manifest` | GET | Server capabilities |
| `/mcp/health` | GET | Health check |
| `/mcp/presets` | GET | List presets |
| `/mcp/config/validate` | POST | Validate config |
| `/mcp/config/schema` | GET | Get config schema |
| `/mcp/normalize` | POST | Normalize events |
| `/mcp/simulate_funding_regime` | POST | Funding simulation |
| `/mcp/venues/{exchange}` | GET | Venue details |
| `/mcp/caches/stats` | GET | Cache statistics |
| `/mcp/caches/stream/{key}` | GET | Stream cached data (SSE) |
| `/mcp/caches/export/{key}` | GET | Export as Parquet |

## Pricing

| Plan | Price | Includes |
|------|-------|----------|
| **Starter** | $249/mo | 14-day trial, basic presets |
| **Pro** | $1,250/mo | All exchanges, priority support |
| **Enterprise** | Custom | SLA, dedicated support, custom presets |

Start your free trial: [www.aleatoric.systems](https://www.aleatoric.systems)

## Support

- Documentation: [www.aleatoric.systems](https://www.aleatoric.systems)
- Issues: [GitHub Issues](https://github.com/aleatoric-systems/aleatoric-engine-mcp/issues)
- Email: support@aleatoric.systems

## License

MIT License - see [LICENSE](LICENSE)
