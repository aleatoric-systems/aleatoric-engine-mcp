# Funding Batch Diagnostics - Architecture Overview

This document explains how the `funding_batch_diagnostics.py` example integrates multiple MCP protocol components into a cohesive workflow.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     User Command Line Interface                      │
│  python funding_batch_diagnostics.py --symbol BTCUSDT --days 5      │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Main Orchestrator                               │
│                 run_funding_batch_analysis()                         │
│                                                                       │
│  • Validates API credentials                                         │
│  • Coordinates workflow steps                                        │
│  • Manages async execution                                           │
└────────────────┬────────────────────┬──────────────────┬────────────┘
                 │                    │                  │
                 ▼                    ▼                  ▼
┌────────────────────────┐ ┌──────────────────┐ ┌──────────────────────┐
│   STEP 1: Generate     │ │  STEP 2: Simulate│ │  STEP 3: Generate    │
│    Market Data         │ │  Funding Rates   │ │  Diagnostics         │
└────────────────────────┘ └──────────────────┘ └──────────────────────┘
         │                          │                      │
         │                          │                      │
         ▼                          ▼                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    MCP API Layer                                     │
│                https://mcp.aleatoric.systems                         │
└────────────────┬────────────────────┬──────────────────┬────────────┘
                 │                    │                  │
                 ▼                    ▼                  ▼
┌────────────────────────┐ ┌──────────────────────────────────────────┐
│  POST /data/generate   │ │  POST /mcp/simulate_funding_regime       │
│                        │ │                                          │
│  Input:                │ │  Input (per exchange):                   │
│  • symbol: BTCUSDT     │ │  • exchange: binance/hyperliquid/okx     │
│  • duration: 432000s   │ │  • spot_price: array                     │
│  • config: {...}       │ │  • mark_price: array                     │
│                        │ │  • position_size: 1.0                    │
│  Output:               │ │  • num_periods: 15                       │
│  • download_url        │ │                                          │
│  • cache_key           │ │  Output (per exchange):                  │
│                        │ │  • periods: array[funding_period]        │
│  Returns:              │ │  • Each period contains:                 │
│  • Parquet file        │ │    - funding_rate                        │
│  • Order book events   │ │    - pnl                                 │
│  • Trade events        │ │    - perp_price                          │
│  • Normalized data     │ │    - index_price                         │
└────────────────────────┘ └──────────────────────────────────────────┘
         │                          │
         │                          │
         ▼                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Data Processing Layer                            │
└────────────────┬────────────────────┬──────────────────┬────────────┘
                 │                    │                  │
                 ▼                    ▼                  ▼
┌────────────────────────┐ ┌──────────────────┐ ┌──────────────────────┐
│  Parquet Processing    │ │  Stats Calculation│ │  Visualization       │
│                        │ │                  │ │                      │
│  • Load with pandas    │ │  • Mean/Std Dev  │ │  • Matplotlib plots  │
│  • Extract prices      │ │  • Min/Max       │ │  • Multi-panel grid  │
│  • Time series         │ │  • Correlations  │ │  • Box plots         │
│  • Save to disk        │ │  • Cross-exchange│ │  • Time series       │
└────────────────────────┘ └──────────────────┘ └──────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Output Generation                             │
└────────────────┬────────────────────┬──────────────────┬────────────┘
                 │                    │                  │
                 ▼                    ▼                  ▼
┌────────────────────────┐ ┌──────────────────┐ ┌──────────────────────┐
│  Parquet File          │ │  JSON Analytics   │ │  Visualizations      │
│                        │ │                  │ │                      │
│  market_data.parquet   │ │  analytics.json  │ │  diagnostics.png     │
│  • Raw market data     │ │  • Statistics    │ │  • 5-panel plot      │
│  • Time-indexed        │ │  • Metadata      │ │  • Publication ready │
│  • Can be loaded       │ │  • Cross-exchange│ │                      │
│    for further work    │ │  • Machine-readable│ │                    │
└────────────────────────┘ └──────────────────┘ │  Text Report         │
                                                 │                      │
                                                 │  report.txt          │
                                                 │  • Human-readable    │
                                                 │  • Summary tables    │
                                                 │  • Insights          │
                                                 └──────────────────────┘
```

## Component Details

### 1. Market Data Generation

**Purpose:** Create realistic, reproducible synthetic market data

**MCP Tool:** `generate_dataset` (via `/data/generate` endpoint)

**Process Flow:**
1. Build SimulationManifest configuration
2. Submit to MCP API with duration
3. API generates orderbook/trade data
4. Returns download URL for Parquet file
5. Download and save locally

**Key Features:**
- Deterministic (same seed = same data)
- Configurable volatility, drift, spreads
- Institutional-grade microstructure
- Compressed Parquet format

### 2. Funding Rate Simulation

**Purpose:** Calculate venue-specific funding rates and PnL

**MCP Tool:** `simulate_funding_regime` (via `/mcp/simulate_funding_regime`)

**Process Flow:**
1. Extract or generate spot/mark prices
2. For each exchange in parallel:
   - Submit price data and position size
   - MCP calculates funding using exchange logic
   - Returns array of funding periods with rates and PnL
3. Aggregate results from all exchanges

**Key Features:**
- Exchange-specific settlement logic
- 8-hour funding cycles (configurable)
- Position-aware PnL calculation
- Parallel execution for speed

**Supported Exchanges:**
- Binance (3x daily, capped rates)
- Hyperliquid (continuous funding)
- OKX (3x daily)
- Bybit (3x daily)
- CME (quarterly futures-style)
- SGX (institutional)

### 3. Analytics Generation

**Purpose:** Calculate statistics and insights

**Libraries:** pandas, numpy

**Metrics Calculated:**
- **Per Exchange:**
  - Mean funding rate
  - Standard deviation (volatility)
  - Min/max extremes
  - Total PnL
  - Period count

- **Cross-Exchange:**
  - Best/worst performing venue
  - PnL spread (arbitrage potential)
  - Rate correlations (optional)

**Output Formats:**
- JSON (machine-readable)
- Text (human-readable)

### 4. Visualization

**Purpose:** Create diagnostic plots for analysis

**Library:** matplotlib

**Visualizations:**
1. **Time Series Plot** - Funding rates over all periods
2. **Cumulative PnL** - Running total for each exchange
3. **Distribution Plot** - Box plot of rate distributions
4. **Bar Charts** - Average rates and total PnL comparison

**Features:**
- Multi-panel layout (3x2 grid)
- Color-coded by exchange
- Publication-ready quality (150 DPI)
- Automatic legends and labels

## Data Flow

### Input Data
```
User Parameters
├── symbol: "BTCUSDT"
├── days: 5
├── exchanges: ["binance", "hyperliquid", "okx"]
├── position_size: 1.0
└── seed: 42
```

### Intermediate Data
```
Market Data (Parquet)
├── timestamp
├── symbol
├── event_type (orderbook_update, trade)
├── side (bid/ask)
├── price
├── quantity
└── ... (exchange-specific fields)

Funding Periods (per exchange)
├── period_index: 0..14
├── funding_rate: -0.0002..0.0003
├── pnl: -5.2..8.4
├── perp_price: 49950..50350
└── index_price: 49900..50300
```

### Output Data
```
outputs/funding_analysis/
├── market_data_BTCUSDT_5d.parquet      [Binary: Market microstructure]
├── analytics_BTCUSDT.json              [JSON: Statistics & metadata]
├── report_BTCUSDT.txt                  [Text: Human-readable summary]
└── funding_diagnostics_BTCUSDT.png     [Image: Multi-panel visualization]
```

## Execution Flow

### Sequential Steps
```
1. Validate API Key
   └─> Check ALEATORIC_API_KEY environment variable

2. Generate Market Data
   └─> POST /data/generate (30-60s for 5 days)
   └─> Download Parquet file
   └─> Save to disk

3. Extract Price Data
   └─> Generate or extract spot/mark prices
   └─> Create arrays for funding periods (15 periods for 5 days)

4. Simulate Funding (Parallel)
   ├─> POST /mcp/simulate_funding_regime [binance]
   ├─> POST /mcp/simulate_funding_regime [hyperliquid]
   └─> POST /mcp/simulate_funding_regime [okx]
   └─> Wait for all to complete (asyncio.gather)

5. Calculate Analytics
   └─> Aggregate results
   └─> Compute statistics (mean, std, min, max)
   └─> Identify best/worst performers

6. Generate Outputs
   ├─> Create diagnostic plots (matplotlib)
   ├─> Write JSON analytics
   └─> Write text report

7. Display Summary
   └─> Print key metrics to console
```

### Timing (Typical)
- Market data generation: 30-60 seconds
- Funding simulation (3 exchanges): 5-10 seconds
- Analytics & visualization: 2-5 seconds
- **Total: ~45-75 seconds for 5 days**

## Error Handling

```
┌─────────────────────────────────────┐
│  Error Source                       │
├─────────────────────────────────────┤
│  • Missing API key                  │──> Exit with error message
│  • Invalid API key                  │──> HTTP 401, display message
│  • Network timeout                  │──> Retry or display timeout
│  • Invalid parameters               │──> HTTP 400, show validation error
│  • Missing dependencies             │──> Import error, show install cmd
│  • Insufficient permissions         │──> File system error
└─────────────────────────────────────┘
```

The script includes defensive checks for:
- Environment variables
- Python package availability
- API response validation
- File system operations

## Extensibility Points

### 1. Custom Price Generation
Replace the synthetic price model:
```python
# Current (synthetic)
spot_prices = [base_price * (1 + 0.001 * i) for i in range(num_periods)]

# Custom (from real data)
df = pd.read_parquet(market_data_path)
spot_prices = df.resample('8H')['mid_price'].mean().tolist()
```

### 2. Additional Exchanges
Add new venues in the config:
```python
EXCHANGES = ["binance", "hyperliquid", "okx", "bybit", "deribit"]
```

### 3. Enhanced Analytics
Extend the metrics:
```python
@dataclass
class ExchangeFundingResult:
    # ... existing fields ...
    sharpe_ratio: float
    max_drawdown: float
    correlation_matrix: Dict[str, float]
```

### 4. Real-Time Integration
Connect to live price feeds:
```python
async def fetch_live_prices(exchange: str):
    # WebSocket or REST API integration
    return spot_price, mark_price
```

### 5. Database Export
Save to SQL/NoSQL:
```python
def export_to_database(results, connection_string):
    engine = create_engine(connection_string)
    df.to_sql('funding_rates', engine, if_exists='append')
```

## MCP Protocol Integration

This example demonstrates key MCP protocol concepts:

### 1. Tool Composition
Combining multiple MCP tools in sequence:
- `generate_dataset` → `simulate_funding_regime`

### 2. Reproducibility
Using deterministic seeds:
- Same seed → identical market data
- Enables backtesting and auditing

### 3. Venue Modeling
Exchange-specific adapters:
- Each exchange has unique funding logic
- MCP provides accurate implementations

### 4. Async Operations
Efficient API usage:
- Parallel funding simulations
- Non-blocking HTTP requests
- Resource optimization

### 5. Data Export
Standard formats:
- Parquet for data
- JSON for metadata
- PNG for visualization

## Performance Characteristics

### Scalability
```
Duration     | Periods | API Time | File Size | Total Time
-------------|---------|----------|-----------|------------
1 day        | 3       | ~10s     | ~3 MB     | ~15s
5 days       | 15      | ~45s     | ~15 MB    | ~60s
7 days       | 21      | ~60s     | ~20 MB    | ~75s
30 days      | 90      | ~180s    | ~80 MB    | ~200s
```

### Optimization Strategies
1. **Parallel Requests** - Use asyncio for concurrent API calls
2. **Caching** - MCP caches generated data (check cache_key)
3. **Compression** - Parquet files are highly compressed
4. **Streaming** - Process data incrementally for very large datasets

## Security Considerations

### API Key Management
```bash
# ✓ Correct: Environment variable
export ALEATORIC_API_KEY="key"

# ✗ Wrong: Hardcoded in script
api_key = "my-secret-key"  # Never do this!

# ✓ Better: .env file (excluded from git)
# .env
ALEATORIC_API_KEY=your-key-here
```

### Data Privacy
- Generated data is synthetic (not real user data)
- API requests are over HTTPS
- Output files may contain market data (handle appropriately)

### Rate Limiting
The MCP API has rate limits:
- Respect limits with proper async timing
- Use exponential backoff on errors
- Monitor your usage via dashboard

## Troubleshooting Guide

### Debug Mode
Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Network Issues
Test connectivity:
```bash
curl -H "X-API-Key: $ALEATORIC_API_KEY" \
  https://mcp.aleatoric.systems/mcp/health
```

### Performance Issues
Profile the script:
```bash
python -m cProfile -o profile.stats funding_batch_diagnostics.py
python -m pstats profile.stats
```

## Conclusion

This architecture demonstrates:
- ✓ Production-ready workflow design
- ✓ MCP protocol best practices
- ✓ Institutional-grade data handling
- ✓ Extensible component structure
- ✓ Comprehensive error handling
- ✓ Professional output generation

The example serves as a template for building sophisticated financial analysis tools using the Aleatoric MCP protocol.
