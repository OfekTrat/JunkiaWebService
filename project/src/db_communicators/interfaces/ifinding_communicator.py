from abc import abstractmethod
from typing import List
from project.src.db_communicators.interfaces.idbcommunicator import IDBCommunicator
from project.src.db_communicators.interfaces.imultiple_delete_communicator import IMultipleDeleteCommunicator
from project.src.finding import Finding
from project.src.location import Location


class IFindingCommunicator(IDBCommunicator, IMultipleDeleteCommunicator):
    @classmethod
    @abstractmethod
    def get_by_radius(cls, radius: int, location: Location) -> List[Finding]:
        raise NotImplementedError()
