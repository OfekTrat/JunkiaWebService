from abc import abstractmethod
from models.imodel import IModel
from typing import Protocol, Union


class ICommunicator(Protocol):
    @classmethod
    @abstractmethod
    def get(cls, object_id: str) -> Union[IModel]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def upload(cls, new_object: Union[IModel]):
        raise NotImplementedError

    @classmethod
    def delete(cls, object_id: str):
        raise NotImplementedError
