import json

from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import StreamingResponse

from app.schemas.travel import TravelPlanRequest, TravelPlanResponse
from app.services.travel_planner import (
    generate_travel_plan,
    stream_travel_plan_events,
)
from app.logger import get_logger

log = get_logger(__name__)

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    log.info("Health check — OK")
    return {"status": "ok"}


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
