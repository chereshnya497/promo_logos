"""
Pydantic models for request and response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal


class LogoRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Natural language description of the logo",
        example="A modern fintech startup logo with a stylized arrow and the letter F",
    )
    style: Literal[
        "minimalist", "corporate", "retro", "modern", "gradient", "hand_drawn"
    ] = Field(default="minimalist", description="Visual style preset")
    colors: Optional[List[str]] = Field(
        default=None,
        description="Preferred hex color codes (e.g. ['#FF5733', '#FFFFFF'])",
        max_length=5,
    )
    format: Literal["png", "jpg", "webp"] = Field(
        default="png", description="Output image format"
    )
    size: Optional[str] = Field(
        default=None,
        description="Image size override (e.g. '512x512'). Defaults to settings value.",
    )


class LogoResponse(BaseModel):
    id: str = Field(..., description="Unique logo identifier")
    url: str = Field(..., description="Relative URL to download the generated logo")
    prompt: str = Field(..., description="Original client prompt")
    style: str = Field(..., description="Style preset used")
    created_at: str = Field(..., description="ISO 8601 creation timestamp")


class LogoListResponse(BaseModel):
    logos: List[LogoResponse]
    total: int
    limit: int
    offset: int


class ErrorResponse(BaseModel):
    detail: str
