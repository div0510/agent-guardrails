from urllib.parse import urlparse

from src.guardrails.base import CheckTrigger, InputCheckError


class DomainAllowlistGuardrail:
    name = "domain_allowlist"

    def __init__(self, allowed_domains: set[str]):
        self.allowed_domains = allowed_domains

    def check(self, run_input: str) -> None:
        tokens = [token for token in run_input.split() if token.startswith("http")]
        for token in tokens:
            domain = urlparse(token).netloc
            if domain and domain not in self.allowed_domains:
                raise InputCheckError(
                    CheckTrigger(self.name, "domain_block", f"domain '{domain}' not allowed")
                )

    async def async_check(self, run_input: str) -> None:
        self.check(run_input)
