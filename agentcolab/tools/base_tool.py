from abc import ABC, abstractmethod
from typing import Any, Dict
import asyncio

class BaseTool(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.max_retries = 3
        self.retry_delay = 1

    @abstractmethod
    async def run(self, **kwargs: Any) -> Any:
        """
        Execute the tool with the given arguments.
        """
        pass

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """
        Return the JSON schema for the tool's arguments.
        """
        pass

    async def execute_with_retry(self, func, *args, **kwargs):
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                print(f"Error in {self.name}: {str(e)}. Retrying... (Attempt {attempt + 1}/{self.max_retries})")
                await asyncio.sleep(self.retry_delay)