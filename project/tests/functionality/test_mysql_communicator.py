import unittest
import mysql.connector as connector
from src.finding import Finding
from src.location import Location
from src.db_communicator.mysql_communicator.mysql_communicator import MySQLCommunicator
from src.db_communicator.communicator_exceptions import FindingNotFoundError


class TestMySQLCommunicator(unittest.TestCase):
    @staticmethod
    def __get_connection():
        conn = connector.connect(
            host=MySQLCommunicator.MYSQL_HOST,
            user=MySQLCommunicator.MYSQL_USER,
            password=MySQLCommunicator.MYSQL_PASSWORD
        )
        return conn

    @staticmethod
    def __get_cursor(conn):
        return conn.cursor(dictionary=True)

    def test_finding_upload(self):
        location = Location(1, 1)
        finding = Finding(location=location, tags=["tag1", "tag2"], image_hash="asdfgh", finding_id="test1")
        MySQLCommunicator.upload_finding(finding)

        conn = self.__get_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT * from junkia.findings WHERE id = '{finding.id}'"
        cursor.execute(query)
        results = cursor.fetchall()[0]

        delete_query = f"DELETE from junkia.findings WHERE id = '{finding.id}'"
        cursor.execute(delete_query)
        conn.commit()

        cursor.close()
        conn.close()

        self.assertEqual(results["id"], finding.id)
        self.assertEqual(results["longitude"], finding.location.longitude)
        self.assertEqual(results["latitude"], finding.location.latitude)
        self.assertEqual(results["image_hash"], finding.image_hash)
        self.assertEqual(results["tags"].split(","), finding.tags)

    def test_get_finding(self):
        location = Location(1, 1)

        finding = Finding(location=location, tags=["tag1", "tag2"], image_hash="asdfgh", finding_id="test")
        # MySQLCommunicator.upload_finding(finding)
        gotten_finding = MySQLCommunicator.get_finding(finding.id)

        self.assertEqual(gotten_finding.id, finding.id)
        self.assertEqual(gotten_finding.location, finding.location)
        self.assertEqual(gotten_finding.tags, finding.tags)
        self.assertEqual(gotten_finding.image_hash, finding.image_hash)

    def test_not_found_finding(self):
        finding_id = "test2"

        with self.assertRaises(FindingNotFoundError):
            MySQLCommunicator.get_finding(finding_id)

    def test_delete_finding(self):
        finding = Finding(location=Location(1, 1), tags=list("1234"), finding_id="delete_test")
        MySQLCommunicator.upload_finding(finding)
        MySQLCommunicator.delete_finding(finding.id)

        with self.assertRaises(FindingNotFoundError):
            MySQLCommunicator.get_finding(finding.id)

    def test_successful_radius_finding(self):
        location = Location(2, 2)
        distance = 2
        close_findings = MySQLCommunicator.get_finding_by_radius(location, distance)
        test_finding = [finding for finding in close_findings if finding.id == "test"]

        self.assertEqual(len(test_finding), 1)
        test_finding = test_finding[0]

        self.assertEqual(test_finding.id, "test")
        self.assertEqual(test_finding.location, Location(1, 1))
        self.assertEqual(test_finding.tags, ["tag1", "tag2"])
        self.assertEqual(test_finding.image_hash, "asdfgh")

    def test_successful_not_finding(self):
        location = Location(2, 2)
        distance = 0.1
        close_findings = MySQLCommunicator.get_finding_by_radius(location, distance)
        test_finding = [finding for finding in close_findings if finding.id == "test"]

        self.assertEqual(len(test_finding), 0)


if __name__ == '__main__':
    unittest.main()
