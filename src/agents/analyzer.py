from dataclasses import dataclass

from src.agents.base import Agent


@dataclass
class AnalyzerAgent(Agent):
    def run(self, prompt: str) -> str:
        for hook in self.pre_hooks:
            hook.check(prompt)
        return f"[analyzer] key_findings={prompt[:180]}"
