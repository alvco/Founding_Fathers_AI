# run_simple_model.py
import yaml
from dotenv import load_dotenv
load_dotenv()

from environment import DebateOrchestrator
from rag_system import RAGSystem
from historical_agent import HistoricalAgent
from specialist_agents import SelectorAgent, ResearcherAgent, ThinkerAgent, CommunicatorAgent

def load_persona_profile(founder_name: str) -> str:
    try:
        filename = f"corpora/{founder_name.lower().split(' ')[-1]}.txt"
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"ERROR: Persona profile for {founder_name} not found.")
        return ""

def run_simple_simulation():
    print("--- Initializing SIMPLE Model Simulation ---")
    try:
        rag_system = RAGSystem(corpora_path="corpora")
        with open("prompts.yaml", "r") as f:
            all_prompts = yaml.safe_load(f)
    except Exception as e:
        print(f"ERROR during setup: {e}")
        return
    
    specialist_agents = {
        "selector": SelectorAgent(),
        "researcher": ResearcherAgent(rag_system=rag_system),
        "thinker": ThinkerAgent(),
        "communicator": CommunicatorAgent()
    }

    founders = ["Alexander Hamilton", "Thomas Jefferson", "James Madison"]
    agents = []
    for name in founders:
        profile = load_persona_profile(name)
        if profile:
            agents.append(HistoricalAgent(name=name, persona_profile=profile, all_prompts=all_prompts, specialist_agents=specialist_agents))

    debate_topic = "Should the United States annex and incorporate Canada and Mexico to form a continental super-national to strengthen its economic and political power and influence?"
    orchestrator = DebateOrchestrator(agents, debate_topic)
    orchestrator.run_simulation(model_type='simple')
    orchestrator.save_transcript(filename="simple_model_results.md")
    print("\n--- Simple Simulation Complete ---")

if __name__ == "__main__":
    run_simple_simulation()