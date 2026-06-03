from fastapi import APIRouter
from schemas import HealthResponse
from model import is_loaded

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Server health check",
)
async def health() -> HealthResponse:
    """Returns server status and whether the model has been loaded."""
    return HealthResponse(
        status="ok",
        model_loaded=is_loaded(),
        version="1.0.0",
    )
