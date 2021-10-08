import json
import unittest
from random import randint
from src.api import API
from main import create_app
from src.db_communicators.mysql_communicator.mysql_executor import MySQLExecutor
from src.db_communicators.mysql_communicator import MySqlFindingCommunicator
from src.db_communicators import ImageCommunicator
from src.user import User
from src.location import Location
from src.db_communicators.mysql_communicator import MySqlUserCommunicator


executor = MySQLExecutor("localhost", "root", "OfekT2021")
api = API(MySqlUserCommunicator(executor), MySqlFindingCommunicator(executor), ImageCommunicator())
user_comm = MySqlUserCommunicator(executor)
app = create_app(api)


class MyTestCase(unittest.TestCase):
    @staticmethod
    def __get_client():
        return app.test_client()

    def test_add_api_user(self):
        client = self.__get_client()
        user_as_json = {
            "id": "test_add_api_user",
            "tags": list("abc"),
            "longitude": 1,
            "latitude": 2,
            "radius": 1,
            "last_notified": "123456"
        }
        resp = client.post("/user", data=json.dumps(user_as_json), content_type="application/json")
        user = user_comm.get(user_as_json["id"])
        user_comm.delete(user.id)

        self.assertEqual(resp.status, "200 OK")
        self.assertEqual(user_as_json["id"], user.id)
        self.assertEqual(user_as_json["tags"], user.tags)
        self.assertEqual(user_as_json["longitude"], user.location.longitude)
        self.assertEqual(user_as_json["latitude"], user.location.latitude)
        self.assertEqual(user_as_json["radius"], user.radius)
        self.assertEqual(user_as_json["last_notified"], user.last_notified)

    def test_get_user(self):
        client = self.__get_client()
        resp = client.get("/user/test")
        user = User.create_from_json(resp.json["result"])

        self.assertEqual(user.id, "test")
        self.assertEqual(user.tags, ["a", "b", "v"])
        self.assertEqual(user.location, Location(1.2, -2))
        self.assertEqual(user.radius, 10)
        self.assertEqual(user.last_notified, "12345678")

    def test_get_non_existant_user(self):
        client = self.__get_client()
        resp = client.get("/user/non_existant")
        json_data = resp.json

        self.assertEqual(resp.status, "404 NOT FOUND")
        self.assertEqual(json_data["exit_code"], 1)

    def test_update_user(self):
        client = self.__get_client()
        user_as_json = {
            "id": "test_updating",
            "tags": list(str(randint(-1000, 1000))),
            "longitude": randint(-1800, 1800) / 10,
            "latitude": randint(-900, 900) / 10,
            "radius": randint(0, 100),
            "last_notified": "12345678"
        }
        prev_user = user_comm.get(user_as_json["id"])
        resp = client.put(f"/user/{user_as_json['id']}", data=json.dumps(user_as_json), content_type="application/json")
        now_user = user_comm.get(user_as_json["id"])

        self.assertEqual(resp.status, "200 OK")
        self.assertEqual(prev_user.id, now_user.id)
        self.assertNotEqual(prev_user.tags, now_user.tags)
        self.assertNotEqual(prev_user.location, now_user.location)
        self.assertNotEqual(prev_user.radius, now_user.radius)


if __name__ == '__main__':
    unittest.main()
