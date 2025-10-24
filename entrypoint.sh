#!/bin/sh
set -e

# Debug info
echo "VIRTUAL_ENV = $VIRTUAL_ENV"
echo "PATH = $PATH"
echo "Which python: $(which python)"
echo "Contents of venv bin: $(ls -l ${VIRTUAL_ENV}/bin)"

echo "Running migrations..."
alembic upgrade head
echo "Migrations completed successfully!"

echo "Starting application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000