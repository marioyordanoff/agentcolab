from abc import ABC, abstractmethod
from typing import List

class BaseLLM(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """
        Generate a response based on the given prompt.
        """
        pass

    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """
        Generate an embedding for the given text.
        """
        pass