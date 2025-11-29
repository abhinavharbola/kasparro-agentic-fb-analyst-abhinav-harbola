import json
from src.utils import llm_call

class PlannerAgent:
    def __init__(self, config):
        self.config = config

    def plan(self, user_query):
        """
        Asks the LLM to break the query into steps.
        """
        response = llm_call(
            prompt_file="prompts/planner.md",
            context={"user_query": user_query},
            config=self.config
        )
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback if LLM fails
            return {"steps": ["DataAgent", "InsightAgent", "EvaluatorAgent"]}