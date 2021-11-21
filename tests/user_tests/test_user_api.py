import os
import json
import unittest
from flask import Flask
from random import randint
from initializers.user_initializer import UserAppInitializer
from communicators.user_communicators.iuser_communicator import IUserCommunicator
from utils.mysql.mysql_executor import MySQLExecutor
from models.user import User
from models.location import Location
from communicators.user_communicators import MySqlUserCommunicator
from services.exceptions.user_exceptions import UserNotFoundError
from services.user_service import UserService


class TestUserApi(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestUserApi, self).__init__(*args, **kwargs)
        self.__user_comm = self.__create_communicator()
        self.__app = self.__create_app(self.__user_comm)
        self.__client = self.__app.test_client()

    @staticmethod
    def __create_communicator():
        server, user, password = os.environ["MYSQL_SERVER"], os.environ["MYSQL_USER"], os.environ["MYSQL_PASSWORD"]
        executor = MySQLExecutor(host=server, user=user, password=password)
        return MySqlUserCommunicator(executor)

    @staticmethod
    def __create_app(user_communicator: IUserCommunicator) -> Flask:
        service = UserService(user_communicator)
        return UserAppInitializer.get_app(service)

    def test_add_api_user(self):
        user_as_json = {
            "id": "test_add_api_user",
            "tags": list("abc"),
            "longitude": 1,
            "latitude": 2,
            "radius": 1,
            "last_notified": "123456"
        }
        resp = self.__client.post("/user", data=json.dumps(user_as_json), content_type="application/json")
        user = self.__user_comm.get(user_as_json["id"])
        self.__user_comm.delete(user.id)

        self.assertEqual(resp.status, "200 OK")
        self.assertEqual(user_as_json["id"], user.id)
        self.assertEqual(user_as_json["tags"], user.tags)
        self.assertEqual(user_as_json["longitude"], user.location.longitude)
        self.assertEqual(user_as_json["latitude"], user.location.latitude)
        self.assertEqual(user_as_json["radius"], user.radius)
        self.assertEqual(user_as_json["last_notified"], user.last_notified)

    def test_get_user(self):
        resp = self.__client.get("/user/test")
        user = User.create_from_json(resp.json["result"])

        self.assertEqual(user.id, "test")
        self.assertEqual(user.tags, ["a", "b", "v"])
        self.assertEqual(user.location, Location(1.2, -2))
        self.assertEqual(user.radius, 10)
        self.assertEqual(user.last_notified, "12345678")

    def test_get_non_existant_user(self):
        resp = self.__client.get("/user/non_existant")
        json_data = resp.json

        self.assertEqual(resp.status, "404 NOT FOUND")
        self.assertEqual(json_data["exit_code"], 1)

    def test_update_user(self):
        user_as_json = {
            "id": "test_updating",
            "tags": list(str(randint(-1000, 1000))),
            "longitude": randint(-1800, 1800) / 10,
            "latitude": randint(-900, 900) / 10,
            "radius": randint(0, 100),
            "last_notified": "12345678"
        }
        prev_user = self.__user_comm.get(user_as_json["id"])
        resp = self.__client.put(f"/user/{user_as_json['id']}", data=json.dumps(user_as_json), content_type="application/json")
        now_user = self.__user_comm.get(user_as_json["id"])

        self.assertEqual(resp.status, "200 OK")
        self.assertEqual(prev_user.id, now_user.id)
        self.assertNotEqual(prev_user.tags, now_user.tags)
        self.assertNotEqual(prev_user.location, now_user.location)
        self.assertNotEqual(prev_user.radius, now_user.radius)

    def test_delete_user(self):
        user = User("test_delete_api", ["a", "b"], Location(1,1), 4, "1234")
        self.__user_comm.upload(user)

        self.__client.delete(f"/user/{user.id}")
        with self.assertRaises(UserNotFoundError):
            self.__user_comm.get(user.id)


if __name__ == '__main__':
    unittest.main()
