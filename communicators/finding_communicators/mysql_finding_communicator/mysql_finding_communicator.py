from models.finding import Finding
from utils.mysql.mysql_communicator_abs import MySQLCommunicatorAbs
from utils.mysql.mysql_executor import IExecutor
from models.location import Location
from .queries import Queries
from services.finding_service import FindingNotFoundError
from typing import List
from communicators.finding_communicators.ifinding_communicator import IFindingCommunicator


class MySqlFindingCommunicator(MySQLCommunicatorAbs, IFindingCommunicator):
    def __init__(self, executor: IExecutor):
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
        found_findings = list()

        with self.__executor as (conn, cursor):
            cursor.execute(query)
            results = cursor.fetchall()

            for res in results:
                res["tags"] = self._str_to_tags(res["tags"])
                found_findings.append(Finding.create_from_json(res))

        return found_findings
