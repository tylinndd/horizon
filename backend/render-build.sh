#!/bin/bash
# Render build script for backend
# This runs migrations automatically on deploy

set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running database migrations..."
alembic upgrade head

echo "Build complete!"

