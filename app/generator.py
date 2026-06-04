"""
Logo generation logic — supports OpenAI DALL-E and Stable Diffusion backends.
"""

import uuid
import httpx
import base64
from datetime import datetime, timezone
from pathlib import Path

from app.config import settings
from app.models import LogoRequest, LogoResponse


STYLE_PROMPT_MAP = {
    "minimalist": "clean minimalist flat vector logo, simple shapes, white background",
    "corporate": "professional corporate logo, sleek modern design, suitable for business",
    "retro": "vintage retro logo, bold typography, classic color palette",
    "modern": "contemporary modern logo, geometric shapes, bold colors",
    "gradient": "vibrant gradient logo, smooth color transitions, dynamic composition",
    "hand_drawn": "hand-drawn artisan logo, sketch style, organic lines",
}


def _build_prompt(request: LogoRequest) -> str:
    """Combine client prompt with style hints."""
    style_hint = STYLE_PROMPT_MAP.get(request.style, "")
    color_hint = ""
    if request.colors:
        color_hint = f", using colors: {', '.join(request.colors)}"
    return f"{request.prompt}, {style_hint}{color_hint}, logo design, vector style"


async def generate_logo(request: LogoRequest) -> LogoResponse:
    """Dispatch logo generation to the configured AI backend."""
    if settings.AI_BACKEND == "openai":
        return await _generate_openai(request)
    elif settings.AI_BACKEND == "stable_diffusion":
        return await _generate_stable_diffusion(request)
    else:
        raise ValueError(f"Unknown AI backend: {settings.AI_BACKEND}")


async def _generate_openai(request: LogoRequest) -> LogoResponse:
    """Generate logo using OpenAI DALL-E API."""
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    prompt = _build_prompt(request)

    response = await client.images.generate(
        model=settings.OPENAI_MODEL,
        prompt=prompt,
        n=1,
        size=request.size or settings.IMAGE_SIZE,
        quality=settings.IMAGE_QUALITY,
        response_format="b64_json",
    )

    image_data = base64.b64decode(response.data[0].b64_json)
    logo_id = f"logo_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    file_path = _save_image(image_data, logo_id, request.format)

    return LogoResponse(
        id=logo_id,
        url=f"/outputs/{file_path.name}",
        prompt=request.prompt,
        style=request.style,
        created_at=datetime.now(timezone.utc).isoformat(),
    )


async def _generate_stable_diffusion(request: LogoRequest) -> LogoResponse:
    """Generate logo using a local Stable Diffusion WebUI API."""
    prompt = _build_prompt(request)
    payload = {
        "prompt": prompt,
        "negative_prompt": "blurry, low quality, text errors, watermark",
        "steps": 30,
        "width": 512,
        "height": 512,
        "cfg_scale": 7,
    }

    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(f"{settings.SD_API_URL}/sdapi/v1/txt2img", json=payload)
        response.raise_for_status()
        result = response.json()

    image_data = base64.b64decode(result["images"][0])
    logo_id = f"logo_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    file_path = _save_image(image_data, logo_id, request.format)

    return LogoResponse(
        id=logo_id,
        url=f"/outputs/{file_path.name}",
        prompt=request.prompt,
        style=request.style,
        created_at=datetime.now(timezone.utc).isoformat(),
    )


def _save_image(data: bytes, logo_id: str, fmt: str = "png") -> Path:
    """Save raw image bytes to the output directory."""
    output_dir = Path(settings.OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f"{logo_id}.{fmt}"
    file_path.write_bytes(data)
    return file_path
