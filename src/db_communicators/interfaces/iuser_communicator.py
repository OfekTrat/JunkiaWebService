from .idbcommunicator import IDBCommunicator
from ...user import User
from abc import abstractmethod


class IUserCommunicator(IDBCommunicator):
    @classmethod
    @abstractmethod
    def update(cls, user: User):
        raise NotImplementedError()
