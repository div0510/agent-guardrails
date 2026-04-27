from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src.api.models import ResponseEnvelope, ResponseRequest, StreamInfoResponse, ensure_request_id
from src.guardrails.base import InputCheckError
from src.main import build_team

app = FastAPI(
    title="Agent Guardrails API",
    version="1.1.0",
    description=(
        "HTTP + WebSocket interface for the multi-agent MCP system. "
        "Swagger UI is available at `/docs` and OpenAPI JSON at `/openapi.json`."
    ),
    contact={"name": "Platform Team"},
)


def _generate_full_response(prompt: str) -> dict[str, str]:
    team = build_team()
    return team.run_with_trace(prompt)


@app.post(
    "/v1/respond",
    response_model=ResponseEnvelope,
    tags=["Responses"],
    summary="Get full multi-agent response",
    description="Runs the complete multi-agent flow and returns the final response in a stable envelope.",
)
def respond(request: ResponseRequest) -> ResponseEnvelope:
    request_id = ensure_request_id(request.request_id)
    try:
        trace = _generate_full_response(request.prompt)
        return ResponseEnvelope(
            request_id=request_id,
            status="success",
            event="final",
            data=trace,
        )
    except InputCheckError as exc:
        return ResponseEnvelope(
            request_id=request_id,
            status="error",
            event="error",
            data={},
            error=str(exc),
        )


@app.get(
    "/v1/respond/stream-info",
    response_model=StreamInfoResponse,
    tags=["Responses"],
    summary="WebSocket contract documentation",
    description="Swagger-readable documentation for the streaming endpoint URI and envelope contract.",
)
def stream_info() -> StreamInfoResponse:
    return StreamInfoResponse(
        websocket_uri="/v1/respond/stream",
        accepted_payload={"prompt": "string", "request_id": "optional-string"},
        envelope_keys=["request_id", "status", "event", "data", "error"],
    )


@app.websocket("/v1/respond/stream")
async def stream_respond(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        payload = ResponseRequest.model_validate(await websocket.receive_json())
        request_id = ensure_request_id(payload.request_id)

        await websocket.send_json(
            ResponseEnvelope(
                request_id=request_id,
                status="success",
                event="start",
                data={"message": "stream_started"},
            ).model_dump()
        )

        trace = _generate_full_response(payload.prompt)
        response_text = trace["final_response"]

        for token in response_text.split():
            await websocket.send_json(
                ResponseEnvelope(
                    request_id=request_id,
                    status="success",
                    event="chunk",
                    data={"chunk": token},
                ).model_dump()
            )

        await websocket.send_json(
            ResponseEnvelope(
                request_id=request_id,
                status="success",
                event="final",
                data=trace,
            ).model_dump()
        )
        await websocket.send_json(
            ResponseEnvelope(
                request_id=request_id,
                status="success",
                event="end",
                data={"message": "stream_completed"},
            ).model_dump()
        )
    except InputCheckError as exc:
        await websocket.send_json(
            ResponseEnvelope(
                request_id="unknown",
                status="error",
                event="error",
                data={},
                error=str(exc),
            ).model_dump()
        )
    except WebSocketDisconnect:
        return
