"""
Exercise 4.B.3 — Prediction Endpoint with Pydantic Models
Guide: docs/curriculum/06-fastapi-professional.md
"""

# from fastapi import FastAPI
# from pydantic import BaseModel, Field


# TODO: Define PredictionRequest
# class PredictionRequest(BaseModel):
#     feature1: float = Field(..., description="First feature")
#     feature2: float = Field(..., description="Second feature")
#     feature3: float = Field(..., description="Third feature")


# TODO: Define PredictionResponse
# class PredictionResponse(BaseModel):
#     prediction: float
#     confidence: float
#     model_version: str = "1.0.0"


# TODO: Create app and prediction endpoint
# app = FastAPI()
#
# @app.post("/predict", response_model=PredictionResponse)
# async def predict(request: PredictionRequest):
#     # Dummy prediction logic
#     prediction = request.feature1 * 0.5 + request.feature2 * 0.3 + request.feature3 * 0.2
#     return PredictionResponse(
#         prediction=prediction,
#         confidence=0.95,
#     )
