#!/bin/bash
# Render build script for backend
# This runs migrations automatically on deploy

set -e

echo "===== Python Version Check ====="
python --version
python -c "import sys; print(f'Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
echo "================================"

echo "Upgrading pip and build tools..."
pip install --upgrade pip setuptools wheel

echo "Installing dependencies..."
# Install setuptools and wheel first
pip install setuptools>=65.0.0 wheel>=0.38.0
# Then install rest of dependencies with binary wheel preference
pip install --only-binary=:all: -r requirements.txt || pip install -r requirements.txt

echo "Running database migrations..."
alembic upgrade head

echo "Build complete!"

