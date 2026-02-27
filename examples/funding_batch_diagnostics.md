# Funding Batch Diagnostics Example

## Overview

The `funding_batch_diagnostics.py` example demonstrates the complete power of the Aleatoric MCP protocol by combining multiple capabilities into a comprehensive institutional-grade funding analysis workflow.

This example showcases:
- **Batch data generation** for multi-day simulations
- **Cross-exchange funding simulation** across multiple venues
- **Advanced analytics** with statistical summaries
- **Professional visualization** with diagnostic plots
- **Reproducible results** with deterministic seeding

## What It Does

### 1. Market Data Generation
Generates 5 days (configurable) of high-fidelity synthetic market data using the MCP `/data/generate` endpoint. The data includes:
- Order book updates
- Trade events
- Price movements
- Market microstructure

### 2. Funding Rate Simulation
Simulates funding rates across multiple exchanges (Binance, Hyperliquid, OKX, Bybit) using exchange-specific settlement logic:
- 8-hour funding cycles (3 per day)
- Venue-specific rate calculations
- Position PnL tracking
- Index vs. perpetual price dynamics

### 3. Diagnostic Visualizations
Creates a comprehensive multi-panel diagnostic plot showing:
- **Funding rates over time** for all exchanges
- **Cumulative PnL** comparison across venues
- **Funding rate distribution** with box plots
- **Average funding rate** comparison
- **Total PnL** by exchange

### 4. Analytics Reports
Generates detailed reports in both JSON and text formats containing:
- Per-exchange statistics (mean, std dev, min, max rates)
- Total PnL calculations
- Cross-exchange comparison
- Key insights and observations

## Usage

### Basic Usage
```bash
# Set your API key
export ALEATORIC_API_KEY="your-api-key-here"

# Run with defaults (5 days, BTCUSDT, 3 exchanges)
python examples/funding_batch_diagnostics.py
```

### Advanced Usage
```bash
# Analyze 7 days with larger position across all exchanges
python examples/funding_batch_diagnostics.py \
    --symbol ETHUSDT \
    --days 7 \
    --exchanges binance hyperliquid okx bybit \
    --position 10.0 \
    --output-dir ./my_analysis

# Quick 1-day test with custom seed
python examples/funding_batch_diagnostics.py \
    --days 1 \
    --seed 123 \
    --exchanges binance hyperliquid
```

## Output Files

The example generates multiple output files in the specified directory:

```
outputs/funding_analysis/
├── market_data_BTCUSDT_5d.parquet       # Raw market data (can be loaded in pandas)
├── funding_diagnostics_BTCUSDT.png      # Multi-panel visualization
├── analytics_BTCUSDT.json               # Machine-readable analytics
└── report_BTCUSDT.txt                   # Human-readable report
```

### Example Output Structure

**analytics_BTCUSDT.json:**
```json
{
  "metadata": {
    "symbol": "BTCUSDT",
    "days": 5,
    "position_size": 1.0,
    "total_periods": 15,
    "exchanges_analyzed": 3,
    "timestamp": "2026-01-30T12:00:00"
  },
  "exchanges": [
    {
      "exchange": "binance",
      "total_pnl": -12.45,
      "avg_funding_rate": 0.0001,
      "avg_funding_rate_bps": 1.0,
      "std_funding_rate": 0.00005,
      "min_funding_rate": -0.0002,
      "max_funding_rate": 0.0003
    }
  ],
  "cross_exchange": {
    "best_pnl_exchange": "hyperliquid",
    "best_pnl": 15.23,
    "worst_pnl_exchange": "binance",
    "worst_pnl": -12.45,
    "pnl_spread": 27.68
  }
}
```

**report_BTCUSDT.txt:**
```
================================================================================
FUNDING BATCH ANALYSIS REPORT - BTCUSDT
================================================================================
Generated: 2026-01-30 12:00:00
Duration: 5 days (15 funding periods)
Position Size: 1.0000
Exchanges: BINANCE, HYPERLIQUID, OKX

================================================================================
SUMMARY STATISTICS BY EXCHANGE
================================================================================

Exchange: BINANCE
----------------------------------------
  Total PnL:           $-12.45
  Average Rate:        +0.0100% (+1.00 bps)
  Std Dev Rate:        0.0050% (0.50 bps)
  Min Rate:            -0.0200% (-2.00 bps)
  Max Rate:            +0.0300% (+3.00 bps)
  Periods Analyzed:    15
...
```

## Requirements

### Python Packages
```bash
pip install -r examples/requirements.txt
```

Required packages:
- `httpx` - Async HTTP client for MCP API calls
- `matplotlib` - Plotting and visualization
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical operations

### API Access
- Valid `ALEATORIC_API_KEY` environment variable
- Access to `https://mcp.aleatoric.systems`

## Understanding the Results

### Funding Rate Interpretation
- Rates are expressed as percentages and basis points (bps)
- 1 bps = 0.01% = 0.0001 in decimal
- Positive rate: Longs pay shorts (typically when perp > spot)
- Negative rate: Shorts pay longs (typically when perp < spot)

### PnL Calculation
For a long position:
```
PnL per period = -position_size × funding_rate × mark_price
```

For a short position, the sign is reversed.

### Cross-Exchange Arbitrage
The "PnL Spread" in the report shows the difference between best and worst performing exchanges. This represents potential arbitrage opportunities from:
- Different funding rate mechanisms
- Varied settlement times
- Exchange-specific premium/discount dynamics

## Use Cases

### 1. Strategy Backtesting
Test how funding costs impact strategy performance across different venues over extended periods.

### 2. Exchange Comparison
Understand which exchanges have historically better funding conditions for your position type (long/short).

### 3. Risk Analysis
Analyze funding rate volatility and extreme scenarios (min/max rates) for risk management.

### 4. Product Demonstrations
Showcase the MCP protocol's capabilities for generating realistic, reproducible market data with venue-specific characteristics.

### 5. Research & Development
Use deterministic seeds to create reproducible datasets for:
- Algorithm development
- Model training
- Performance benchmarking

## Technical Details

### Funding Period Calculation
- Most exchanges: 3 funding periods per day (every 8 hours)
- Total periods = days × 3
- Example: 5 days = 15 funding periods

### Price Simulation
The example uses a simplified price model for demonstration:
```python
spot_prices = [base_price * (1 + 0.001 * i) for i in range(num_periods)]
mark_prices = [sp * (1 + 0.0001 * (i % 3 - 1)) for i, sp in enumerate(spot_prices)]
```

In production, you would:
1. Extract actual spot/mark prices from the generated market data
2. Use the MCP normalization tools to process real exchange data
3. Apply venue-specific index calculation logic

### Parallel Execution
The example uses Python's `asyncio` for concurrent API calls:
- Market data generation
- Multiple exchange simulations in parallel
- Efficient use of MCP API resources

## Extending the Example

### Custom Exchanges
Add support for additional venues by modifying the `EXCHANGES` list:
```python
EXCHANGES = ["binance", "hyperliquid", "okx", "bybit", "cme", "sgx"]
```

### Real Data Integration
Replace synthetic prices with real market data:
```python
# Load from Parquet
df = pd.read_parquet(market_data_path)
spot_prices = df['spot_price'].tolist()
mark_prices = df['mark_price'].tolist()
```

### Additional Metrics
Extend `ExchangeFundingResult` to include:
- Sharpe ratio of funding rates
- Correlation between exchanges
- Funding rate momentum indicators
- Premium/discount analysis

### Export Formats
Add CSV or database export:
```python
# CSV export
df.to_csv(output_dir / f"funding_data_{symbol}.csv")

# Database export (example)
import sqlite3
conn = sqlite3.connect(output_dir / "funding_analysis.db")
df.to_sql('funding_rates', conn, if_exists='replace')
```

## Performance Considerations

### Data Generation
- 5 days ≈ 432,000 seconds
- Typical generation time: 30-60 seconds
- File size: 5-50 MB (depends on activity level)

### API Rate Limits
The example respects MCP API limits:
- Concurrent requests are controlled via `asyncio`
- Reasonable timeout values (60-300 seconds)
- Exponential backoff on failures (not shown, but recommended)

### Memory Usage
- Parquet data is streamed (not loaded entirely)
- Results are accumulated incrementally
- Plot generation uses matplotlib's efficient rendering

## Troubleshooting

### "ALEATORIC_API_KEY not set"
```bash
export ALEATORIC_API_KEY="your-key-here"
```

### "pandas not available"
```bash
pip install pandas numpy
```

### "matplotlib not available"
The script will skip visualization but continue with data generation and JSON reports:
```bash
pip install matplotlib
```

### API Timeout
For very long durations (>7 days), consider:
- Increasing timeout values in the code
- Breaking into smaller chunks
- Using the batch generation script instead

## Related Examples

- `funding_simulation.py` - Simple single-exchange funding simulation
- `generate_batch.py` - Advanced parallel batch generation
- `validation_showcase.py` - Config validation and caching

## Support

For issues or questions:
- GitHub Issues: https://github.com/aleatoric/aleatoric-engine-mcp
- Documentation: https://docs.aleatoric.systems
- API Reference: https://mcp.aleatoric.systems/docs

## License

This example is part of the Aleatoric MCP SDK and follows the same license terms.
