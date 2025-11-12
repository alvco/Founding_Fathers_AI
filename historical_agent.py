# historical_agent.py
import json
from typing import Dict, Any

class HistoricalAgent:
    def __init__(self, name: str, persona_profile: str, all_prompts: Dict, specialist_agents: Dict):
        self.name = name
        self.persona_profile = persona_profile
        self.all_prompts = all_prompts
        self.specialist_agents = specialist_agents
        self.founder_key = name.split(' ')[-1]

    def _get_prompts(self, agent_name: str, prompt_type: str) -> (str, str):
        prompts = self.all_prompts[agent_name]
        if self.founder_key in prompts and 'system_prompt' in prompts[self.founder_key]:
            system_prompt = prompts[self.founder_key]['system_prompt']
        else:
            system_prompt = prompts.get('system_prompt', '')
        user_prompt_template = prompts.get(prompt_type)
        return system_prompt, user_prompt_template

    def _format_user_prompt(self, agent_name: str, template: str, dynamic_vars: Dict = None) -> str:
        all_vars = self.all_prompts[agent_name][self.founder_key].get('prompt_variables', {})
        if dynamic_vars:
            all_vars.update(dynamic_vars)
        if all_vars:
            return template.format(**all_vars)
        return template

    def generate_complex_response(self, topic: str, debate_history: str) -> str:
        print(f"\n--- Running COMPLEX Pipeline for {self.name} ---")
        
        # Step 1: Selector
        system_prompt, user_template = self._get_prompts('SelectorAgent', 'base_user_prompt')
        user_prompt = self._format_user_prompt('SelectorAgent', user_template, {"topic_variable": topic, "persona_profile_variable": self.persona_profile})
        selector_output = self.specialist_agents["selector"].run(system_prompt, user_prompt)
        if "error" in selector_output: return f"({self.name}'s Selector agent failed: {selector_output.get('response', '')})"
        
        # Step 2: Researcher
        research_dossier = self.specialist_agents["researcher"].run(selector_output, topic, self.name)

        # Step 3: Thinker
        system_prompt, user_template = self._get_prompts('ThinkerAgent', 'complex_user_prompt')
        user_prompt = user_template.format(
            topic_variable=topic,
            selector_output_json=json.dumps(selector_output, indent=2), 
            researcher_dossier_text=json.dumps(research_dossier, indent=2), 
            persona_profile_text=self.persona_profile
        )
        thinker_output = self.specialist_agents["thinker"].run(system_prompt, user_prompt)
        if "error" in thinker_output: return f"({self.name}'s Thinker agent failed: {thinker_output.get('response', '')})"

        # Step 4: Validator
        system_prompt, user_template = self._get_prompts('ValidatorAgent', 'base_user_prompt')
        user_prompt = self._format_user_prompt('ValidatorAgent', user_template, {"thinker_output_json": json.dumps(thinker_output, indent=2), "selector_output_json": json.dumps(selector_output, indent=2), "persona_profile_text": self.persona_profile})
        validator_output = self.specialist_agents["validator"].run(system_prompt, user_prompt)
        
        if "error" in validator_output: return f"({self.name}'s Validator agent failed: {validator_output.get('response', '')})"
        
        # SIMPLIFIED LOGIC: Directly get the text from the simpler JSON
        winning_argument = validator_output.get("winning_argument_text", "")
        if not winning_argument: return f"({self.name}'s Validator agent failed to select an argument.)"

        # Step 5: Red Team
        system_prompt, user_template = self._get_prompts('RedTeamAgent', 'base_user_prompt')
        user_prompt = self._format_user_prompt('RedTeamAgent', user_template, {"validator_winning_argument": winning_argument})
        red_team_output = self.specialist_agents["red_team"].run(system_prompt, user_prompt)
        if "error" in red_team_output: return f"({self.name}'s Red Team agent failed: {red_team_output.get('response', '')})"

        # Step 6: Strategist
        system_prompt, user_template = self._get_prompts('StrategistAgent', 'base_user_prompt')
        user_prompt = self._format_user_prompt('StrategistAgent', user_template, {"red_team_output_json": json.dumps(red_team_output, indent=2), "persona_profile_text": self.persona_profile})
        strategist_output = self.specialist_agents["strategist"].run(system_prompt, user_prompt)
        if "error" in strategist_output: return f"({self.name}'s Strategist agent failed: {strategist_output.get('response', '')})"

        # Step 7: Final Judge
        system_prompt, user_template = self._get_prompts('FinalJudgeAgent', 'user_prompt_template')
        user_prompt = user_template.format(original_argument_text=winning_argument, strategist_output_json=json.dumps(strategist_output, indent=2))
        final_judge_output = self.specialist_agents["final_judge"].run(system_prompt, user_prompt)
        if "error" in final_judge_output: return f"({self.name}'s Final Judge agent failed: {final_judge_output.get('response', '')})"

        # Step 8: Communicator
        system_prompt, user_template = self._get_prompts('CommunicatorAgent', 'base_user_prompt')
        user_prompt = self._format_user_prompt(
            'CommunicatorAgent', 
            user_template, 
            {
                "final_judge_output_json": json.dumps(final_judge_output, indent=2), 
                "debate_history_text": debate_history, 
                "persona_profile_text": self.persona_profile,
                "topic_variable": topic
            }
        )
        communicator_output = self.specialist_agents["communicator"].run(system_prompt, user_prompt)
        if "error" in communicator_output: return f"({self.name}'s Communicator agent failed: {communicator_output.get('response', '')})"
        
        return communicator_output.get("final_statement", f"({self.name} could not formulate a final statement.)")

    def generate_simple_response(self, topic: str, debate_history: str) -> str:
        """Runs the simplified 4-agent pipeline."""
        print(f"\n--- Running SIMPLE Pipeline for {self.name} ---")

        # Step 1: Selector
        system_prompt, user_template = self._get_prompts('SelectorAgent', 'base_user_prompt')
        user_prompt = self._format_user_prompt('SelectorAgent', user_template, {"topic_variable": topic, "persona_profile_variable": self.persona_profile})
        selector_output = self.specialist_agents["selector"].run(system_prompt, user_prompt)
        if "error" in selector_output: return f"({self.name}'s Selector agent failed: {selector_output.get('response', '')})"

        # Step 2: Researcher
        research_dossier = self.specialist_agents["researcher"].run(selector_output, topic, self.name)
        
        # Step 3: Thinker (using the simple prompt)
        system_prompt, user_template = self._get_prompts('ThinkerAgent', 'simple_user_prompt')
        user_prompt = user_template.format(selector_output_json=json.dumps(selector_output, indent=2), researcher_dossier_text=json.dumps(research_dossier, indent=2), persona_profile_text=self.persona_profile)
        thinker_output = self.specialist_agents["thinker"].run(system_prompt, user_prompt)
        if "error" in thinker_output: return f"({self.name}'s simple Thinker agent failed: {thinker_output.get('response', '')})"

        # Repackage the Thinker's output for the Communicator
        argument_text_from_thinker = thinker_output.get("argument", "")
        communicator_brief = { "final_argument_text": argument_text_from_thinker }

        # Step 4: Communicator
        system_prompt, user_template = self._get_prompts('CommunicatorAgent', 'base_user_prompt')
        user_prompt = self._format_user_prompt(
            'CommunicatorAgent', 
            user_template, 
            {
                "final_judge_output_json": json.dumps(communicator_brief, indent=2), 
                "debate_history_text": debate_history, 
                "persona_profile_text": self.persona_profile,
                "topic_variable": topic
            }
        )
        communicator_output = self.specialist_agents["communicator"].run(system_prompt, user_prompt)
        if "error" in communicator_output: return f"({self.name}'s Communicator agent failed: {communicator_output.get('response', '')})"

        return communicator_output.get("final_statement", f"({self.name} could not formulate a final statement.)")