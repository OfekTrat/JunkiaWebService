from src.finding import Finding
from ..mysql_communicator_abs import MySQLCommunicatorAbs
from ..mysql_executer.iexecuter import IExecuter
from ....location import Location
from .queries import Queries
from .exceptions import FindingNotFoundError
from typing import List
from src.db_communicators.interfaces.ifinding_communicator import IFindingCommunicator


class MySqlFindingCommunicator(MySQLCommunicatorAbs, IFindingCommunicator):
    def __init__(self, executor: IExecuter):
        self.__executor = executor

    def get(self, finding_id: str) -> Finding:
        get_query = Queries.GET.value.format(finding_id=finding_id)

        with self.__executor as (conn, cursor):
            cursor.execute(get_query)
            result = cursor.fetchall()

            if len(result) == 0:
                raise FindingNotFoundError()

            finding_as_json = result[0]
            finding_as_json["tags"] = self._str_to_tags(finding_as_json["tags"])

            return Finding.create_from_json(finding_as_json)

    def upload(self, finding: Finding):
        upload_query = Queries.UPLOAD.value.format(
            finding_id=finding.id,
            longitude=finding.location.longitude,
            latitude=finding.location.latitude,
            image_hash=finding.image_hash,
            tags=self._tags_to_str(finding.tags)
        )

        with self.__executor as (conn, cursor):
            cursor.execute(upload_query)
            conn.commit()

    def delete(self, finding_id: str):
        delete_query = Queries.DELETE.value.format(ids=f"'{finding_id}'")

        with self.__executor as (conn, cursor):
            cursor.execute(delete_query)
            conn.commit()

    def delete_multiple(self, finding_ids: List[str]):
        ids = ", ".join([f"'{finding_id}'" for finding_id in finding_ids])
        delete_query = Queries.DELETE.value.format(ids=ids)

        with self.__executor as (conn, cursor):
            cursor.execute(delete_query)
            conn.commit()

    def get_by_radius(self, radius: int, location: Location) -> List[Finding]:
        query = Queries.FIND_BY_RADIUS.value.format(radius=radius, longitude=location.longitude,
                                                    latitude=location.latitude)

        with self.__executor as (conn, cursor):
            cursor.execute(query)
            results = cursor.fetchall()
            return [Finding.create_from_json(res) for res in results]
