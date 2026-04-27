from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class ResponseRequest(BaseModel):
    """Request payload for synchronous and streaming response generation."""

    prompt: str = Field(min_length=1, description="User prompt that should be handled by the multi-agent system.")
    request_id: str | None = Field(
        default=None,
        description="Optional caller-provided request id. If omitted, a UUID is generated.",
    )


class ResponseEnvelope(BaseModel):
    """Consistent envelope for API and WebSocket responses."""

    request_id: str = Field(description="Request identifier used to correlate all events.")
    status: Literal["success", "error"] = Field(description="Processing status.")
    event: Literal["start", "chunk", "final", "end", "error"] = Field(
        description="Event type for synchronous and streaming flows."
    )
    data: dict[str, Any] = Field(default_factory=dict, description="Event payload.")
    error: str | None = Field(default=None, description="Error message when status=error.")


class StreamInfoResponse(BaseModel):
    """Swagger-visible documentation for the WebSocket contract."""

    websocket_uri: str
    accepted_payload: dict[str, str]
    envelope_keys: list[str]


def ensure_request_id(request_id: str | None) -> str:
    return request_id or str(uuid4())
