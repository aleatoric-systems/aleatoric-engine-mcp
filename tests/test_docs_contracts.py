from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text()


def test_readme_points_api_key_signup_to_data_site():
    readme = _read("README.md")
    assert "https://data.aleatoric.systems/get-started" in readme
    assert "same registered account and issued API key work across" in readme
    assert '{"status": "ok"}' in readme


def test_install_guide_uses_shared_account_language():
    guide = _read("assistant/llms-install.md")
    assert "https://data.aleatoric.systems/get-started" in guide
    assert "The same account and API key also work on `sim.aleatoric.systems`" in guide
    assert "https://data.aleatoric.systems/getting-started/quickstart" in guide


def test_agent_guides_keep_public_discovery_and_authenticated_mcp_distinct():
    agent = _read("assistant/assistant_agent.md")
    llms = _read("llms.txt")
    assert "Public discovery is limited to endpoints like `/mcp/health` and `/mcp/manifest`" in agent
    assert "If asked where to create an account or API key" in llms
