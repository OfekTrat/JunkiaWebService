from project.src.finding import Finding
from project.src.db_communicators.mysql_communicator.mysql_communicator_abs import MySQLCommunicatorAbs
from project.src.location import Location
from .queries import Queries
from project.src.db_communicators.mysql_communicator.mysql_executer import MySQLExecuter
from .exceptions import FindingNotFoundError
from multipledispatch import dispatch
from typing import Protocol, List


class MySqlFindingCommunicator(MySQLCommunicatorAbs):
    HOST = "localhost"
    USER = "root"
    PASS = "OfekT2021"

    @classmethod
    def get(cls, finding_id: str) -> Finding:
        get_query = Queries.GET.value.format(finding_id=finding_id)

        executer = MySQLExecuter(cls.HOST, cls.USER, cls.PASS)
        result = executer.execute(get_query)

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
        executer = MySQLExecuter(cls.HOST, cls.USER, cls.PASS)
        executer.commit(upload_query)
        executer.close()

    @classmethod
    def delete(cls, finding_id: str):
        delete_query = Queries.DELETE.value.format(ids=f"'{finding_id}'")

        executer = MySQLExecuter(cls.HOST, cls.USER, cls.PASS)
        executer.commit(delete_query)
        executer.close()

    @classmethod
    def delete_multiple(cls, finding_ids: List[str]):
        ids = ", ".join([f"'{finding_id}'" for finding_id in finding_ids])
        delete_query = Queries.DELETE.value.format(ids=ids)

        executer = MySQLExecuter(cls.HOST, cls.USER, cls.PASS)
        executer.commit(delete_query)
        executer.close()

    @classmethod
    def get_by_radius(cls, radius: int, location: Location) -> List[Finding]:
        query = Queries.FIND_BY_RADIUS.value.format(radius=radius, longitude=location.longitude,
                                                    latitude=location.latitude)

        executer = MySQLExecuter(cls.HOST, cls.USER, cls.PASS)
        results = executer.execute(query)
        executer.close()

        return [Finding.create_from_json(res) for res in results]
