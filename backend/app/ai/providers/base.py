from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseAIProvider(ABC):
    @abstractmethod
    async def generate_reply(
        self,
        prompt: str,
        system_instruction: str,
        history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate a text response from the configured LLM provider.
        """
        pass

