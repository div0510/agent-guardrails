from dataclasses import dataclass

from src.agents.base import Agent


@dataclass
class ResponderAgent(Agent):
    def run(self, prompt: str) -> str:
        for hook in self.pre_hooks:
            hook.check(prompt)
        return f"[responder]\n## Final Answer\n{prompt}"
