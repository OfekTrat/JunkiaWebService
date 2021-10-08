from project.src.finding import Finding
from project.src.db_communicators.mysql_communicator.mysql_communicator_abs import MySQLCommunicatorAbs
from project.src.location import Location
from .queries import Queries
from project.src.db_communicators.mysql_communicator.mysql_executer import MySQLExecuter
from .exceptions import FindingNotFoundError
from typing import List
from project.constants import Constants


class MySqlFindingCommunicator(MySQLCommunicatorAbs):
    executer = MySQLExecuter(Constants.HOST, Constants.USER, Constants.PASS)

    @classmethod
    def get(cls, finding_id: str) -> Finding:
        get_query = Queries.GET.value.format(finding_id=finding_id)

        with cls.executer as (conn, cursor):
            cursor.execute(get_query)
            result = cursor.fetchall()

            if len(result) == 0:
                raise FindingNotFoundError()

            finding_as_json = result[0]
            finding_as_json["tags"] = cls._str_to_tags(finding_as_json["tags"])

            return Finding.create_from_json(finding_as_json)

    @classmethod
    def upload(cls, finding: Finding):
        upload_query = Queries.UPLOAD.value.format(
            finding_id=finding.id,
            longitude=finding.location.longitude,
            latitude=finding.location.latitude,
            image_hash=finding.image_hash,
            tags=cls._tags_to_str(finding.tags)
        )

        with cls.executer as (conn, cursor):
            cursor.execute(upload_query)
            conn.commit()

    @classmethod
    def delete(cls, finding_id: str):
        delete_query = Queries.DELETE.value.format(ids=f"'{finding_id}'")

        with cls.executer as (conn, cursor):
            cursor.execute(delete_query)
            conn.commit()

    @classmethod
    def delete_multiple(cls, finding_ids: List[str]):
        ids = ", ".join([f"'{finding_id}'" for finding_id in finding_ids])
        delete_query = Queries.DELETE.value.format(ids=ids)

        with cls.executer as (conn, cursor):
            cursor.execute(delete_query)
            conn.commit()

    @classmethod
    def get_by_radius(cls, radius: int, location: Location) -> List[Finding]:
        query = Queries.FIND_BY_RADIUS.value.format(radius=radius, longitude=location.longitude,
                                                    latitude=location.latitude)

        with cls.executer as (conn, cursor):
            cursor.execute(query)
            results = cursor.fetchall()
            return [Finding.create_from_json(res) for res in results]
