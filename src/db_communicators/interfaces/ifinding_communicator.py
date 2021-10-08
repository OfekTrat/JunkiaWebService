from abc import abstractmethod
from typing import List
from src.db_communicators.interfaces.idbcommunicator import IDBCommunicator
from ..interfaces.imultiple_delete_communicator import IMultipleDeleteCommunicator
from src.finding import Finding
from ...location import Location


class IFindingCommunicator(IDBCommunicator, IMultipleDeleteCommunicator):
    @classmethod
    @abstractmethod
    def get_by_radius(cls, radius: int, location: Location) -> List[Finding]:
        raise NotImplementedError()
