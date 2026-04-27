# Executable Steps (Implemented Sequentially)

## Step 1 — Bootstrap project structure ✅
- Created source/test folders for agents, teams, guardrails, tools, and config.
- Added package initialization files.

## Step 2 — Add MCP connectivity module ✅
- Implemented `MCPConfig` and `MCPClient`.
- Added retry + optional refresh behavior and fallback error type.

## Step 3 — Implement specialized agents ✅
- Added retriever agent (MCP-enabled).
- Added analyzer and responder agents.

## Step 4 — Build team orchestration ✅
- Added `MainTeam` coordinator flow: retriever → analyzer → responder.
- Added shared team/agent pre-hook guardrail checks.

## Step 5 — Add built-in and custom guardrails ✅
- Implemented prompt-injection and PII built-in guardrails.
- Implemented custom domain allowlist guardrail.

## Step 6 — Wire end-to-end demo ✅
- Added `src/main.py` with `build_team()` and `run_demo()`.
- Added MCP fallback behavior for outage simulation.

## Step 7 — Add regression and integration tests ✅
- Added unit tests for guardrails.
- Added integration tests for happy path and MCP fallback.
- Added security regression tests for prompt-injection/PII/domain abuse.

## Step 8 — Export service interfaces with FastAPI + Pydantic ✅
- Added POST API endpoint: `/v1/respond` returning full response in consistent envelope.
- Added WebSocket endpoint: `/v1/respond/stream` streaming chunk events and final payload using the same envelope structure.
- Added Pydantic request/response schemas for strict payload validation.

## Step 9 — API contract tests for consistency ✅
- Added integration tests validating identical JSON envelope keys for POST and WebSocket messages.

## Step 10 — Add Swagger/OpenAPI documentation ✅
- Added endpoint metadata (`summary`, `description`, tags) for HTTP APIs.
- Added `GET /v1/respond/stream-info` so WebSocket contract is visible from Swagger.
- Documented discovery points: `/docs` (Swagger UI) and `/openapi.json`.
