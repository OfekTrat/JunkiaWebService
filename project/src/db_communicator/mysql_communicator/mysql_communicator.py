from typing import List

from src.db_communicator.idbcommunicator import IDBCommunicator
from src.finding import Finding
from src.location import Location
from src.user import User


class MySQLCommunicator(IDBCommunicator):
    def upload_finding(self, finding: Finding):
        pass

    def get_finding(self, finding_id: str) -> Finding:
        pass

    def delete_finding(self, finding_id: str):
        pass

    def get_finding_by_radius(self, location: Location, radius: int) -> List[Finding]:
        pass

    def add_user(self, user: User):
        pass
