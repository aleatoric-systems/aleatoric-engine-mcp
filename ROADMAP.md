# Aleatoric Engine Roadmap

This roadmap outlines the planned evolution of The Aleatoric Engine and the Aleatoric MCP Client.

---

## 🟢 Phase 1: Foundation (Complete)
*Focus: Reproducibility, Core Venues, and Basic Normalization.*

- [x] Deterministic price & book generation (HyperSynthReactor)
- [x] Core venue models: Binance, HyperLiquid, OKX, Bybit
- [x] Initial MCP implementation (Tools: `validate_config`, `get_presets`)
- [x] Basic normalization layer
- [x] Local artifact caching (Parquet)

## 🟡 Phase 2: Operational Hardening (Complete — Q1 2026)
*Focus: Scalability, Async processing, and Compliance.*

- [x] **Asynchronous Batch Jobs**: Offload large generation jobs to background workers (Azure Service Bus integration).
- [x] **Production Autoscaling**: Support for event-driven scaling (KEDA) to handle burst demand.
- [x] **Client-Side Parallelization**: Efficiently split large requests into parallel chunks.
- [x] **Governance Alignment**: Adopt Apache 2.0 license and community standards.
- [x] **Data Integrity Assertions**: `aleatoric.validation` package with pre-built test suites against exchange specs (v0.4.5).
- [x] **TradFi Bridges**: CME and SGX futures with accurate session hours, carry cost, and settlement logic (v0.4.1).
- [x] **MCP JSON-RPC 2.0**: Full standard Model Context Protocol — 13 tools across `tools/list`, `tools/call`, `initialize`, `ping` (v0.4.7).
- [x] **OAuth 2.0**: Client Credentials Grant flow for machine-to-machine auth with scoped JWT tokens (v0.4.5).
- [ ] **Signed Provenance**: Cryptographic signatures for generated artifacts to ensure auditability.

## 🟠 Phase 3: Advanced Microstructure (Q2 2026)
*Focus: Deepening realism and empirical calibration.*

- [x] **Regime-Switching Funding OU**: Regime signal from spot EWMA → bear/neutral/bull parameter blending (kappa, mu, sigma) calibrated to BTC Binance empirical data (v0.4.8).
- [x] **Funding Jump Component**: Compound Poisson jumps in funding OU (λ≈0.1/8h, configurable) to capture liquidation cascade spikes (v0.4.8).
- [x] **Coupled Basis OU**: Perpetual basis tracks funding dynamically via `dB = κ_b(β·F−B)dt + σ_b·dW_b`; `basis_beta=4.0` calibrated to BTC/USDT-PERP (v0.4.8).
- [ ] **480-sample TWAP Funding Settlement**: Weighted settlement calculation matching Binance's exact recency-biased TWAP.
- [ ] **Causal Funding→Spot Feedback**: Arb pressure model — large funding deviations bias spot drift.
- [ ] **GARCH / Stochastic Volatility**: Replace constant vol with time-varying volatility process.
- [ ] **Cross-Asset Correlation**: Simulate correlated baskets of tokens with shared jump intensity.
- [ ] **Liquidity Voids & Flash Crashes**: Pre-set scenarios for stress-testing execution algorithms.
- [ ] **L3 Book Simulation**: Individual order tracking and MBO (Market-by-Order) granularity.

## 🔴 Phase 4: Ecosystem & Integration (H2 2026)
*Focus: Integration with ML pipelines and trading platforms.*

- [ ] **Direct SDKs**: Native wrappers for Rust, C++, and Go.
- [ ] **Backtrader/Lean Integration**: One-click data feed integration for popular backtesting engines.
- [ ] **Synthetic Latency Injector**: Model-based network jitter simulation for HFT testing.
- [ ] **OpenData Initiative**: Publicly available daily snapshots of synthetic high-volatility regimes.

---
*Note: This roadmap is a living document and is subject to change based on community feedback and institutional research requirements.*
