# Capstone Dockerfile — Multi-stage Production Build
# Guide: docs/curriculum/20-capstone-project.md

# TODO: Build the production Dockerfile

# ---- Stage 1: Builder ----
# FROM python:3.11-slim AS builder
# WORKDIR /app
# COPY pyproject.toml ./
# RUN pip install uv && uv sync --frozen --no-dev
# COPY src/ src/

# ---- Stage 2: Runtime ----
# FROM python:3.11-slim AS runtime
# WORKDIR /app
# RUN groupadd -r appuser && useradd -r -g appuser appuser
# COPY --from=builder /app/.venv /app/.venv
# COPY --from=builder /app/src /app/src
# ENV PATH="/app/.venv/bin:$PATH"
# USER appuser
# EXPOSE 8000
# HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8000/health || exit 1
# CMD ["uvicorn", "appcore.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
