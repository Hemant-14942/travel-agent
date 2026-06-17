from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import build_health_response, router
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
            "https://travel-agent-zeta-eight.vercel.app",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health",methods=["GET","HEAD"])
    def root_health_check() -> JSONResponse:
        body, status_code = build_health_response()
        return JSONResponse(content=body, status_code=status_code)

    app.include_router(router, prefix="/api")

    log.info(
        "FastAPI app ready — routes: /health · /api/health · "
        "/api/travel-plan · /api/travel-plan/stream"
    )
    return app


app = create_app()
