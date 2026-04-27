from dataclasses import dataclass, field

from src.guardrails.base import BaseGuardrail


@dataclass
class Agent:
    name: str
    instructions: str
    pre_hooks: list[BaseGuardrail] = field(default_factory=list)

    def run(self, prompt: str) -> str:
        for hook in self.pre_hooks:
            hook.check(prompt)
        return f"[{self.name}] {prompt}"
