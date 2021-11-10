from flask import Flask
import base64
import json
import unittest
from typing import Dict, Union, List
import os
from flask import Response
from app_initializer import AppInitializer
from communicators.interfaces import IImageCommunicator
from models.image import Image
from services.image_service import ImageService
from communicators.image_communicators import SimpleImageCommunicator


class TestImageAPI(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestImageAPI, self).__init__(*args, **kwargs)
        self.__image_comm = SimpleImageCommunicator()
        self.__app = self.__create_app(self.__image_comm)
        self.__client = self.__app.test_client()

    @staticmethod
    def __create_app(image_comm: IImageCommunicator) -> Flask:
        service = ImageService(image_comm)
        app_init = AppInitializer()
        app_init.add_image_service(service)
        return app_init.get_app()

    @staticmethod
    def __load_response(resp: Response) -> Dict[str, Union[List, Dict, str]]:
        return json.loads(resp.data.decode())

    def test_get_image(self):
        resp: Response = self.__client.get(f"/image/test")
        json_data = self.__load_response(resp)["result"]

        assert resp.status_code == 200
        assert json_data["hash"] == "test"
        assert json_data["data"] == base64.b64encode(b"test_image_data").decode()

    def test_get_nonexistant_image(self):
        resp: Response = self.__client.get("/image/nonexistant_image")
        assert resp.status_code == 404

    def test_upload_image(self):
        image = Image("test_upload", b"testing_upload")
        image_json = image.to_json()
        resp = self.__client.post("/image", data=json.dumps(image_json), content_type="application/json")
        resp_json = self.__load_response(resp)

        uploaded_image = self.__image_comm.get("test_upload")
        self.__image_comm.delete("test_upload")

        assert resp.status_code == 200
        assert resp_json["msg"] == "Successful Image Upload"
        assert uploaded_image.data == b"testing_upload"
        assert uploaded_image.hash == "test_upload"

    def test_upload_already_existed_image(self):
        image = Image("test", b"123456")
        resp = self.__client.post("/image", data=json.dumps(image.to_json()), content_type="application/json")
        resp_json = self.__load_response(resp)

        assert resp.status_code == 302
        assert resp_json["error"] == "Image Already Exists"

    def test_delete(self):
        image = Image("test_delete", b"test_deleting")
        self.__image_comm.upload(image)
        images_to_delete = {"hashes": [image.hash]}
        resp = self.__client.delete("/image", data=json.dumps(images_to_delete), content_type="application/json")
        resp_json = self.__load_response(resp)
        resp_get = self.__client.get(f"/image/{image.hash}")

        assert resp.status_code == 200
        assert resp_json["msg"] == "Successful Delete"
        assert resp_get.status_code == 404

    def test_multiple(self):
        image1 = Image("test_delete_multiple1", b"test1")
        image2 = Image("test_delete_multiple2", b"test2")
        self.__image_comm.upload(image1)
        self.__image_comm.upload(image2)

        images_to_delete = {"hashes": [image1.hash, image2.hash]}
        resp = self.__client.delete("/image", data=json.dumps(images_to_delete), content_type="application/json")
        resp_json = self.__load_response(resp)

        resp_get1 = self.__client.get(f"/image/{image1.hash}")
        resp_get2 = self.__client.get(f"/image/{image2.hash}")

        assert resp.status_code == 200
        assert resp_json["msg"] == "Successful Delete"
        assert resp_get1.status_code == 404
        assert resp_get2.status_code == 404


if __name__ == '__main__':
    unittest.main()
