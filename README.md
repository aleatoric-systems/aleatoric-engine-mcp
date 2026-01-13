<p align="center">
  <img src="aleatoric.png" alt="Aleatoric Systems" width="200">
</p>

# Aleatoric MCP Client

[![MCP Version](https://img.shields.io/badge/MCP-1.0.0-blue)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/aleatoric-systems/aleatoric-engine-mcp)](https://github.com/aleatoric-systems/aleatoric-engine-mcp)
[![MCP Badge](https://lobehub.com/badge/mcp/aleatoric-systems-aleatoric-engine-mcp?style=for-the-badge)](https://lobehub.com/mcp/aleatoric-systems-aleatoric-engine-mcp)

> Official MCP client SDK for [Aleatoric Systems](https://www.aleatoric.systems) — Institutional-grade synthetic market data generation.

**Keywords:** `mcp` `market-data` `synthetic-data` `backtesting` `trading` `fintech` `quantitative-finance` `perpetuals` `futures` `order-book`

## Overview

Aleatoric MCP provides AI assistants with tools to generate deterministic synthetic market data for backtesting, stress testing, and model validation. Connect your AI coding assistant to generate reproducible datasets across 6 major exchanges.

**Supported Exchanges:** Binance, HyperLiquid, OKX, Bybit, CME, SGX

## Use Cases

- **Backtesting** — Generate months of realistic order book data in seconds
- **Stress Testing** — Simulate extreme market conditions with reproducible seeds
- **Model Validation** — Test trading algorithms against deterministic synthetic data
- **CI/CD Pipelines** — Automated testing with consistent market scenarios
- **Research** — Explore funding rate dynamics across venues

## Quick Start

### Installation Methods (Friendly)
- **Zero install** — MCP server is hosted; no local binary to build or run.
- **Drop-in configs** — ready JSONs in `configs/` for Claude Desktop, Cursor, VS Code Copilot, and Cline; replace `YOUR_API_KEY_HERE` with your key.
- **Health validation** — confirm connectivity anytime:

```bash
curl -s -H "X-API-Key: $ALEATORIC_API_KEY" https://mcp.aleatoric.systems/mcp/health
```

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

### 3. Verify Installation

Test the connection:

```bash
curl -s -H "X-API-Key: YOUR_KEY" https://mcp.aleatoric.systems/mcp/health
```

**Expected output:**
```json
{"status": "healthy", "version": "0.4.3"}
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

### Prompts & Resources
- **Prompts:** Example asks live in `README.md` (see Example Prompts) and can be reused directly in MCP-capable IDEs.
- **Resources:** The server exposes MCP `resources` for cache inspection/export; attach outputs via `get_cache_stats`, `stream_cache`, or `export_cache` to feed downstream tools.

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
