"""
Section 6 — FastAPI: Intermediate Exercises
Guide: docs/curriculum/06-fastapi-professional.md

Exercise 4.C.1 — Dependency Injection for Configuration
Exercise 4.C.2 — Dependency Injection for Business Logic
Exercise 4.C.3 — Custom Exception Handling
Exercise 4.C.4 — Request ID Middleware
"""

# from fastapi import FastAPI, Depends, Request, HTTPException
# from pydantic import BaseModel
# import uuid


# Exercise 4.C.1 — DI for Configuration
# TODO: Create a Settings class and inject it
# class Settings(BaseModel):
#     model_version: str = "1.0.0"
#     debug: bool = False
#     max_batch_size: int = 100
#
# def get_settings() -> Settings:
#     return Settings()


# Exercise 4.C.3 — Custom Exception Handling
# TODO: Create custom exceptions and handlers
# class PredictionError(Exception):
#     def __init__(self, detail: str):
#         self.detail = detail
#
# @app.exception_handler(PredictionError)
# async def prediction_error_handler(request, exc):
#     return JSONResponse(status_code=500, content={"error": exc.detail})


# Exercise 4.C.4 — Request ID Middleware
# TODO: Add a unique request ID to every request/response
# @app.middleware("http")
# async def add_request_id(request: Request, call_next):
#     request_id = str(uuid.uuid4())
#     request.state.request_id = request_id
#     response = await call_next(request)
#     response.headers["X-Request-ID"] = request_id
#     return response
