import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import Any, Dict, List
from .base_tool import BaseTool
import os
import json
import string

class WebSearchTool(BaseTool):
    def __init__(self, serper_api_key: str):
        super().__init__(name="web_search", description="Search the web and retrieve content from webpages")
        self.serper_api_key = serper_api_key
        self.search_url = "https://google.serper.dev/search"
        self.max_retries = 3

    async def run(self, query: str) -> Dict[str, Any]:
        search_results = await self.fetch_search_results(query)
        best_url = await self.get_best_url(search_results)
        content = await self.scrape_website_content(best_url)
        return {"source": best_url, "content": content}

    async def fetch_search_results(self, query: str) -> List[Dict[str, Any]]:
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': self.serper_api_key
        }
        payload = json.dumps({"q": query})

        async with aiohttp.ClientSession() as session:
            async with session.post(self.search_url, headers=headers, data=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('organic', [])
                else:
                    raise Exception(f"Search API returned status code {response.status}")

    async def get_best_url(self, search_results: List[Dict[str, Any]]) -> str:
        # For simplicity, we're just returning the first result's URL
        # In a more advanced implementation, you might want to use an LLM to choose the best URL
        return search_results[0]['link']

    async def scrape_website_content(self, url: str) -> str:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        }

        for _ in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers, timeout=15) as response:
                        if response.status == 200:
                            content = await response.text()
                            soup = BeautifulSoup(content, 'html.parser')
                            text = soup.get_text(separator='\n')
                            clean_text = '\n'.join([line.strip() for line in text.splitlines() if line.strip()])
                            return ' '.join(clean_text.split()[:5000])  # First 5000 words
                        else:
                            raise Exception(f"HTTP error: {response.status}")
            except Exception as e:
                print(f"Error scraping {url}: {str(e)}. Retrying...")
                await asyncio.sleep(1)
        
        raise Exception(f"Failed to scrape {url} after {self.max_retries} attempts")

    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"}
            },
            "required": ["query"]
        }