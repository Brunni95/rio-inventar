# backend/app/main.py
import os
import time
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging_config import setup_logging
from app.core.error_handlers import init_error_handlers
from app.auth import load_jwks
from app.api.v1.endpoints import assets, locations, manufacturers, statuses, suppliers, asset_types, users

# --- Setup logging first ---
setup_logging()
logger = logging.getLogger("request_logger")

# --- App init ---
app = FastAPI(title="RIO-Inventar API")

# --- CORS ---
ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*")
allow_origins = [o.strip() for o in ALLOW_ORIGINS.split(",")] if ALLOW_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request logging middleware ---
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        ms = (time.time() - start) * 1000.0
        logger.info("%s %s Status: %s Time: %.2fms", request.method, request.url.path, response.status_code, ms)
        return response

app.add_middleware(RequestLoggingMiddleware)

# --- Errors ---
init_error_handlers(app)

# --- Config ---
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
DISABLE_AUTH = os.getenv("DISABLE_AUTH", "0") in ("1", "true", "True")

# --- Startup: JWKS laden, wenn Auth aktiv ---
@app.on_event("startup")
async def on_startup():
    if not DISABLE_AUTH:
        await load_jwks()

# --- Router registrieren ---
app.include_router(assets.router,        prefix=f"{API_PREFIX}/assets",         tags=["Assets"])
app.include_router(locations.router,     prefix=f"{API_PREFIX}/locations",      tags=["Locations"])
app.include_router(manufacturers.router, prefix=f"{API_PREFIX}/manufacturers",  tags=["Manufacturers"])
app.include_router(statuses.router,      prefix=f"{API_PREFIX}/statuses",       tags=["Statuses"])
app.include_router(suppliers.router,     prefix=f"{API_PREFIX}/suppliers",      tags=["Suppliers"])
app.include_router(asset_types.router,   prefix=f"{API_PREFIX}/asset-types",    tags=["Asset Types"])
app.include_router(users.router,         prefix=f"{API_PREFIX}/users",          tags=["Users"])

# --- Root ---
@app.get("/")
def read_root():
    return {"message": "Willkommen bei der RIO-Inventar API!"}
