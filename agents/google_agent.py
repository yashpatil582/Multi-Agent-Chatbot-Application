from typing import Dict, List
from googleapiclient.discovery import build
from .base_agent import BaseAgent
import os

class GoogleSearchAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.service = build(
            "customsearch", "v1",
            developerKey=os.getenv("GOOGLE_API_KEY")
        )
        
    async def search(self, query: str) -> Dict:
        """Perform Google search and analyze results"""
        try:
            # Perform Google search
            results = self.service.cse().list(
                q=query,
                cx=os.getenv("GOOGLE_CSE_ID"),
                num=5
            ).execute()
            
            search_results = [{
                "title": item["title"],
                "snippet": item.get("snippet", ""),
                "link": item["link"]
            } for item in results.get("items", [])]
            
            # Create prompt for LLM
            messages = [
                {"role": "system", "content": "You are a helpful assistant that analyzes search results to provide accurate answers."},
                {"role": "user", "content": f"Based on the following search results, answer the query: {query}\n\nResults:\n{str(search_results)}"}
            ]
            
            # Get LLM response
            response = await self.get_llm_response(messages)
            
            return {
                "answer": response,
                "sources": search_results,
                "agent_type": "google"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "agent_type": "google"
            } 