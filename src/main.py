from src.agents.analyzer import AnalyzerAgent
from src.agents.responder import ResponderAgent
from src.agents.retriever import RetrieverAgent
from src.config.settings import MCPConfig
from src.guardrails.builtin.pii_detection import PIIDetectionGuardrail
from src.guardrails.builtin.prompt_injection import PromptInjectionGuardrail
from src.guardrails.custom.domain_allowlist_guardrail import DomainAllowlistGuardrail
from src.teams.main_team import MainTeam
from src.tools.mcp_client import MCPClient


def build_team() -> MainTeam:
    config = MCPConfig(mode="local", command="mock-mcp-server", retries=1, refresh_connection=True)
    mcp_client = MCPClient(config=config)
    mcp_client.connect()

    team_guardrails = [
        PromptInjectionGuardrail(),
        PIIDetectionGuardrail(),
        DomainAllowlistGuardrail({"docs.agno.com"}),
    ]

    retriever = RetrieverAgent(
        name="retriever",
        instructions="Retrieve MCP-backed facts only when needed.",
        pre_hooks=team_guardrails,
        mcp_client=mcp_client,
    )
    analyzer = AnalyzerAgent(
        name="analyzer",
        instructions="Convert retrieved data into concise findings.",
        pre_hooks=team_guardrails,
    )
    responder = ResponderAgent(
        name="responder",
        instructions="Generate final user-facing answer.",
        pre_hooks=team_guardrails,
    )
    return MainTeam(retriever=retriever, analyzer=analyzer, responder=responder, pre_hooks=team_guardrails)


def run_demo(prompt: str) -> str:
    team = build_team()
    return team.run(prompt)


if __name__ == "__main__":
    print(run_demo("Summarize https://docs.agno.com/tools/mcp/overview for setup"))
