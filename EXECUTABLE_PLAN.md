# Multi-Agent System with One MCP + Custom Guardrails

This plan turns the architecture into executable implementation tickets for Agno-based projects.

## Assumptions
- Framework: Agno (`Team`, `Agent`, `MCPTools`, guardrails pre-hooks).
- Initial scope: one MCP server integration, one custom guardrail, production-oriented hardening.
- Delivery shape: 3 sprints (can be compressed into 5- or 10-day tracks).

---

## Sprint 1 — Working Multi-Agent Flow with 1 MCP Server

### Ticket 1 — Bootstrap project skeleton
**Why**  
Create a predictable structure so new agents, tools, and guardrails can be added without refactors.

**Steps**
1. Create directories:
   - `src/agents/`
   - `src/teams/`
   - `src/tools/`
   - `src/guardrails/builtin/`
   - `src/guardrails/custom/`
   - `src/config/`
   - `tests/unit/`
   - `tests/integration/`
2. Add package init files where needed.
3. Add a minimal run entrypoint (`src/main.py`) with a no-op team run.

**Acceptance criteria**
- Repo installs and imports without path errors.
- `python -m src.main` runs and exits successfully.

**Estimate**: 0.5 day  
**Dependencies**: none

---

### Ticket 2 — Implement MCP client module
**Why**  
Centralize MCP session lifecycle and avoid duplicated connect/close logic across agents.

**Steps**
1. Create `src/tools/mcp_client.py` that builds `MCPTools` from config.
2. Support both connection modes:
   - Hosted: `MCPTools(url=...)`
   - Local: `MCPTools(command=...)`
3. Implement lifecycle helpers:
   - `connect_mcp()`
   - `close_mcp()`
   - optional context manager wrapper.
4. Add structured connection logs.

**Acceptance criteria**
- Standalone script can connect and close with no exceptions.
- Logs include session start and session close markers.

**Estimate**: 1 day  
**Dependencies**: Ticket 1

---

### Ticket 3 — Build specialized agents
**Why**  
Role separation improves quality and reduces misuse of tools.

**Steps**
1. Create `retriever_agent` with `tools=[mcp_tools]`.
2. Create `analyzer_agent` (no external tools).
3. Create `responder_agent` for final user-facing output.
4. Add explicit role instructions and output contracts per agent.

**Acceptance criteria**
- Each agent can be invoked independently with a test prompt.
- Retriever uses MCP tool path; non-retriever agents do not have MCP tools.

**Estimate**: 1 day  
**Dependencies**: Ticket 2

---

### Ticket 4 — Build team orchestrator
**Why**  
Coordinate delegation, enforce predictable routing, and standardize response format.

**Steps**
1. Create `src/teams/main_team.py` with a coordinator/leader.
2. Define delegation rules:
   - retrieval tasks → retriever
   - reasoning/validation tasks → analyzer
   - final response generation → responder
3. Require structured member outputs (e.g., headings or JSON fields).
4. Add top-level run flow that executes one full team request.

**Acceptance criteria**
- One end-to-end prompt triggers at least two members.
- Final output is synthesized (not raw tool output).

**Estimate**: 1 day  
**Dependencies**: Ticket 3

---

### Ticket 5 — Happy-path integration tests
**Why**  
Verify baseline functionality before introducing guardrails and resilience complexity.

**Steps**
1. Add integration test for:
   - user input → coordinator
   - coordinator → retriever (MCP)
   - analyzer + responder synthesis
2. Validate MCP lifecycle close in teardown.
3. Run test 3x to catch flaky behavior.

**Acceptance criteria**
- Integration test passes 3 consecutive runs.
- No leaked MCP sessions.

**Estimate**: 0.5–1 day  
**Dependencies**: Ticket 4

---

## Sprint 2 — Guardrails Baseline + First Custom Guardrail

### Ticket 6 — Enable built-in guardrails
**Why**  
Block common attack patterns early (prompt injection, PII leakage) before custom policy work.

**Steps**
1. Add built-in guardrails to pre-hooks where applicable:
   - prompt injection
   - PII detection
   - optional moderation
2. Attach at team level and critical agent level.
3. Add explicit blocked-response behavior.

**Acceptance criteria**
- Known malicious prompt-injection test inputs are blocked.
- Known PII examples are blocked or flagged.

**Estimate**: 0.5 day  
**Dependencies**: Sprint 1 complete

---

### Ticket 7 — Implement custom guardrail #1 (domain policy)
**Why**  
Enforce business-specific constraints not covered by generic built-ins.

**Steps**
1. Add `src/guardrails/custom/<policy_name>_guardrail.py`.
2. Inherit `BaseGuardrail`.
3. Implement:
   - `check(self, run_input)`
   - `async_check(self, run_input)`
4. On violation, raise `InputCheckError` with actionable `CheckTrigger`.
5. Keep rule small and single-purpose.

**Acceptance criteria**
- Unit tests cover allowed, blocked, and edge-case inputs.
- Trigger payload identifies guardrail and reason.

**Estimate**: 1 day  
**Dependencies**: Ticket 6

---

### Ticket 8 — Guardrail scope hardening (anti-bypass)
**Why**  
Ensure blocked requests cannot bypass policies via alternate agent path.

**Steps**
1. Attach custom guardrail at both:
   - Team pre-hooks
   - Retriever pre-hooks (and any high-risk agent)
2. Add bypass-attempt test cases.
3. Confirm all routes are evaluated pre-execution.

**Acceptance criteria**
- Bypass attempts fail regardless of delegation path.
- Guardrail trigger logs identify interception point.

**Estimate**: 0.5 day  
**Dependencies**: Ticket 7

---

## Sprint 3 — Reliability + Observability + Security Regression

### Ticket 9 — MCP resilience and graceful fallback
**Why**  
Prevent outages from causing user-visible crashes.

**Steps**
1. Add timeout and retry wrappers around MCP calls.
2. Optionally enable `refresh_connection=True` for unstable backends.
3. Define user-safe fallback response when MCP unavailable.
4. Add simulated outage tests.

**Acceptance criteria**
- Simulated MCP failure returns graceful degraded output.
- System does not crash on MCP timeout.

**Estimate**: 1 day  
**Dependencies**: Sprint 2 complete

---

### Ticket 10 — Guardrail telemetry and analytics hooks
**Why**  
Operational visibility is needed for tuning policies and incident response.

**Steps**
1. Add structured logging fields:
   - `guardrail_name`
   - `trigger_type`
   - `request_id`
   - `timestamp`
2. Redact sensitive fields before logging.
3. Emit metrics counters for block/allow by guardrail.

**Acceptance criteria**
- Logs can be queried for top triggered guardrails.
- No raw sensitive content is written to logs.

**Estimate**: 0.5–1 day  
**Dependencies**: Ticket 8

---

### Ticket 11 — Security regression test pack
**Why**  
Prevent policy drift and accidental weakening over time.

**Steps**
1. Create `tests/security/` datasets for:
   - prompt injection
   - PII exfiltration
   - prohibited-domain access
   - MCP abuse attempts
2. Add CI gate to fail on blocked-case regressions.
3. Add periodic review process for new adversarial cases.

**Acceptance criteria**
- CI fails if any blocked case becomes allowed.
- Test fixtures are versioned and documented.

**Estimate**: 1 day  
**Dependencies**: Ticket 10

---

## Suggested sequencing options

### 5-day compressed track
- Day 1: Tickets 1–2
- Day 2: Tickets 3–4
- Day 3: Ticket 5 + 6
- Day 4: Tickets 7–8
- Day 5: Tickets 9–11 (minimum viable depth)

### 10-day standard track
- Days 1–3: Sprint 1
- Days 4–6: Sprint 2
- Days 7–10: Sprint 3 + documentation

---

## Ready-to-copy ticket template (Jira/Linear)

**Title**:  
**Why**:  
**Scope**:  
**Implementation steps**:
1.
2.
3.

**Acceptance criteria**:
- [ ]
- [ ]

**Dependencies**:  
**Estimate**:  
**Owner**:  
**Risks/notes**:

---

## Definition of done (program-level)
- Team-based multi-agent flow is functional with one MCP server.
- Guardrails enforce both built-in and custom policy at non-bypassable scopes.
- MCP failures degrade gracefully.
- Regression tests protect against injection/PII/policy regressions.
- Telemetry supports operational monitoring and policy iteration.
