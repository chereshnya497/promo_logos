"""
Web UI routes — renders HTML pages for browser-based logo generation.
"""

from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Optional

from app.generator import generate_logo
from app.models import LogoRequest

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse, summary="Home page")
async def index(request: Request):
    """Render the main logo generation form."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": None, "error": None},
    )


@router.post("/", response_class=HTMLResponse, summary="Submit logo generation form")
async def generate_from_form(
    request: Request,
    prompt: str = Form(...),
    style: str = Form(default="minimalist"),
    colors: Optional[str] = Form(default=None),
    fmt: str = Form(default="png"),
):
    """Handle form submission and return the result page."""
    color_list = [c.strip() for c in colors.split(",")] if colors else None
    logo_req = LogoRequest(prompt=prompt, style=style, colors=color_list, format=fmt)

    try:
        result = await generate_logo(logo_req)
        return templates.TemplateResponse(
            "result.html",
            {"request": request, "result": result, "error": None},
        )
    except Exception as exc:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": None, "error": str(exc)},
        )
