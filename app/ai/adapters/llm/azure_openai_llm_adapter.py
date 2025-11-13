from typing import Any
from httpx import AsyncClient, Client
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import AIMessage
from langchain_core.language_models.base import LanguageModelInput
from langchain_core.runnables import RunnableConfig
from .base_llm_adapter import BaseLLMAdapter


class AzureOpenAILLMAdapter(BaseLLMAdapter):

    def __init__(
        self, 
        model: str,
        endpoint: str,
        api_version: str,
        api_key: str,
        temperature: float,
        top_p: float,
        http_async_client: AsyncClient, 
        http_client: Client,
        verbose: bool = True
    ):
        self.llm = AzureChatOpenAI(
            model=model,
            azure_endpoint=endpoint,
            api_version=api_version,
            api_key=api_key,
            temperature=temperature,
            top_p=top_p,
            http_async_client=http_async_client,
            http_client=http_client,
            verbose=verbose,
        )
    
    async def ainvoke(
        self, 
        input: LanguageModelInput,
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> AIMessage:
        return self.llm.ainvoke(input=input, config=config, **kwargs)