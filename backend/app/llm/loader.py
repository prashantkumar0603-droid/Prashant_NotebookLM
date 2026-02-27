
import os
from langchain_community.llms import Ollama
from langchain.llms.base import LLM
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class MockLLM(LLM):
    """Mock LLM for development and testing without external services."""
    
    @property
    def _llm_type(self) -> str:
        return "mock"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
    ) -> str:
        """Generate a simple mock response based on the prompt."""
        prompt_lower = prompt.lower()
        
        if "summarize" in prompt_lower or "summary" in prompt_lower:
            return "This document contains important information about various topics. Based on the retrieved context, the main points are: 1) The document discusses key concepts, 2) It provides detailed analysis, 3) Multiple perspectives are covered. For more specific information, please refer to the full document."
        elif "what" in prompt_lower:
            return "Based on the provided context and retrieved documents, the answer to your question is: The document addresses this topic by providing relevant information and examples. Additional context can be found in the referenced sections."
        elif "how" in prompt_lower:
            return "The process outlined in the document describes the following steps: First, you need to understand the foundational concepts. Second, apply the principles discussed. Third, implement the recommendations provided. This approach is supported by the examples and case studies in the document."
        elif "why" in prompt_lower:
            return "The document explains the reasoning behind this through several key points: The underlying factors include important considerations discussed in the text. The justification is based on evidence and analysis presented in the context. This is further supported by the specific examples provided."
        else:
            return "Based on the retrieved documents and the context provided, here is the answer to your question: The document contains relevant information that addresses your inquiry. Please refer to the specific sections cited for more detailed explanations and supporting evidence."

class LLMManager:
    def __init__(self, use_ollama: bool = False):
        """Initialize LLM Manager.
        
        Args:
            use_ollama: If True, use Ollama. If False (default), use mock LLM.
                       Can be overridden by LLM_PROVIDER env var (values: 'ollama' or 'mock')
        """
        self.use_ollama = use_ollama
        self.model = "mistral"
        
        # Check environment variable
        llm_provider = os.getenv("LLM_PROVIDER", "mock").lower()
        if llm_provider == "ollama":
            self.use_ollama = True
        elif llm_provider == "mock":
            self.use_ollama = False

    def get_llm(self):
        """Get the appropriate LLM instance."""
        if self.use_ollama:
            try:
                return Ollama(model=self.model, temperature=0.2, num_ctx=8192)
            except Exception as e:
                logger.warning(f"Failed to initialize Ollama: {e}. Falling back to MockLLM.")
                return MockLLM()
        else:
            logger.info("Using MockLLM for development. Set LLM_PROVIDER=ollama to use Ollama.")
            return MockLLM()
