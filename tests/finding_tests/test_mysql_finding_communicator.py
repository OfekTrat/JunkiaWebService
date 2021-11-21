import os
import unittest
from models.finding import Finding
from utils.mysql.mysql_executor import MySQLExecutor
from models.location import Location
from communicators.finding_communicators import MySqlFindingCommunicator
from services.exceptions.finding_exceptions import FindingNotFoundError


class TestFindingCommunicator(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestFindingCommunicator, self).__init__(*args, **kwargs)
        host, user, password = os.environ["MYSQL_SERVER"], os.environ["MYSQL_USER"], os.environ["MYSQL_PASSWORD"]
        self.__executor = MySQLExecutor(host ,user, password)
        self.__finding_comm = MySqlFindingCommunicator(self.__executor)

    def test_get(self):
        finding_id = "test"
        finding = self.__finding_comm.get(finding_id)

        assert finding.id == finding_id
        assert finding.tags == ["tag1", "tag2"]
        assert finding.location.longitude == 1
        assert finding.location.latitude == 1
        assert finding.image_hash == "asdfgh"

    def test_upload(self):
        delete_query = "DELETE FROM junkia.findings WHERE id = 'test_upload'"
        get_query = "SELECT * FROM junkia.findings WHERE id = 'test_upload'"
        finding = Finding(
            finding_id="test_upload",
            location=Location(1,1),
            tags=list("abc"),
            image_hash="asdf",
        )
        self.__finding_comm.upload(finding)

        with self.__executor as (conn, cursor):
            cursor.execute(get_query)
            result = cursor.fetchall()

            assert type(result) == list
            assert len(result) == 1

            finding_as_json = result[0]
            finding_as_json["tags"] = finding_as_json["tags"].split(",")
            uploaded_finding = Finding.create_from_json(finding_as_json)

            assert uploaded_finding.id == finding.id
            assert uploaded_finding.location.longitude == finding.location.longitude
            assert uploaded_finding.location.latitude == finding.location.latitude
            assert uploaded_finding.image_hash == finding.image_hash
            assert uploaded_finding.tags == finding.tags

            cursor.execute(delete_query)
            conn.commit()

    def test_delete_single_finding(self):
        get_query = "SELECT * FROM junkia.findings WHERE id = 'test_delete'"
        finding = Finding(
            finding_id="test_delete",
            location=Location(1, 1),
            tags=list("abc"),
            image_hash="asdf",
        )
        self.__finding_comm.upload(finding)
        self.__finding_comm.delete(finding.id)

        with self.__executor as (conn, cursor):
            cursor.execute(get_query)
            results = cursor.fetchall()

            assert type(results) == tuple
            assert len(results) == 0

    def test_delete_multiple_finding(self):
        get_query = "SELECT * FROM junkia.findings WHERE id = 'test_delete1' OR id = 'test_delete2'"
        finding1 = Finding(
            finding_id="test_delete1",
            location=Location(1, 1),
            tags=list("abc"),
            image_hash="asdf",
        )
        finding2 = Finding(
            finding_id="test_delete2",
            location=Location(1, 1),
            tags=list("abc"),
            image_hash="asdf",
        )
        self.__finding_comm.upload(finding1)
        self.__finding_comm.upload(finding2)
        self.__finding_comm.delete_multiple([finding1.id, finding2.id])

        with self.__executor as (conn, cursor):
            cursor.execute(get_query)
            results = cursor.fetchall()

            assert type(results) == tuple
            assert len(results) == 0
    
    def test_get_finding_by_close_radius(self):
        radius = 10
        location = Location(1.000001, 0.99999)
        results = self.__finding_comm.get_by_radius(radius, location)

        assert type(results) == list
        assert len(results) == 1
        assert results[0].id == "test"

    def test_get_finding_by_far_radius(self):
        radius = 10
        location = Location(-90.2, 89.993)
        results = self.__finding_comm.get_by_radius(radius, location)

        assert type(results) == list
        assert len(results) == 0

    def test_get_nonexistant_finding(self):
        with self.assertRaises(FindingNotFoundError):
            self.__finding_comm.get("4567ujkp")


if __name__ == '__main__':
    unittest.main()
