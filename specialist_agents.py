# specialist_agents.py
from base_agent import BaseAgent
from rag_system import RAGSystem
from typing import Dict, Any

class SelectorAgent(BaseAgent):
    def __init__(self): super().__init__(name="Selector")
    def run(self, s: str, u: str) -> Dict: return self.execute_task(s, u, 800)

class ThinkerAgent(BaseAgent):
    def __init__(self): super().__init__(name="Thinker")
    def run(self, s: str, u: str) -> Dict: return self.execute_task(s, u, 4000)

class ValidatorAgent(BaseAgent):
    def __init__(self): super().__init__(name="Validator")
    def run(self, s: str, u: str) -> Dict: return self.execute_task(s, u, 4000)

class RedTeamAgent(BaseAgent):
    def __init__(self): super().__init__(name="RedTeam")
    def run(self, s: str, u: str) -> Dict: return self.execute_task(s, u, 4000)

class StrategistAgent(BaseAgent):
    def __init__(self): super().__init__(name="Strategist")
    def run(self, s: str, u: str) -> Dict: return self.execute_task(s, u, 4000)

class FinalJudgeAgent(BaseAgent):
    def __init__(self): super().__init__(name="FinalJudge")
    def run(self, s: str, u: str) -> Dict: return self.execute_task(s, u, 4000)

class CommunicatorAgent(BaseAgent):
    def __init__(self): super().__init__(name="Communicator")
    def run(self, s: str, u: str) -> Dict: return self.execute_task(s, u, 2000)

class ArbiterAgent(BaseAgent):
    def __init__(self): super().__init__(name="Arbiter")
    def run(self, s: str, u: str) -> Dict: return self.execute_task(s, u, 4000)

class ResearcherAgent:
    def __init__(self, rag_system: RAGSystem):
        self.rag_system = rag_system
        self.name = "Researcher"
        
    def run(self, selector_output: Dict, topic: str, author_name: str) -> Dict[str, str]:
        print(f"     > Executing task for agent: {self.name} for {author_name}...")
        
        # Safely extract core principle
        core_principle = selector_output.get("core_principle", "")
        
        # Safely extract historical precedent issue
        precedent_value = selector_output.get("historical_precedent", {})
        precedent_issue = ""
        if isinstance(precedent_value, dict):
            precedent_issue = precedent_value.get("issue", "")
        else:
            print(f"    WARN: {self.name} expected a dictionary for 'historical_precedent', but got {type(precedent_value)}. Value: {precedent_value}")

        # --- CORRECTED LOGIC FOR ALLIED THINKER ---
        allied_thinker_value = selector_output.get("allied_thinker", {})
        allied_thinker_name = ""
        allied_thinker_key = ""
        
        if isinstance(allied_thinker_value, dict):
            allied_thinker_name = allied_thinker_value.get("name", "")
            if allied_thinker_name and isinstance(allied_thinker_name, str):
                 allied_thinker_key = allied_thinker_name.split(' ')[-1].lower()
        else:
             print(f"    WARN: {self.name} expected a dictionary for 'allied_thinker', but got {type(allied_thinker_value)}. Value: {allied_thinker_value}")
             # Optionally, handle if the value itself might be the name as a string
             if isinstance(allied_thinker_value, str):
                 allied_thinker_name = allied_thinker_value # Use the string directly if needed
                 # allied_thinker_key = allied_thinker_name.split(' ')[-1].lower() # Uncomment if you want to try using the string as name
        # --- END OF CORRECTION ---

        author_key = author_name.split(' ')[-1].lower()
        
        principle_text = self.rag_system.query(f"On '{topic}', what are {author_name}'s views on '{core_principle}'?", author=author_key, top_k=3)
        precedent_text = self.rag_system.query(f"Details of '{precedent_issue}' from {author_name}'s writings?", author=author_key, top_k=3)
        
        allied_thinker_text = ""
        if allied_thinker_key: # Only query if we successfully got a key
            allied_thinker_text = self.rag_system.query(f"Ideas of '{allied_thinker_name}' on '{core_principle}'?", author=allied_thinker_key, top_k=2)
        
        return {
            "principle_text": principle_text,
            "precedent_text": precedent_text,
            "allied_thinker_text": allied_thinker_text
        }