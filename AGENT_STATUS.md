# Agent Status & Open Tasks

## Current Context
- Repo path: `aleatoric-engine-mcp` (hosted MCP server; no local binary).
- Tooling: `.venv` created; `httpx` installed in `.venv`.
- Recent changes: Unlocked `/mcp/health` and `/mcp/manifest` for public access (no API key required), added `keywords` and `categories` to metadata.

## Completed
- Added `prompts` capability to `mcp.json` (generate_synthetic_data, simulate_funding).
- README now includes LobeHub quick import JSON and end-to-end validation checklist.
- Offline sanity: `python -m compileall examples` passes.
- MCP badge present.
- **Fixed:** Configured health/manifest as public to satisfy LobeHub crawler.
- **Fixed:** Added registry metadata (keywords/category) to `mcp.json` and `main.py`.
- **Premium Standard (LobeHub):** Verified `mcp.json` has `prompts`, `keywords`, and `categories`. Updated README to reflect public health/manifest endpoints (no auth required for discovery).
- **Fixed:** Added `package.json` to satisfy "Installation Validation" and "Metadata" requirements for registry crawlers.
- **Enhanced:** `aleatoric-engine-mcp/README.md` now features a 90-second demo, "Why Deterministic?" section, and polished Quick Start.
- **Community:** Added `CODE_OF_CONDUCT.md`, `SECURITY.md`, and Issue/PR templates to `.github/`.
- **Metadata:** Created `GITHUB_METADATA.md` with descriptions, topics, and Org profile README for manual application.

## Blocking / Open Items
- Valid API key unknown; two provided keys returned 401. Clarify expected header (`X-API-Key` vs Bearer) and test with a working key for *protected* endpoints (like `/mcp/stream`).
- Live tool validation pending for protected endpoints.

## Suggested Next Steps
- **Action:** Apply settings from `GITHUB_METADATA.md` to GitHub repositories.
- **Action:** Create `v0.1.0` release tag for `aleatoric-engine-mcp`.
- Redeploy the updated codebase to production to apply the public health/manifest fix.
- Test endpoints once deployed: `curl https://mcp.aleatoric.systems/mcp/health` (should return 200 without key).
- Rerun validation checklist.