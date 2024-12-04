from typing import Dict, List
from .base_agent import BaseAgent
from .wiki_agent import WikipediaAgent
from .google_agent import GoogleSearchAgent
import asyncio

class CoordinatorAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.wiki_agent = WikipediaAgent()
        self.google_agent = GoogleSearchAgent()
        
    async def coordinate_search(self, query: str) -> Dict:
        """Coordinate parallel searches and combine results"""
        try:
            # Run searches in parallel
            wiki_task = asyncio.create_task(self.wiki_agent.search(query))
            google_task = asyncio.create_task(self.google_agent.search(query))
            
            results = await asyncio.gather(wiki_task, google_task)
            wiki_result, google_result = results
            
            # Create prompt for result analysis
            messages = [
                {"role": "system", "content": "You are a coordinator that analyzes and combines information from multiple sources."},
                {"role": "user", "content": f"""Analyze and combine the following results for the query: {query}
                
                Wikipedia Results: {wiki_result['answer']}
                Google Search Results: {google_result['answer']}
                
                Provide a comprehensive answer that combines the best information from both sources."""}
            ]
            
            # Get combined response
            final_response = await self.get_llm_response(messages)
            
            return {
                "combined_answer": final_response,
                "wikipedia_result": wiki_result,
                "google_result": google_result
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "agent_type": "coordinator"
            } 