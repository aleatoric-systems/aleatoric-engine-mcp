# Quick Start: Funding Batch Diagnostics

A 5-minute guide to running your first comprehensive funding analysis with Aleatoric MCP.

## Prerequisites

1. **Get an API Key**
   - Sign up at https://aleatoric.systems
   - Obtain your API key from the dashboard

2. **Install Dependencies**
   ```bash
   cd aleatoric-engine-mcp/examples
   pip install -r requirements.txt
   ```

## 3-Step Quick Start

### Step 1: Set Your API Key
```bash
export ALEATORIC_API_KEY="your-api-key-here"
```

### Step 2: Run the Analysis
```bash
python funding_batch_diagnostics.py
```

This will:
- Generate 5 days of synthetic market data for BTCUSDT
- Simulate funding rates across Binance, Hyperliquid, and OKX
- Create diagnostic plots and analytics

### Step 3: View Results
```bash
ls -lh outputs/funding_analysis/
```

You should see:
- `market_data_BTCUSDT_5d.parquet` - Raw market data
- `funding_diagnostics_BTCUSDT.png` - Visualization
- `analytics_BTCUSDT.json` - Detailed analytics
- `report_BTCUSDT.txt` - Human-readable report

View the report:
```bash
cat outputs/funding_analysis/report_BTCUSDT.txt
```

Open the plot:
```bash
# macOS
open outputs/funding_analysis/funding_diagnostics_BTCUSDT.png

# Linux
xdg-open outputs/funding_analysis/funding_diagnostics_BTCUSDT.png

# Windows
start outputs/funding_analysis/funding_diagnostics_BTCUSDT.png
```

## What You'll See

### Console Output
```
================================================================================
FUNDING BATCH DIAGNOSTICS
================================================================================
Symbol:        BTCUSDT
Duration:      5 days
Exchanges:     BINANCE, HYPERLIQUID, OKX
Position Size: 1.0
Output Dir:    outputs/funding_analysis
================================================================================

Generating 5 days of market data for BTCUSDT...
Downloading market data...
Market data generated (15,234,567 bytes)
Market data saved to outputs/funding_analysis/market_data_BTCUSDT_5d.parquet

Simulating funding rates across 3 exchanges...
  Simulating 15 funding periods for binance...
  Simulating 15 funding periods for hyperliquid...
  Simulating 15 funding periods for okx...

Funding simulation complete!

Generating diagnostic plots and analytics...
Diagnostic plots saved to outputs/funding_analysis/funding_diagnostics_BTCUSDT.png
Analytics JSON saved to outputs/funding_analysis/analytics_BTCUSDT.json
Text report saved to outputs/funding_analysis/report_BTCUSDT.txt

================================================================================
SUMMARY STATISTICS BY EXCHANGE
================================================================================

Exchange: BINANCE
----------------------------------------
  Total PnL:           $-12.45
  Average Rate:        +0.0100% (+1.00 bps)
  ...

================================================================================
ANALYSIS COMPLETE
================================================================================
All outputs saved to: /path/to/outputs/funding_analysis
```

### The Diagnostic Plot
The generated PNG contains 5 panels:

1. **Top Panel** - Funding rates over all 15 periods for each exchange
2. **Middle Left** - Cumulative PnL showing total profit/loss over time
3. **Middle Right** - Box plot distribution of funding rates
4. **Bottom Left** - Bar chart of average funding rates
5. **Bottom Right** - Bar chart of total PnL comparison

## Customization Examples

### Different Symbol
```bash
python funding_batch_diagnostics.py --symbol ETHUSDT
```

### Longer Duration
```bash
python funding_batch_diagnostics.py --days 7
```

### Larger Position
```bash
python funding_batch_diagnostics.py --position 10.0
```

### All Exchanges
```bash
python funding_batch_diagnostics.py --exchanges binance hyperliquid okx bybit
```

### Complete Custom Run
```bash
python funding_batch_diagnostics.py \
    --symbol ETHUSDT \
    --days 3 \
    --position 5.0 \
    --exchanges binance hyperliquid \
    --output-dir ./my_eth_analysis \
    --seed 123
```

## Understanding Your Results

### Key Metrics

**Funding Rate**
- Expressed in % and basis points (bps)
- Positive = longs pay shorts
- Negative = shorts pay longs
- Typical range: -0.05% to +0.05% (±5 bps)

**PnL (Profit & Loss)**
- For long positions: you pay positive funding, receive negative funding
- For short positions: opposite
- Cumulative PnL shows total funding costs over the period

**Cross-Exchange Spread**
- Difference between best and worst exchange
- Represents arbitrage opportunity
- Venues with different rate mechanisms show larger spreads

### Reading the JSON Analytics

```json
{
  "metadata": {
    "symbol": "BTCUSDT",
    "days": 5,
    "total_periods": 15  // 5 days × 3 periods/day
  },
  "exchanges": [
    {
      "exchange": "binance",
      "total_pnl": -12.45,           // Total funding cost
      "avg_funding_rate": 0.0001,    // 0.01% average
      "avg_funding_rate_bps": 1.0,   // 1 basis point
      "std_funding_rate": 0.00005,   // Volatility of rates
      "min_funding_rate": -0.0002,   // Most negative rate
      "max_funding_rate": 0.0003     // Most positive rate
    }
  ],
  "cross_exchange": {
    "best_pnl_exchange": "hyperliquid",  // Best venue for this position
    "pnl_spread": 27.68                  // Arbitrage potential
  }
}
```

## Next Steps

### 1. Analyze the Data
Load the Parquet file in Python:
```python
import pandas as pd
df = pd.read_parquet('outputs/funding_analysis/market_data_BTCUSDT_5d.parquet')
print(df.head())
print(df.describe())
```

### 2. Build on the Example
- Modify the price generation logic
- Add custom analytics metrics
- Integrate with your trading strategy
- Export to your database

### 3. Explore Other Examples
```bash
# Simple funding simulation
python funding_simulation.py --exchange binance

# Large batch generation
python generate_batch.py --symbol BTCUSDT --days 30

# Config validation
python validation_showcase.py --symbol BTC --seed 42
```

## Troubleshooting

### Error: "ALEATORIC_API_KEY not set"
**Solution:** Export your API key in the terminal:
```bash
export ALEATORIC_API_KEY="your-key-here"
```

To make it permanent, add to your `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export ALEATORIC_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Error: "No module named 'pandas'"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Error: "HTTP 401 Unauthorized"
**Solution:** Check your API key is valid and has not expired.

### Script Runs But No Plots Generated
**Solution:** This is normal if matplotlib is not installed. The script will still:
- Generate market data
- Simulate funding rates
- Create JSON and text reports

To get plots:
```bash
pip install matplotlib
```

### Slow Performance
**Solution:** For large analyses (>7 days):
- Use the `--days` parameter to test with fewer days first
- Consider using `generate_batch.py` for very large datasets
- Check your network connection speed

## Getting Help

- **Full Documentation:** See `funding_batch_diagnostics.md`
- **API Reference:** https://mcp.aleatoric.systems/docs
- **GitHub Issues:** Report bugs or request features
- **Community:** Join the Aleatoric Discord/Slack

## What This Example Demonstrates

This example showcases the complete MCP protocol workflow:

1. **Data Generation** - Institutional-grade synthetic market data
2. **Tool Integration** - Multiple MCP tools working together
3. **Reproducibility** - Deterministic seeding for consistent results
4. **Venue Modeling** - Exchange-specific funding mechanisms
5. **Professional Output** - Publication-ready plots and reports
6. **API Efficiency** - Async parallel processing

It's designed to help you:
- Understand MCP capabilities
- Build production workflows
- Evaluate exchange funding characteristics
- Develop and backtest funding-sensitive strategies

## Real-World Applications

### Quantitative Trading
- Backtest strategies that depend on funding costs
- Optimize position sizes based on funding exposure
- Select optimal venues for execution

### Risk Management
- Model funding rate volatility
- Stress test positions under extreme funding scenarios
- Calculate Value-at-Risk (VaR) including funding costs

### Market Making
- Understand funding revenue/costs
- Adjust quotes based on funding expectations
- Manage inventory across exchanges

### Research & Development
- Train ML models on synthetic funding data
- Test algorithms without market impact
- Develop venue-specific strategies

---

**Ready to get started?** Run the example now:
```bash
export ALEATORIC_API_KEY="your-key-here"
python funding_batch_diagnostics.py
```

Happy analyzing! 🚀
