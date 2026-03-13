# Changelog

All notable changes to the `aleatoric-engine-mcp` package are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.5.6] - 2026-03-13

### Changed
- **Version alignment** — SDK package, mcp.json, and README version references updated from 0.5.2 to 0.5.6 to match engine release
- **README compliance badge** — Updated from v0.4.7 to v0.5.6; health check examples updated

### Added
- **Alpha proxy endpoints** — Engine now proxies `/api/v1/unified/consensus-pulse` for dashboard clients
- **Session auth for alpha tokens** — Engine recognizes `alpha_*` token prefix alongside `sess_*` for session validation
- **Service catalog** — Typed commercial service catalog with plan definitions and Stripe price resolution
- **Service entitlements** — Entitlement management with upsert, list, legacy derivation, and dashboard expansion
- **Control plane API** — `/v1/control-plane/catalog`, `/v1/control-plane/dashboard-state`, `/v1/control-plane/inventory/sources`, `/v1/control-plane/summary` endpoints
- **Billing audit trail** — Non-fatal Cosmos writes for billing lifecycle events
- **Usage threshold alerts** — `/v1/usage/current` returns alerts array with 70%/90%/100% threshold warnings

## [0.5.2] - 2026-03-01

### Added
- **Composite pair stream mode** (`mode=composite_pair` on `GET /stream/live`): Interleaved
  `{"type": "spot", "payload": {...}}` / `{"type": "perp", "payload": {...}}` SSE events.
  Spot payload conforms to TickSpotBook schema; perp to TickPerpMark schema. No
  client-side transformation required.
- **`src_latency_mode` query parameter** on `/stream/live`: Controls simulated source
  latency in the `src_latency_ms` event field. Values: `zero` (0ms, default),
  `colocated` (1–5ms uniform), `retail` (50–200ms uniform).
- **`source_type` field** on all stream event payloads: `"trade"` or `"depth"`.
  Composite spot: ~70% trade / 30% depth mix. Composite perp: always `"trade"`.
- **`src_latency_ms` field** on all composite event payloads: Float simulated latency.
- **`periods` array in `simulate_funding_regime` response**: `POST /mcp/simulate_funding_regime`
  now returns a `periods` array alongside existing scalar fields. Each element contains
  `period_index`, `start_ts_ms`, `next_funding_time`, `funding_rate`, `funding_rate_bps`,
  and `premium_bps`. Fully backward compatible.
- **`num_periods` param** on `simulate_funding_regime`: Number of forward settlement
  periods to generate (default 1, max ~12 for a 4-day window on 8h venues).
- **`seed` param** on `simulate_funding_regime`: Deterministic multi-period generation.
- **mcp.json updated** to v0.5.2: `simulate_funding_regime` tool description updated
  to document `num_periods`, `seed`, and the `periods[]` response. `generate_dataset`
  description updated to document `src_latency_ms` field and reference composite stream.

### Changed
- `server.version` in `mcp.json` bumped to `0.5.2`.
- `num_periods` default in `simulate_funding_regime` corrected to `1` (was `10` in
  prior spec; the engine now defaults to returning the current period only).

---

## [0.5.0] - 2026-02-27

### Added
- Initial public release of `aleatoric-engine-mcp` package.
- `mcp.json` server card with 13 tools: `get_health`, `get_presets`, `get_config_schema`,
  `validate_config`, `generate_dataset`, `normalize_events`, `simulate_funding_regime`,
  `get_venue_details`, `get_cache_stats`, `get_cache_manifest`, `delete_cache`,
  `stream_cache`, `export_cache`.
- All tools accessible via both REST endpoints and JSON-RPC `tools/call`.
- `mcpVersion: 2024-11-05`, protocol-compliant manifest.
