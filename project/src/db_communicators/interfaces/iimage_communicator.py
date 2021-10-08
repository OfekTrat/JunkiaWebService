from typing import List, Union
from abc import abstractmethod
from project.src.db_communicators.interfaces.idbcommunicator import IDBCommunicator
from project.src.db_communicators.interfaces.imultiple_delete_communicator import IMultipleDeleteCommunicator
from project.src.finding import Finding
from project.src.image import Image
from project.src.user import User


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
