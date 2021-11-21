from .icommunicator import ICommunicator
from models.user import User
from abc import abstractmethod


class IUserCommunicator(IDBCommunicator):
    @classmethod
    @abstractmethod
    def update(cls, user: User):
        raise NotImplementedError()
