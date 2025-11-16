#!/bin/bash
# Render build script - builds both backend and frontend
# This runs migrations automatically on deploy

set -e

echo "===== Python Version Check ====="
python --version
python -c "import sys; print(f'Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
echo "================================"

echo "Upgrading pip and build tools..."
pip install --upgrade pip setuptools wheel

echo "Installing Python dependencies..."
# Install setuptools and wheel first
pip install setuptools>=65.0.0 wheel>=0.38.0
# Then install rest of dependencies with binary wheel preference
pip install --only-binary=:all: -r requirements.txt || pip install -r requirements.txt

echo "Running database migrations..."
alembic upgrade head

echo "===== Building Frontend ====="
cd ../frontend

echo "Installing Node dependencies..."
npm install --legacy-peer-deps

echo "Building React app..."
npm run build

echo "Verifying build output..."
ls -la dist/

echo "================================"
echo "✅ Build complete! Backend + Frontend ready"
echo "================================"

