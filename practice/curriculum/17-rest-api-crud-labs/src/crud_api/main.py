"""FastAPI application entry point."""

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from .routes import router
from .rate_limiter import RateLimiter

app = FastAPI(
    title="CRUD API Practice Lab",
    description="REST CRUD API with proper HTTP semantics — Module 17",
    version="1.0.0",
)

rate_limiter = RateLimiter(max_requests=100, window_seconds=60)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Simple rate limiting middleware based on client IP."""
    client_ip = request.client.host if request.client else "unknown"
    if not rate_limiter.allow(client_ip):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests", "status_code": 429},
        )
    response: Response = await call_next(request)
    return response


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


app.include_router(router)
