from src.main import run_demo


def test_team_happy_path() -> None:
    result = run_demo("Summarize https://docs.agno.com/guardrails/overview")
    assert "## Final Answer" in result
    assert "[analyzer]" in result


def test_team_handles_mcp_outage_with_fallback() -> None:
    result = run_demo("simulate_mcp_failure while checking https://docs.agno.com/tools/mcp/overview")
    assert "## Final Answer" in result
    assert "fallback" in result.lower()
