from src.guardrails.base import CheckTrigger, InputCheckError


class PromptInjectionGuardrail:
    name = "prompt_injection"

    _BLOCK_PATTERNS = (
        "ignore previous instructions",
        "reveal system prompt",
        "bypass guardrails",
    )

    def check(self, run_input: str) -> None:
        lowered = run_input.lower()
        for pattern in self._BLOCK_PATTERNS:
            if pattern in lowered:
                raise InputCheckError(
                    CheckTrigger(self.name, "prompt_injection", f"matched '{pattern}'")
                )

    async def async_check(self, run_input: str) -> None:
        self.check(run_input)
