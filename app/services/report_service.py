from app.services.search_service import search_service
from app.services.llm_service import llm_service
import logging

logger = logging.getLogger(__name__)

class ReportService:
    async def generate_report(self, sector: str) -> str:
        logger.info(f"Generating report for {sector}")
        
        # 1. Search for data
        search_results = search_service.search_sector_news(sector)
        
        # 2. Analyze with LLM
        report_content = await llm_service.analyze_sector(sector, search_results)
        
        return report_content

report_service = ReportService()
