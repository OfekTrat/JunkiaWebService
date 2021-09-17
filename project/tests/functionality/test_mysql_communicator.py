import unittest
from random import randint
from datetime import datetime
import pymysql
from pymysql import Connection
from pymysql.cursors import Cursor
from project.src.finding import Finding
from project.src.location import Location
from project.src.user import User
from project.src.db_communicator.mysql_communicator.mysql_communicator import MySQLCommunicator
from project.src.db_communicator.communicator_exceptions import FindingNotFoundError, UserAlreadyExistError,\
    UserNotFoundError


class TestMySQLCommunicator(unittest.TestCase):
    @staticmethod
    def __get_connection() -> Connection:
        conn = pymysql.connect(
            host=MySQLCommunicator.MYSQL_HOST,
            user=MySQLCommunicator.MYSQL_USER,
            password=MySQLCommunicator.MYSQL_PASSWORD
        )
        return conn

    @staticmethod
    def __get_cursor(conn: Connection) -> Cursor:
        return conn.cursor(cursor=pymysql.cursors.DictCursor)

    def test_finding_upload(self):
        location = Location(1, 1)
        finding = Finding(location=location, tags=["tag1", "tag2"], image_hash="asdfgh", finding_id="test1")
        MySQLCommunicator.upload_finding(finding)

        conn = self.__get_connection()
        cursor = self.__get_cursor(conn)
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
        location = Location(1.00001, 1.00001)
        distance = 100
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

    def test_adding_user(self):
        user = User("test_adding", list("123"), Location(1, 1), 3, str(int(datetime.now().timestamp())))
        MySQLCommunicator.add_user(user)

        query = f"SELECT * FROM `junkia`.`users` WHERE id = '{user.id}'"
        conn = self.__get_connection()
        cursor = self.__get_cursor(conn)
        cursor.execute(query)
        results = cursor.fetchone()

        cursor.execute(f"DELETE FROM `junkia`.`users` WHERE id = '{user.id}'")
        conn.commit()
        cursor.close()
        conn.close()

        self.assertEqual(results["id"], user.id)
        self.assertEqual(results["tags"].split(","), user.tags)
        self.assertEqual(results["longitude"], user.location.longitude)
        self.assertEqual(results["latitude"], user.location.latitude)
        self.assertEqual(results["last_notified"], user.last_notified)
        self.assertEqual(results["radius"], user.radius)

    def test_adding_existing_user(self):
        user = User("test", list("123"), Location(1, 1), 3, str(int(datetime.now().timestamp())))

        with self.assertRaises(UserAlreadyExistError):
            MySQLCommunicator.add_user(user)

    def test_getting_user(self):
        # user = User("test", tags=list("abv"), location=Location(1.2, -2), radius=10, last_notified="12345678")
        # MySQLCommunicator.add_user(user)
        user_id = "test"
        user = MySQLCommunicator.get_user(user_id)

        self.assertEqual(user.id, user_id)
        self.assertEqual(user.location.latitude, -2)
        self.assertEqual(user.location.longitude, 1.2)
        self.assertEqual(user.tags, list("abv"))
        self.assertEqual(user.radius, 10)
        self.assertEqual(user.last_notified, "12345678")

    def test_getting_unexistant_user(self):
        user_id = "test_non_existant"

        with self.assertRaises(UserNotFoundError):
            MySQLCommunicator.get_user(user_id)

    def test_updating_user(self):
        user = User("test_updating", list(str(randint(-1000, 1000))),
                    Location(randint(-100, 100) / 2, randint(-100, 100) / 2), randint(-10, 10),
                    str(int(datetime.now().timestamp())))
        # MySQLCommunicator.add_user(user)
        MySQLCommunicator.update_user(user)
        updated_user = MySQLCommunicator.get_user(user.id)

        self.assertEqual(updated_user.id, user.id)
        self.assertEqual(updated_user.tags, user.tags)
        self.assertEqual(updated_user.location, user.location)
        self.assertEqual(updated_user.radius, user.radius)


if __name__ == '__main__':
    unittest.main()
