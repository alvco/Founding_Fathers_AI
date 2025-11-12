# base_agent.py
import anthropic
import json
import re
from abc import ABC
from typing import Dict, Any
import dirtyjson

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.llm_client = anthropic.Anthropic()

    def _execute_llm_call(self, system_prompt: str, user_prompt: str, max_tokens: int) -> str:
        """A simple, direct wrapper for the API call."""
        try:
            print(f"    > Contacting Anthropic API for {self.name}...")
            message = self.llm_client.messages.create(
                model="claude-sonnet-4-5-20250929", 
                max_tokens=max_tokens,
                temperature=0.2,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return message.content[0].text.strip()
        except anthropic.APIError as e:
            print(f"ERROR: Anthropic API error for agent {self.name}: {e}")
            return f"({self.name} is unable to respond due to an API error.)"

    def execute_task(self, system_prompt: str, user_prompt: str, max_tokens: int) -> Dict[str, Any]:
        """Executes the robust two-step 'reason-then-extract' process."""
        print(f"    > Executing task for agent: {self.name}...")

        reasoning_response_str = self._execute_llm_call(system_prompt, user_prompt, max_tokens)
        
        if reasoning_response_str.startswith("("):
            return {"error": "API call failed", "response": reasoning_response_str}

        extraction_system_prompt = "You are an expert at extracting structured data. Extract the JSON object from the provided text. Output only the valid, raw JSON object and nothing else."
        extraction_user_prompt = f"<text_to_parse>\n{reasoning_response_str}\n</text_to_parse>\n\nExtract the JSON object now."
        
        extracted_data_str = self._execute_llm_call(extraction_system_prompt, extraction_user_prompt, max_tokens=max_tokens)
        
        try:
            json_match = re.search(r'\{.*\}', extracted_data_str, re.DOTALL)
            if json_match:
                json_string = json_match.group(0)
                return dirtyjson.loads(json_string)
            else:
                raise ValueError("No JSON object found in the output to parse.")

        except Exception as e:
            print(f"ERROR: {self.name} failed to produce valid JSON even with dirtyjson. Error: {e}")
            return {"error": "JSON parsing failed", "response": extracted_data_str}