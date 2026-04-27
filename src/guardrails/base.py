from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class CheckTrigger:
    guardrail_name: str
    trigger_type: str
    detail: str


class InputCheckError(ValueError):
    def __init__(self, trigger: CheckTrigger):
        super().__init__(f"{trigger.guardrail_name}:{trigger.trigger_type}:{trigger.detail}")
        self.trigger = trigger


class BaseGuardrail(Protocol):
    name: str

    def check(self, run_input: str) -> None:
        ...

    async def async_check(self, run_input: str) -> None:
        ...
