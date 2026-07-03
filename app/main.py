from fastapi import FastAPI

from app.core.config import settings
from app.routes.companies import router as companies_router
from app.routes.equipment import router as equipment_router
from app.routes.service_jobs import router as service_jobs_router
from app.routes.invitations import router as invitations_router
from app.routes.auth import router as auth_router

from app.routes.account_activation import (
    router as account_activation_router,
)

app = FastAPI(title=settings.app_name)
app.include_router(companies_router)
app.include_router(equipment_router)
app.include_router(service_jobs_router)
app.include_router(invitations_router)
app.include_router(account_activation_router)
app.include_router(auth_router)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.environment,
    }