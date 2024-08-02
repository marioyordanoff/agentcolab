# agentcolab/agents/base_agent.py

import asyncio
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

from agentcolab.models.llm_providers import BaseLLM
from agentcolab.tools.base_tool import BaseTool
from agentcolab.memory.memory_providers import BaseMemory
from agentcolab.config.settings import AgentConfig

class BaseAgent(ABC):
    def __init__(
        self,
        name: str,
        llm: BaseLLM,
        memory: BaseMemory,
        tools: List[BaseTool],
        config: AgentConfig
    ):
        self.name = name
        self.llm = llm
        self.memory = memory
        self.tools = {tool.name: tool for tool in tools}
        self.config = config
        self.conversation_history: List[Dict[str, Any]] = []

    @abstractmethod
    async def process_message(self, message: str) -> str:
        pass

    async def execute_tool(self, tool_name: str, **tool_args: Any) -> Any:
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        tool = self.tools[tool_name]
        return await tool.execute_with_retry(tool.run, **tool_args)

    async def _call_llm(self, prompt: str) -> str:
        return await self.llm.generate(prompt)

    async def _update_memory(self, message: Dict[str, Any]):
        await self.memory.add(message)
        self.conversation_history.append(message)

    async def _get_relevant_memory(self, query: str) -> List[Dict[str, Any]]:
        return await self.memory.search(query)

    @abstractmethod
    async def _generate_prompt(self, message: str) -> str:
        pass

    async def run(self, message: str) -> str:
        try:
            response = await self.process_message(message)
            await self._update_memory({"role": "human", "content": message})
            await self._update_memory({"role": "ai", "content": response})
            return response
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            return "I'm sorry, but I encountered an error while processing your message."

    @abstractmethod
    async def reflect(self) -> None:
        pass

    async def generate_search_query(self, message: str) -> str:
        prompt = f"Based on the following message, generate a search query that would help find relevant information:\n\n{message}\n\nSearch Query:"
        return await self._call_llm(prompt)