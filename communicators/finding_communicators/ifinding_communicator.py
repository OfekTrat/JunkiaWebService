from abc import abstractmethod
from typing import List
from communicators.icommunicator import ICommunicator
from ..interfaces.imultiple_delete_communicator import IMultipleDeleteCommunicator
from models.finding import Finding
from models.location import Location


class IFindingCommunicator(ICommunicator, IMultipleDeleteCommunicator):
    @classmethod
    @abstractmethod
    def get_by_radius(cls, radius: int, location: Location) -> List[Finding]:
        raise NotImplementedError()
