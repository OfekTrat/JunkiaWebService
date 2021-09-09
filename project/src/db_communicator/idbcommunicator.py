from abc import abstractmethod
from typing import Protocol, List
from project.src.finding import Finding
from project.src.location import Location
from project.src.user import User


class IDBCommunicator(Protocol):
    @classmethod
    @abstractmethod
    def upload_finding(cls, finding: Finding):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_finding(cls, finding_id: str) -> Finding:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def delete_finding(cls, finding_id: str):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_finding_by_radius(cls, location: Location, radius: int) -> List[Finding]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def add_user(cls, user: User):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def update_user(cls, user_to_update: User):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_user(cls, user_id: str) -> User:
        pass
