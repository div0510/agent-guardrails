import re

from src.guardrails.base import CheckTrigger, InputCheckError


class PIIDetectionGuardrail:
    name = "pii_detection"

    _SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
    _EMAIL_PATTERN = re.compile(r"\b[\w.%-]+@[\w.-]+\.[A-Za-z]{2,}\b")

    def check(self, run_input: str) -> None:
        if self._SSN_PATTERN.search(run_input):
            raise InputCheckError(CheckTrigger(self.name, "pii_ssn", "SSN pattern detected"))
        if self._EMAIL_PATTERN.search(run_input):
            raise InputCheckError(CheckTrigger(self.name, "pii_email", "Email pattern detected"))

    async def async_check(self, run_input: str) -> None:
        self.check(run_input)
