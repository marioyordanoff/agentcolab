

import openai
import aiohttp
from typing import List, Dict, Any
from .base_llm import BaseLLM
from agentcolab.config.settings import AgentConfig

class OpenAI(BaseLLM):
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", config: AgentConfig = AgentConfig(), server: str = "openai"):
        self.api_key = api_key
        self.model = model
        self.config = config
        self.server = server
        self.endpoint = self._get_endpoint()

    def _get_endpoint(self):
        if self.server == "openai":
            return "https://api.openai.com/v1/chat/completions"
        elif self.server == "azure":
            # You would need to set this up in your config
            return self.config.azure_endpoint
        else:
            raise ValueError(f"Unsupported server type: {self.server}")

    async def generate(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.endpoint, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['choices'][0]['message']['content']
                else:
                    raise Exception(f"Error in OpenAI LLM generation: {await response.text()}")

    async def embed(self, text: str) -> List[float]:
        payload = {
            "model": "text-embedding-ada-002",
            "input": text
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.openai.com/v1/embeddings", json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['data'][0]['embedding']
                else:
                    raise Exception(f"Error in OpenAI embedding generation: {await response.text()}")