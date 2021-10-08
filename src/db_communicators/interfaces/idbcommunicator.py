from abc import abstractmethod
from src.user import User
from typing import Protocol, Union
from src.image import Image
from src.finding import Finding


class IDBCommunicator(Protocol):
    @classmethod
    @abstractmethod
    def get(cls, object_id: str) -> Union[User, Finding, Image]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def upload(cls, new_object: Union[User, Finding, Image]):
        raise NotImplementedError

    @classmethod
    def delete(cls, object_id: str):
        raise NotImplementedError
