# agentcolab/config/settings.py

import yaml
import os
from pydantic import BaseModel, Field

def load_config(file_path: str):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        for key, value in config.items():
            os.environ[key] = str(value)

class AgentConfig(BaseModel):
    max_conversation_history: int = Field(default=100, description="Maximum number of messages to keep in conversation history")
    temperature: float = Field(default=0.7, description="Temperature for LLM responses")
    max_tokens: int = Field(default=150, description="Maximum number of tokens for LLM responses")
    tools_enabled: bool = Field(default=True, description="Whether to enable tool usage")
    reflection_enabled: bool = Field(default=True, description="Whether to enable agent self-reflection")
    memory_enabled: bool = Field(default=True, description="Whether to enable memory usage")
    serper_api_key: str = Field(default="", description="API key for Serper (Google Search API)")
    openai_api_key: str = Field(default="", description="API key for OpenAI")
    azure_endpoint: str = Field(default="", description="Endpoint for Azure OpenAI service")

    @classmethod
    def from_env(cls):
        return cls(
            serper_api_key=os.getenv("SERPER_API_KEY", ""),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            azure_endpoint=os.getenv("AZURE_ENDPOINT", ""),
            # Add other fields as needed
        )