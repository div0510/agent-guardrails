# Agent Guardrails Demo

This repository contains a runnable multi-agent demo with:
- MCP-backed retriever flow
- Guardrails (prompt injection, PII, domain allowlist)
- FastAPI endpoints (POST + WebSocket stream)
- Pytest suite (unit, integration, security)

## 1) Prerequisites
- Python 3.10+
- `pip`

## 2) Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## 3) Install dependencies
```bash
pip install -r requirements.txt
```

## 4) Run the CLI demo
```bash
python -m src.main
```

Expected output includes:
- `[responder]`
- `## Final Answer`

## 5) Run the API server
```bash
uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload
```

## 6) Use the APIs

### 6.1 Swagger UI
- Open: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

### 6.2 POST full response
```bash
curl -X POST http://localhost:8000/v1/respond \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Summarize https://docs.agno.com/teams/overview","request_id":"demo-1"}'
```

### 6.3 WebSocket streaming URI
- `ws://localhost:8000/v1/respond/stream`

Example payload to send after connecting:
```json
{
  "prompt": "Summarize https://docs.agno.com/tools/mcp/overview",
  "request_id": "stream-1"
}
```

The stream emits envelope events with keys:
- `request_id`
- `status`
- `event`
- `data`
- `error`

## 7) Run tests
```bash
pytest -q
```

Notes:
- API tests auto-skip if FastAPI is not installed in your environment.
- The MCP client in this repo is a local demo/stub (`mock-mcp-server`), so you can run the flow without external MCP infra.
