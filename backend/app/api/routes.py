import json
import os

from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse, StreamingResponse

from app.schemas.travel import TravelPlanRequest, TravelPlanResponse
from app.services.travel_planner import (
    generate_travel_plan,
    stream_travel_plan_events,
)
from app.logger import get_logger

log = get_logger(__name__)

router = APIRouter()

SERVICE_VERSION = "0.1.0"


def build_health_response() -> tuple[dict, int]:
    provider = os.getenv("LLM_PROVIDER", "groq").strip().lower()
    llm_env = "GEMINI_API_KEY" if provider == "gemini" else "GROQ_API_KEY"

    checks = {
        llm_env.lower(): bool(os.getenv(llm_env)),
        "tavily_api_key": bool(os.getenv("TAVILY_API_KEY")),
        "aviationstack_api_key": bool(os.getenv("AVIATIONSTACK_API_KEY")),
    }

    all_ok = all(checks.values())
    body = {
        "status": "ok" if all_ok else "degraded",
        "service": "AI Travel Planner API",
        "version": SERVICE_VERSION,
        "llm_provider": provider,
        "checks": checks,
    }
    status_code = 200 if all_ok else 503
    return body, status_code


@router.get("/health")
def health_check() -> JSONResponse:
    body, status_code = build_health_response()
    log.info("Health check — %s", body["status"])
    return JSONResponse(content=body, status_code=status_code)


@router.post("/travel-plan", response_model=TravelPlanResponse)
async def create_travel_plan(request: TravelPlanRequest) -> dict:
    log.info(f"POST /travel-plan  query='{request.user_query[:80]}'")
    try:
        result = await run_in_threadpool(generate_travel_plan, request.user_query)
        log.info("POST /travel-plan  completed successfully")
        return result
    except Exception as exc:
        log.error(f"POST /travel-plan  failed — {exc}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate travel plan: {exc}",
        ) from exc


@router.post("/travel-plan/stream")
def stream_travel_plan(request: TravelPlanRequest) -> StreamingResponse:
    log.info(f"POST /travel-plan/stream  query='{request.user_query[:80]}'")

    def event_generator():
        try:
            for event in stream_travel_plan_events(request.user_query):
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as exc:
            log.error(f"Stream generator error — {exc}")
            error_event = {"type": "error", "detail": str(exc)}
            yield f"data: {json.dumps(error_event)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
