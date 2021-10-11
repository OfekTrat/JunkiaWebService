import base64
import json
import unittest
from typing import Dict, Union, List
import os
from flask import Response

from main import create_app
from src.api import API
from src.db_communicators import MySQLExecutor, MySqlUserCommunicator, MySqlFindingCommunicator, ImageCommunicator

executor = MySQLExecutor("localhost", "root", "OfekT2021")
api = API(MySqlUserCommunicator(executor), MySqlFindingCommunicator(executor), ImageCommunicator())
app = create_app(api)


class TestImageAPI(unittest.TestCase):
    def __get_client(self):
        return app.test_client()

    @staticmethod
    def __load_response(resp: Response) -> Dict[str, Union[List, Dict, str]]:
        return json.loads(resp.data.decode())

    @staticmethod
    def __change_current_dir():
        if os.getcwd() != r"D:\git\JunkiaWebService":
            os.chdir(r"D:\git\JunkiaWebService")

    def test_get_image(self):
        self.__change_current_dir()
        client = self.__get_client()
        resp: Response = client.get(f"/image/test")
        json_data = self.__load_response(resp)

        assert resp.status_code == 200
        assert json_data["hash"] == "test"
        assert json_data["data"] == base64.b64encode(b"test_image_data").decode()

    def test_get_nonexistant_image(self):
        client = self.__get_client()
        resp: Response = client.get("/image/nonexistant_image")
        assert resp.status_code == 404


if __name__ == '__main__':
    unittest.main()
