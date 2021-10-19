import base64
import json
import unittest
from typing import Dict, Union, List
import os
from flask import Response

from main import create_app
from src.api import API
from src.db_communicators import MySQLExecutor, MySqlUserCommunicator, MySqlFindingCommunicator, ImageCommunicator
from src.image import Image
from src.db_communicators.image_communicator.exceptions import ImageNotFoundError, ImageAlreadyExistsError

executor = MySQLExecutor("localhost", "root", "OfekT2021")
image_communicator = ImageCommunicator()
api = API(MySqlUserCommunicator(executor), MySqlFindingCommunicator(executor), image_communicator)
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
        json_data = self.__load_response(resp)["result"]

        assert resp.status_code == 200
        assert json_data["hash"] == "test"
        assert json_data["data"] == base64.b64encode(b"test_image_data").decode()

    def test_get_nonexistant_image(self):
        client = self.__get_client()
        resp: Response = client.get("/image/nonexistant_image")
        assert resp.status_code == 404

    def test_upload_image(self):
        self.__change_current_dir()
        client = self.__get_client()
        image = Image("test_upload", b"testing_upload")
        image_json = image.to_json()
        resp = client.post("/image", data=json.dumps(image_json), content_type="application/json")
        resp_json = self.__load_response(resp)

        uploaded_image = image_communicator.get("test_upload")
        image_communicator.delete("test_upload")

        assert resp.status_code == 200
        assert resp_json["msg"] == "Successful Image Upload"
        assert uploaded_image.data == b"testing_upload"
        assert uploaded_image.hash == "test_upload"

    def test_upload_already_existed_image(self):
        self.__change_current_dir()
        client = self.__get_client()
        image = Image("test", b"123456")
        resp = client.post("/image", data=json.dumps(image.to_json()), content_type="application/json")
        resp_json = self.__load_response(resp)

        assert resp.status_code == 302
        assert resp_json["error"] == "Image Already Exists"

    def test_delete(self):
        self.__change_current_dir()
        client = self.__get_client()
        image = Image("test_delete", b"test_deleting")
        image_communicator.upload(image)
        images_to_delete = {"hashes": [image.hash]}
        resp = client.delete("/image", data=json.dumps(images_to_delete), content_type="application/json")
        resp_json = self.__load_response(resp)
        resp_get = client.get(f"/image/{image.hash}")

        assert resp.status_code == 200
        assert resp_json["msg"] == "Successful Delete"
        assert resp_get.status_code == 404

    def test_multiple(self):
        self.__change_current_dir()
        client = self.__get_client()
        image1 = Image("test_delete_multiple1", b"test1")
        image2 = Image("test_delete_multiple2", b"test2")
        image_communicator.upload(image1)
        image_communicator.upload(image2)

        images_to_delete = {"hashes": [image1.hash, image2.hash]}
        resp = client.delete("/image", data=json.dumps(images_to_delete), content_type="application/json")
        resp_json = self.__load_response(resp)

        resp_get1 = client.get(f"/image/{image1.hash}")
        resp_get2 = client.get(f"/image/{image2.hash}")

        assert resp.status_code == 200
        assert resp_json["msg"] == "Successful Delete"
        assert resp_get1.status_code == 404
        assert resp_get2.status_code == 404









if __name__ == '__main__':
    unittest.main()
