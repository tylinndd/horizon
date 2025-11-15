"""
OpenRouter LLM API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.services.llm_service import LLMService
from app.core.config import settings

router = APIRouter()


class LLMQueryRequest(BaseModel):
    query: str
    context: Optional[dict] = None


class LLMQueryResponse(BaseModel):
    response: str


@router.post("/query", response_model=LLMQueryResponse)
async def query_llm(
    request: LLMQueryRequest
):
    """Query OpenRouter LLM with a natural language question"""
    if not settings.OPENROUTER_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OpenRouter API key not configured"
        )
    
    try:
        llm_service = LLMService()
        response = await llm_service.query(request.query, request.context)
        return LLMQueryResponse(response=response)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error querying LLM: {str(e)}"
        )


@router.post("/explain-risk")
async def explain_risk(
    region_id: str,
    risk_score: float,
    context: Optional[dict] = None
):
    """Get natural language explanation of a risk score"""
    if not settings.OPENROUTER_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OpenRouter API key not configured"
        )
    
    prompt = f"""Explain why Region {region_id} has a risk score of {risk_score:.2%} for potential outbreak.
    
    Provide a clear, concise explanation suitable for healthcare professionals.
    Focus on the key contributing factors."""
    
    if context:
        prompt += f"\n\nAdditional context: {context}"
    
    try:
        llm_service = LLMService()
        response = await llm_service.query(prompt)
        return {"explanation": response}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating explanation: {str(e)}"
        )

