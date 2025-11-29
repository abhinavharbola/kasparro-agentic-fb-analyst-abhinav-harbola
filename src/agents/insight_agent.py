import json
from src.utils import llm_call

class InsightAgent:
    def __init__(self, config):
        self.config = config

    def analyze(self, data_summary):
        """
        Generates hypotheses based on data summaries.
        """
        response = llm_call(
            prompt_file="prompts/insight.md",
            context={"data_summary": data_summary},
            config=self.config
        )
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "hypothesis": "Error parsing insight.",
                "primary_metric": "none"
            }