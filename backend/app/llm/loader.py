
from langchain_community.llms import Ollama

class LLMManager:
    def __init__(self):
        self.model = "mistral"

    def get_llm(self):
        return Ollama(model=self.model, temperature=0.2, num_ctx=8192)
