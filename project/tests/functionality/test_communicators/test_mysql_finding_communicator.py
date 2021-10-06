import unittest
from project.src.finding import Finding
from project.src.db_communicators.mysql_communicator.mysql_finding_communicator import MySqlFindingCommunicator
from project.src.db_communicators.mysql_communicator.mysql_executer import MySQLExecuter
from project.src.location import Location
from project.src.db_communicators.mysql_communicator.mysql_finding_communicator.exceptions import FindingNotFoundError


class TestFindingCommunicator(unittest.TestCase):
    HOST = "localhost"
    USER = "root"
    PASS = "OfekT2021"

    def test_get(self):
        finding_id = "test"
        finding = MySqlFindingCommunicator.get(finding_id)

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
        MySqlFindingCommunicator.upload(finding)

        executer = MySQLExecuter(self.HOST, self.USER, self.PASS)
        result = executer.execute(get_query)
        executer.commit(delete_query)
        executer.close()

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

    def test_delete_single_finding(self):
        get_query = "SELECT * FROM junkia.findings WHERE id = 'test_delete'"
        finding = Finding(
            finding_id="test_delete",
            location=Location(1, 1),
            tags=list("abc"),
            image_hash="asdf",
        )
        MySqlFindingCommunicator.upload(finding)
        MySqlFindingCommunicator.delete(finding.id)

        executer = MySQLExecuter(self.HOST, self.USER, self.PASS)
        results = executer.execute(get_query)
        executer.close()

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
        MySqlFindingCommunicator.upload(finding1)
        MySqlFindingCommunicator.upload(finding2)
        MySqlFindingCommunicator.delete_multiple([finding1.id, finding2.id])

        executer = MySQLExecuter(self.HOST, self.USER, self.PASS)
        results = executer.execute(get_query)
        executer.close()

        assert len(results) == 0
    
    def test_get_finding_by_close_radius(self):
        radius = 10
        location = Location(1.000001, 0.99999)
        results = MySqlFindingCommunicator.get_by_radius(radius, location)

        assert type(results) == list
        assert len(results) == 1
        assert results[0].id == "test"

    def test_get_finding_by_far_radius(self):
        radius = 10
        location = Location(-90.2, 89.993)
        results = MySqlFindingCommunicator.get_by_radius(radius, location)

        assert type(results) == list
        assert len(results) == 0

    def test_get_nonexistant_finding(self):
        with self.assertRaises(FindingNotFoundError):
            MySqlFindingCommunicator.get("4567ujkp")

if __name__ == '__main__':
    unittest.main()
