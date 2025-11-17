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

echo "Installing Python dependencies..."
# Install setuptools and wheel first
pip install setuptools>=65.0.0 wheel>=0.38.0
# Then install rest of dependencies with binary wheel preference
pip install --only-binary=:all: -r requirements.txt || pip install -r requirements.txt

echo "Building frontend..."
cd ../frontend
npm install
npm run build
cd ../backend

echo "Copying frontend build into backend static directory..."
rm -rf app/static
mkdir -p app/static
cp -r ../frontend/dist/* app/static/

if [ -z "$DATABASE_URL" ]; then
  echo "DATABASE_URL is not set. Skipping database migrations."
else
  echo "Running database migrations..."
  alembic upgrade head
fi

echo "================================"
echo "✅ Backend build complete!"
echo "================================"

