import wikipediaapi
from typing import Dict, List
from .base_agent import BaseAgent

class WikipediaAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        # Create a proper user agent string
        user_agent = "MultiAgentSearch/1.0 (https://github.com/yourusername/multiagentsearch; your@email.com)"
        self.wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent=user_agent
        )
        
    async def search(self, query: str) -> Dict:
        """Search Wikipedia and get relevant information"""
        try:
            # Search Wikipedia
            page = self.wiki.page(query)
            if page.exists():
                result = {
                    "title": page.title,
                    "summary": page.summary[0:1500],  # Get first 1500 chars of summary
                    "url": page.fullurl
                }
            else:
                # If exact page not found, try alternative approach
                result = {
                    "title": "No exact match found",
                    "summary": "Could not find an exact match for the query.",
                    "url": None
                }
            
            # Create prompt for LLM
            messages = [
                {"role": "system", "content": "You are a helpful assistant that analyzes Wikipedia information to provide accurate answers."},
                {"role": "user", "content": f"Based on the following Wikipedia information, answer the query: {query}\n\nInformation:\n{str(result)}"}
            ]
            
            # Get LLM response
            response = await self.get_llm_response(messages)
            
            return {
                "answer": response,
                "sources": [result],
                "agent_type": "wikipedia"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "agent_type": "wikipedia"
            } 