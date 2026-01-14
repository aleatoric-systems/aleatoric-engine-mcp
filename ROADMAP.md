# Aleatoric Engine Roadmap

This roadmap outlines the planned evolution of The Aleatoric Engine and the Aleatoric MCP Client.

---

## 🟢 Phase 1: Foundation (Current)
*Focus: Reproducibility, Core Venues, and Basic Normalization.*

- [x] Deterministic price & book generation (HyperSynthReactor)
- [x] Core venue models: Binance, HyperLiquid, OKX, Bybit
- [x] Initial MCP implementation (Tools: `validate_config`, `get_presets`)
- [x] Basic normalization layer
- [x] Local artifact caching (Parquet)

## 🟡 Phase 2: Operational Hardening (Q1 2026)
*Focus: Scalability, Async processing, and Compliance.*

- [x] **Asynchronous Batch Jobs**: Offload large generation jobs to background workers (Azure Service Bus integration).
- [x] **Production Autoscaling**: Support for event-driven scaling (KEDA) to handle burst demand.
- [x] **Client-Side Parallelization**: Efficiently split large requests into parallel chunks.
- [x] **Governance Alignment**: Adopt Apache 2.0 license and community standards.
- [ ] **Data Integrity Assertions**: Pre-built test suites to verify generated data against exchange specs.
- [ ] **Signed Provenance**: Cryptographic signatures for generated artifacts to ensure auditability.

## 🟠 Phase 3: Advanced Microstructure (Q2 2026)
*Focus: Deepening realism and adding new asset classes.*

- [ ] **Cross-Asset Correlation**: Simulate correlated baskets of tokens with shared jump intensity.
- [ ] **Liquidity Voids & Flash Crashes**: Pre-set scenarios for stress-testing execution algorithms.
- [ ] **TradFi Bridges**: Initial support for CME and SGX futures with accurate session hours and settlement logic.
- [ ] **L3 Book Simulation**: Individual order tracking and MBO (Market-by-Order) granularity.

## 🔴 Phase 4: Ecosystem & Integration (H2 2026)
*Focus: Integration with ML pipelines and trading platforms.*

- [ ] **Direct SDKs**: Native wrappers for Rust, C++, and Go.
- [ ] **Backtrader/Lean Integration**: One-click data feed integration for popular backtesting engines.
- [ ] **Synthetic Latency Injector**: Model-based network jitter simulation for HFT testing.
- [ ] **OpenData Initiative**: Publicly available daily snapshots of synthetic high-volatility regimes.

---
*Note: This roadmap is a living document and is subject to change based on community feedback and institutional research requirements.*
