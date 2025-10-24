FROM python:3.12-slim

WORKDIR /app

# Install build deps.
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     python3-dev \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# Copy uv binary.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV VIRTUAL_ENV=/.venv
ENV UV_PROJECT_ENVIRONMENT=/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=/app

# Copy project files.
COPY . .

# Run uv sync (will create .venv in /app).
RUN uv sync

# Create logs directory.
RUN mkdir -p logs

# Run the application
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]