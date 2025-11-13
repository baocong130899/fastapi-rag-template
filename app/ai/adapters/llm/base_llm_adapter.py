from abc import ABC, abstractmethod
from typing import Any
from langchain_core.messages import AIMessage
from langchain_core.language_models.base import LanguageModelInput
from langchain_core.runnables import RunnableConfig


class BaseLLMAdapter(ABC):

    @abstractmethod
    async def ainvoke(
        self, 
        input: LanguageModelInput,
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> AIMessage:
        """"""