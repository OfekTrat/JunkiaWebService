from abc import abstractmethod
from typing import Protocol, List
from src.finding import Finding
from src.location import Location
from src.user import User


class IDBCommunicator(Protocol):
    @abstractmethod
    def upload_finding(self, finding: Finding):
        raise NotImplementedError

    @abstractmethod
    def get_finding(self, finding_id: str) -> Finding:
        raise NotImplementedError

    @abstractmethod
    def delete_finding(self, finding_id: str):
        raise NotImplementedError

    @abstractmethod
    def get_finding_by_radius(self, location: Location, radius: int) -> List[Finding]:
        raise NotImplementedError

    @abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError
