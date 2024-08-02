from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseMemory(ABC):
    @abstractmethod
    async def add(self, item: Dict[str, Any]) -> None:
        """
        Add an item to the memory.
        """
        pass

    @abstractmethod
    async def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for relevant items in the memory based on the query.
        """
        pass

    @abstractmethod
    async def clear(self) -> None:
        """
        Clear all items from the memory.
        """
        pass