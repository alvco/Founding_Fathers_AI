# environment.py
from historical_agent import HistoricalAgent
from typing import List, Literal

class DebateOrchestrator:
    """Manages a single-iteration simulation for comparative analysis."""
    def __init__(self, agents: List[HistoricalAgent], topic: str):
        self.agents = agents
        self.topic = topic
        self.final_statements = [f"# Simulation Topic: {self.topic}\n"]

    def run_simulation(self, model_type: Literal['simple', 'complex']):
        method_name = f"generate_{model_type}_response"
        print(f"--- Running {model_type.upper()} Model Simulation ---")
        self.final_statements.append(f"## {model_type.upper()} Model Outputs\n")

        for agent in self.agents:
            print(f"\nGenerating response for {agent.name}...")
            context = f"The topic for consideration is: {self.topic}"
            response_method = getattr(agent, method_name)
            response = response_method(self.topic, context)
            statement = f"### {agent.name}:\n{response}\n"
            self.final_statements.append(statement)
            print(f"Response for {agent.name} generated.")
        print("\n--- Simulation Complete ---")

    def save_transcript(self, filename: str):
        final_transcript = "\n".join(self.final_statements)
        with open(filename, "w", encoding='utf-8') as f:
            f.write(final_transcript)
        print(f"\nSimulation results saved to {filename}")