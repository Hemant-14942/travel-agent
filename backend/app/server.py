from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.logger import get_logger

log = get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Travel Planner API",
        description="FastAPI backend for a LangGraph-powered travel planner.",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router, prefix="/api")

    log.info("FastAPI app ready — routes: /api/health · /api/travel-plan · /api/travel-plan/stream")
    return app


app = create_app()
