from __future__ import annotations

import time
from dataclasses import dataclass

from src.config.settings import MCPConfig


class MCPUnavailableError(RuntimeError):
    pass


@dataclass
class MCPClient:
    config: MCPConfig
    connected: bool = False

    def connect(self) -> None:
        self.config.validate()
        self.connected = True

    def close(self) -> None:
        self.connected = False

    def query(self, prompt: str) -> str:
        if not self.connected:
            raise MCPUnavailableError("MCP client is not connected")
        if "simulate_mcp_failure" in prompt:
            raise MCPUnavailableError("simulated MCP outage")
        return f"mcp_result:{prompt[:120]}"


def run_with_retry(client: MCPClient, prompt: str) -> str:
    last_error: Exception | None = None
    for _ in range(client.config.retries + 1):
        try:
            start = time.time()
            result = client.query(prompt)
            elapsed = time.time() - start
            if elapsed > client.config.timeout_seconds:
                raise MCPUnavailableError("MCP query timed out")
            return result
        except Exception as exc:  # query-time reliability boundary
            last_error = exc
            if client.config.refresh_connection:
                client.close()
                client.connect()
    raise MCPUnavailableError(f"MCP query failed after retries: {last_error}")
