from dataclasses import dataclass, field

from src.agents.analyzer import AnalyzerAgent
from src.agents.responder import ResponderAgent
from src.agents.retriever import RetrieverAgent
from src.guardrails.base import BaseGuardrail


@dataclass
class MainTeam:
    retriever: RetrieverAgent
    analyzer: AnalyzerAgent
    responder: ResponderAgent
    pre_hooks: list[BaseGuardrail] = field(default_factory=list)

    def run_with_trace(self, user_prompt: str) -> dict[str, str]:
        for hook in self.pre_hooks:
            hook.check(user_prompt)

        retrieved = self.retriever.run(user_prompt)
        analyzed = self.analyzer.run(retrieved)
        final_answer = self.responder.run(analyzed)
        return {
            "retriever": retrieved,
            "analyzer": analyzed,
            "responder": final_answer,
            "final_response": final_answer,
        }

    def run(self, user_prompt: str) -> str:
        return self.run_with_trace(user_prompt)["final_response"]
