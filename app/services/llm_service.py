import google.generativeai as genai
from app.core.config import get_settings
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            logger.warning("GEMINI_API_KEY not set. LLM service will fail if called.")
            self.model = None

    async def analyze_sector(self, sector: str, search_results: list) -> str:
        """
        Analyzes the sector based on search results using Gemini.
        """
        if not self.model:
            return "Error: Gemini API Key not configured."

        if not search_results:
            # Fallback to internal knowledge if search fails
            context = "No live search data available. Please provide an analysis based on your general knowledge up to your cutoff."
        else:
             context = "\n".join([f"- {item['title']}: {item['body']}" for item in search_results if 'body' in item])
        
        prompt = f"""
        You are an expert market analyst for the Indian market.
        Analyze the '{sector}' sector in India.
        
        Context/Search Data:
        {context}
        
        Generate a structured Markdown report covering:
        1. **Executive Summary**: Brief overview of the sector's current state.
        2. **Key Trade Opportunities**: Specific areas with high growth potential.
        3. **Market Trends**: Current trends driving the market.
        4. **Risks & Challenges**: Potential pitfalls.
        5. **Conclusion**: Final recommendation.
        
        Format the output clearly in Markdown.
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating analysis: {e}")
            return f"Error generating analysis: {str(e)}"

llm_service = LLMService()
