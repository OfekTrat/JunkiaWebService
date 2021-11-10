from typing import List, Union
from abc import abstractmethod
from ..interfaces import IDBCommunicator
from ..interfaces.imultiple_delete_communicator import IMultipleDeleteCommunicator
from models.finding import Finding
from models.image import Image
from models.user import User


class IImageCommunicator(IDBCommunicator, IMultipleDeleteCommunicator):
    @classmethod
    @abstractmethod
    def get(cls, object_id: str) -> Union[User, Finding, Image]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def upload(cls, new_object: Union[User, Finding, Image]):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def delete(cls, object_id: str):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def delete_multiple(cls, ids: List[str]):
        raise NotImplementedError()
