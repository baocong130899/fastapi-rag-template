from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseMessagingClient(ABC):

    @abstractmethod
    async def publish(self, payload: Dict[str, Any]) -> None:
        """Publish payload to some destination."""
