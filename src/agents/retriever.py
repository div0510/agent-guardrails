from dataclasses import dataclass

from src.agents.base import Agent
from src.tools.mcp_client import MCPClient, MCPUnavailableError, run_with_retry


@dataclass
class RetrieverAgent(Agent):
    mcp_client: MCPClient | None = None

    def run(self, prompt: str) -> str:
        for hook in self.pre_hooks:
            hook.check(prompt)

        if self.mcp_client is None:
            return "[retriever] no mcp client configured"

        try:
            return f"[retriever] {run_with_retry(self.mcp_client, prompt)}"
        except MCPUnavailableError:
            return "[retriever] MCP unavailable, using fallback context"
