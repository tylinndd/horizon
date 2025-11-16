#!/bin/bash
# Render build script for backend
# This runs migrations automatically on deploy

set -e

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
# Use --only-binary to prefer pre-built wheels and avoid compilation
pip install --only-binary=:all: -r requirements.txt || pip install -r requirements.txt

echo "Running database migrations..."
alembic upgrade head

echo "Build complete!"

