import os
from dotenv import load_dotenv
from together import Together
from typing import List, Dict, Optional

load_dotenv()

class BaseAgent:
    def __init__(self):
        self.client = Together()
        self.client.api_key = os.getenv("TOGETHER_API_KEY")

    async def get_llm_response(self, messages: List[Dict], stream: bool = True) -> str:
        """Get response from LLM and return the actual content"""
        try:
            response = self.client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
                messages=messages,
                temperature=0.7,
                top_p=0.7,
                top_k=50,
                repetition_penalty=1,
                stop=["<|eot_id|>", "<|eom_id|>"],
                stream=False  # Changed to False for simpler handling
            )
            
            # Extract the actual content from the response
            if hasattr(response, 'choices') and len(response.choices) > 0:
                return response.choices[0].message.content
            return "No response generated"
            
        except Exception as e:
            print(f"Error in LLM response: {str(e)}")
            return f"Error: {str(e)}" 