"""
Horizon FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Include routers
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(risk.router, prefix="/api/risk", tags=["risk"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])
app.include_router(fintech.router, prefix="/api/fintech", tags=["fintech"])
app.include_router(llm.router, prefix="/api/llm", tags=["llm"])
app.include_router(hospital.router, prefix="/api/hospital", tags=["hospital"])


@app.get("/")
async def root():
    return {"message": "Horizon API", "version": "1.0.0"}

