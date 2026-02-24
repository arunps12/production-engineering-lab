"""
Exercise 4.B.4 — Request Logging Middleware
Guide: docs/curriculum/06-fastapi-professional.md
"""

# import time
# import logging
# from fastapi import FastAPI, Request

# app = FastAPI()
# logger = logging.getLogger(__name__)


# TODO: Add middleware that logs every request
# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     start = time.perf_counter()
#     response = await call_next(request)
#     elapsed = time.perf_counter() - start
#     logger.info(f"{request.method} {request.url.path} → {response.status_code} ({elapsed:.3f}s)")
#     return response
