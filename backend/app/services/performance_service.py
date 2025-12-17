import aiohttp
from typing import Dict, Any
from app.config import get_settings

class PerformanceService:
    """Service for fetching Lighthouse metrics via PageSpeed Insights API"""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        
    async def get_lighthouse_metrics(self, url: str) -> Dict[str, Any]:
        """
        Fetch Lighthouse metrics for a given URL
        """
        params = {
            "url": url,
            "category": ["performance", "accessibility", "best-practices", "seo"],
            "strategy": "mobile" # Default to mobile as it's more critical for SEO
        }
        
        # Add API key if available
        if self.settings.GOOGLE_API_KEY:
            params["key"] = self.settings.GOOGLE_API_KEY
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params, timeout=60) as response:
                    if response.status == 200:
                        data = await response.json()
                        categories = data.get("lighthouseResult", {}).get("categories", {})
                        
                        return {
                            "performance": categories.get("performance", {}).get("score", 0) * 100,
                            "accessibility": categories.get("accessibility", {}).get("score", 0) * 100,
                            "best_practices": categories.get("best-practices", {}).get("score", 0) * 100,
                            "seo": categories.get("seo", {}).get("score", 0) * 100,
                        }
                    else:
                        print(f"PageSpeed API error: {response.status}")
                        return self._get_empty_metrics()
        except Exception as e:
            print(f"Error fetching Lighthouse metrics: {e}")
            return self._get_empty_metrics()
            
    def _get_empty_metrics(self) -> Dict[str, Any]:
        return {
            "performance": None,
            "accessibility": None,
            "best_practices": None,
            "seo": None,
        }
