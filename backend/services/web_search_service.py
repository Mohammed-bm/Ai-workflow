import os
import requests

class WebSearchService:
    def __init__(self):
        # Try SerpAPI first, fallback to Brave
        self.serp_api_key = os.getenv("SERPAPI_KEY")
        self.brave_api_key = os.getenv("BRAVE_API_KEY")
        
        if self.serp_api_key:
            self.provider = "serpapi"
        elif self.brave_api_key:
            self.provider = "brave"
        else:
            self.provider = None
            print("⚠️ No web search API key found")
    
    def search(self, query: str, max_results: int = 5) -> str:
        """Perform web search and return formatted results"""
        
        if not self.provider:
            return "Web search not configured."
        
        if self.provider == "serpapi":
            return self._search_serpapi(query, max_results)
        else:
            return self._search_brave(query, max_results)
    
    def _search_serpapi(self, query: str, max_results: int) -> str:
        """Search using SerpAPI"""
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": self.serp_api_key,
            "num": max_results
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = data.get("organic_results", [])
                
                formatted = []
                for r in results[:max_results]:
                    formatted.append(f"Title: {r.get('title')}\n{r.get('snippet')}\nURL: {r.get('link')}")
                
                return "\n\n".join(formatted)
            else:
                return "Web search failed."
        except Exception as e:
            print(f"SerpAPI error: {e}")
            return "Web search error."
    
    def _search_brave(self, query: str, max_results: int) -> str:
        """Search using Brave Search API"""
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.brave_api_key
        }
        params = {"q": query, "count": max_results}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = data.get("web", {}).get("results", [])
                
                formatted = []
                for r in results:
                    formatted.append(f"Title: {r.get('title')}\n{r.get('description')}\nURL: {r.get('url')}")
                
                return "\n\n".join(formatted)
            else:
                return "Web search failed."
        except Exception as e:
            print(f"Brave API error: {e}")
            return "Web search error."