from typing import Union, List

from project.src.db_communicators.idbcommunicator import IDBCommunicator
from project.src.finding import Finding
from project.src.user import User
from abc import abstractmethod


class MySQLCommunicatorAbs(IDBCommunicator):
    @classmethod
    @abstractmethod
    def get(cls, object_id: str) -> Union[User, Finding, bytes]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def upload(cls, new_object: Union[User, Finding, bytes]):
        pass

    @classmethod
    @abstractmethod
    def delete(cls, object_id: str):
        pass

    @classmethod
    def _tags_to_str(cls, tags: List[str]) -> str:
        return ",".join(tags)

    @classmethod
    def _str_to_tags(cls, tags_as_str: str) -> List[str]:
        return tags_as_str.split(",")
