from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .model import load_artifacts
from . import routers


# ── Startup / shutdown lifecycle ─────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model artifacts once when the server starts."""
    print("Loading model artifacts...")
    load_artifacts()
    print("Model loaded successfully. Server is ready.")
    yield
    print("Server shutting down.")


# ── App factory ───────────────────────────────────────────────────────────────

app = FastAPI(
    title="F1 Racer Diet Planning API",
    description=(
        "Predicts calories burned by an F1 racer based on biometric and "
        "session data, then returns a personalised diet recommendation."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# ── CORS (allow Streamlit frontend to call this API) ─────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # tighten this in production (e.g. your domain)
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routers ───────────────────────────────────────────────────────────────────

app.include_router(routers.health.router)
app.include_router(routers.predict.router)
