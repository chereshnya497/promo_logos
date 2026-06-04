"""
PromoLogos - AI-Powered Logo Generator
FastAPI application entry point
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.routes.api import router as api_router
from app.routes.web import router as web_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    print(f"PromoLogos started. Output dir: {settings.OUTPUT_DIR}")
    yield
    print("PromoLogos shutting down.")


app = FastAPI(
    title="PromoLogos",
    description="AI-powered logo generator from client prompts",
    version="1.0.0",
    lifespan=lifespan,
)

# Mount static files and outputs
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/outputs", StaticFiles(directory=settings.OUTPUT_DIR), name="outputs")

# Register routers
app.include_router(api_router, prefix="/api")
app.include_router(web_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
