from fastapi import APIRouter, Depends, HTTPException, Request
from app.services.report_service import report_service
from app.core.security import get_api_key

router = APIRouter()

@router.get("/analyze/{sector}")
async def analyze_sector(
    request: Request,
    sector: str, 
    api_key: str = Depends(get_api_key)
):
    """
    Analyzes trade opportunities for a specific sector.
    Requires 'X-API-Key: gemini-trade-api' header.
    Rate limit: 5 requests per minute.
    """
    if not sector:
        raise HTTPException(status_code=400, detail="Sector name is required")
        
    try:
        report = await report_service.generate_report(sector)
        return {"sector": sector, "analysis_report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
