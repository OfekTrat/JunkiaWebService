from communicators.icommunicator import ICommunicator
from models.user import User
from abc import abstractmethod


class IUserCommunicator(ICommunicator):
    @classmethod
    @abstractmethod
    def update(cls, user: User):
        raise NotImplementedError()
