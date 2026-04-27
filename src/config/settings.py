from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class MCPConfig:
    """Configuration for connecting to one MCP endpoint."""

    mode: str = "local"
    url: Optional[str] = None
    command: Optional[str] = "mock-mcp-server"
    refresh_connection: bool = False
    timeout_seconds: float = 3.0
    retries: int = 1

    def validate(self) -> None:
        if self.mode not in {"local", "hosted"}:
            raise ValueError("mode must be either 'local' or 'hosted'")
        if self.mode == "hosted" and not self.url:
            raise ValueError("url is required when mode='hosted'")
        if self.mode == "local" and not self.command:
            raise ValueError("command is required when mode='local'")
