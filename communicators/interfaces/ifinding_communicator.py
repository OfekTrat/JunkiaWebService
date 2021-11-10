from abc import abstractmethod
from typing import List
from communicators.interfaces import IDBCommunicator
from ..interfaces.imultiple_delete_communicator import IMultipleDeleteCommunicator
from models.finding import Finding
from models.location import Location


class IFindingCommunicator(IDBCommunicator, IMultipleDeleteCommunicator):
    @classmethod
    @abstractmethod
    def get_by_radius(cls, radius: int, location: Location) -> List[Finding]:
        raise NotImplementedError()
