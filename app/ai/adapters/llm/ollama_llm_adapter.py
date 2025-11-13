from typing import Any
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
from langchain_core.language_models.base import LanguageModelInput
from langchain_core.runnables import RunnableConfig
from .base_llm_adapter import BaseLLMAdapter


class OllamaLLMAdapter(BaseLLMAdapter):

    def __init__(
        self,
        model: str,
        endpoint: str,
        temperature: float,
        top_p: float,
        verbose: bool = True
    ):
        self.llm = ChatOllama(
            model=model,
            base_url=endpoint,
            temperature=temperature,
            top_p=top_p,
            verbose=verbose
        )
    
    async def ainvoke(
        self, 
        input: LanguageModelInput,
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> AIMessage:
        return self.llm.ainvoke(input=input, config=config, **kwargs)
