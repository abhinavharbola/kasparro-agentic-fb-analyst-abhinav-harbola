from src.utils import llm_call

class CreativeAgent:
    def __init__(self, config):
        self.config = config

    def generate(self, low_perf_messages):
        response = llm_call("prompts/creative.md", {"current_message": str(low_perf_messages)}, self.config)
        return response