from abc import abstractmethod
from typing import List, Protocol


class IMultipleDeleteCommunicator(Protocol):
    @classmethod
    @abstractmethod
    def delete_multiple(cls, ids: List[str]):
        raise NotImplementedError()
