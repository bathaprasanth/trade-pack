from duckduckgo_search import DDGS
import logging

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self):
        self.ddgs = DDGS()

    def search_sector_news(self, sector: str, max_results: int = 5):
        """
        Searches for recent news and market data for the given sector.
        """
        # Simplified query to get better hits
        query = f"{sector} sector trade opportunities india"
        try:
            # text search
            results = self.ddgs.text(query, max_results=max_results, region="in-en")
            return results
        except Exception as e:
            logger.error(f"Error searching for sector {sector}: {e}")
            return []

search_service = SearchService()
