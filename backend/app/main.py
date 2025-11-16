"""
Horizon FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.api import health, risk, alerts, fintech, llm, hospital
from app.core.config import settings

app = FastAPI(
    title="Horizon API",
    description="Outbreak detection and risk assessment platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(risk.router, prefix="/api/risk", tags=["risk"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])
app.include_router(fintech.router, prefix="/api/fintech", tags=["fintech"])
app.include_router(llm.router, prefix="/api/llm", tags=["llm"])
app.include_router(hospital.router, prefix="/api/hospital", tags=["hospital"])


@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {"message": "Horizon API", "version": "1.0.0"}


# Serve static files from React build (if exists)
frontend_build_dir = Path(__file__).parent.parent.parent / "frontend" / "dist"

if frontend_build_dir.exists():
    # Mount static files (CSS, JS, images, etc.)
    app.mount("/assets", StaticFiles(directory=str(frontend_build_dir / "assets")), name="assets")
    
    # Serve index.html for all non-API routes (SPA routing)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve React frontend for all non-API routes"""
        # If path is a file in the build directory, serve it
        file_path = frontend_build_dir / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        # Otherwise serve index.html (for React Router)
        return FileResponse(frontend_build_dir / "index.html")
else:
    # Fallback when frontend not built
    @app.get("/")
    async def root():
        return {
            "message": "Horizon API", 
            "version": "1.0.0",
            "note": "Frontend not built. Build frontend with: cd frontend && npm run build"
        }

