from fastapi import FastAPI, APIRouter
from routes import leads_router


infra_router = APIRouter(prefix="/infra/health/check")

@infra_router.get("/", tags=["Health Check"])
async def health_check():
    return {"status": "ok"}


def create_app():
    app = FastAPI(title="Leads API", version="0.0.1")

    app.include_router(infra_router)
    app.include_router(leads_router)

    return app