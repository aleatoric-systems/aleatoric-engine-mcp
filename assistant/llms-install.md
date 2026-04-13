# Aleatoric MCP Installation Guide for AI Assistants

This guide provides step-by-step instructions for AI assistants (like Cline) to configure the Aleatoric MCP server.

## Prerequisites

- An Aleatoric API key (create your account at https://data.aleatoric.systems/get-started)
- No local installation required — this is a remote HTTP MCP server

## Installation Steps

### Step 1: Obtain API Key

1. Go to https://data.aleatoric.systems/get-started
2. Register for an account
3. Open the console and navigate to API Keys
4. Create a new API key with `mcp` scope
5. Copy the key (it will only be shown once)

The same account and API key also work on `sim.aleatoric.systems` and the hosted
MCP endpoint at `mcp.aleatoric.systems`.

### Step 2: Configure Cline

Add this to your Cline MCP configuration:

```json
{
  "mcpServers": {
    "aleatoric": {
      "url": "https://mcp.aleatoric.systems/mcp",
      "headers": {
        "X-API-Key": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

Replace `YOUR_API_KEY_HERE` with your actual API key.

### Step 3: Verify Installation

Test the connection by asking:

> "List available Aleatoric presets"

**Expected output:** A list of simulation presets including exchanges like Binance, HyperLiquid, etc.

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API key | Check API key is correct and has `mcp` scope |
| 403 Forbidden | API key lacks required scope | Regenerate key with `mcp` scope enabled |
| Connection refused | Network/firewall issue | Ensure https://mcp.aleatoric.systems is accessible |

## Available Tools

Once configured, you have access to:

- `validate_config` — Validate simulation configurations
- `get_presets` — List available market simulation profiles
- `normalize_events` — Normalize exchange data to canonical format
- `simulate_funding_regime` — Calculate funding rates across venues
- `get_venue_details` — Get exchange adapter info
- `get_config_schema` — Get JSON Schema for configs
- `get_cache_stats` — Cache statistics
- `stream_cache` — Stream cached events
- `export_cache` — Export as Parquet

## Example Usage

After installation, try:

```
"Generate synthetic BTC order book data with seed 42"
"Simulate 10 days of funding rates on HyperLiquid"
"What exchanges does Aleatoric support?"
```

## Support

- Documentation: https://data.aleatoric.systems/getting-started/quickstart
- Issues: https://github.com/aleatoric-systems/aleatoric-engine-mcp/issues
- Email: support@aleatoric.systems
