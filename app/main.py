from fastapi import FastAPI

from app.core.config import settings
from app.routes.companies import router as companies_router

app = FastAPI(title=settings.app_name)

app.include_router(companies_router)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.environment,
    }