from fastapi import FastAPI

from app.core.config import settings
from app.routes.companies import router as companies_router
from app.routes.equipment import router as equipment_router
from app.routes.service_jobs import router as service_jobs_router

app = FastAPI(title=settings.app_name)
app.include_router(companies_router)
app.include_router(equipment_router)
app.include_router(service_jobs_router)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.environment,
    }