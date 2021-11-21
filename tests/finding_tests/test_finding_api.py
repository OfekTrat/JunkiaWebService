import os
import json
import unittest
from flask import Response, Flask
from models.finding import Finding
from typing import List, Dict, Union
from models.location import Location
from services.finding_service import FindingService
from services.exceptions.finding_exceptions import FindingNotFoundError
from utils.mysql.mysql_executor import MySQLExecutor
from initializers.finding_initializer import FindingAppInitializer
from communicators.finding_communicators import MySqlFindingCommunicator
from communicators.finding_communicators.ifinding_communicator import IFindingCommunicator


class TestFindingService(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestFindingService, self).__init__(*args, **kwargs)
        self.__finding_comm = self.__get_finding_communicator()
        self.__app = self.__get_app(self.__finding_comm)
        self.__client = self.__app.test_client()

    @staticmethod
    def __get_finding_communicator():
        server, user, password = os.environ["MYSQL_SERVER"], os.environ["MYSQL_USER"], os.environ["MYSQL_PASSWORD"]
        executor = MySQLExecutor(host=server, user=user, password=password)
        return MySqlFindingCommunicator(executor)

    @staticmethod
    def __get_app(finding_communicator: IFindingCommunicator) -> Flask:
        service = FindingService(finding_communicator)
        return FindingAppInitializer.get_app(service)

    @staticmethod
    def __load_response(resp: Response) -> Dict[str, Union[List, Dict, str]]:
        return json.loads(resp.data.decode())

    def test_getting_finding(self):
        finding_id = "test"

        resp = self.__client.get(f"/finding/{finding_id}")
        finding_as_json = self.__load_response(resp)
        assert "result" in finding_as_json.keys()
        finding = Finding.create_from_json(finding_as_json["result"])

        self.assertEqual(finding.id, "test")
        self.assertEqual(finding.tags, ["tag1", "tag2"])
        self.assertEqual(finding.location, Location(1, 1))
        self.assertEqual(finding.image_hash, "asdfgh")

    def test_delete_finding(self):
        finding = Finding(Location(1, 1), tags=list("abc"), finding_id="test_api_delete")
        self.__finding_comm.upload(finding)
        resp = self.__client.delete(f"/finding/{finding.id}")

        self.assertEqual(resp.status, "200 OK")

        with self.assertRaises(FindingNotFoundError):
            self.__finding_comm.get(finding.id)

    def test_upload_finding(self):
        finding = Finding(Location(1, 1), tags=list("abc"), finding_id="test_api_upload")
        resp = self.__client.post("/finding", data=json.dumps(finding.to_dict()), content_type="application/json")

        gotten_finding = self.__finding_comm.get(finding.id)
        self.__finding_comm.delete(finding.id)

        self.assertEqual(resp.status, "200 OK")
        self.assertEqual(gotten_finding.id, finding.id)
        self.assertEqual(gotten_finding.location, finding.location)
        self.assertEqual(gotten_finding.tags, finding.tags)
        self.assertEqual(gotten_finding.image_hash, str(finding.image_hash))

    def test_get_nonexistant_finding(self):
        finding_id = "test_nonexistant"

        resp = self.__client.get(f"/finding/{finding_id}")
        data = resp.json
        self.assertEqual(resp.status, "404 NOT FOUND")
        self.assertEqual(data["exit_code"], 1)

    def test_find_by_radius(self):
        location = Location(1, 2)
        radius = 1000
        payload = {"radius": radius, "longitude": location.longitude, "latitude": location.latitude}

        resp = self.__client.post("/finding/by_radius", data=json.dumps(payload), content_type="application/json")
        json_data = resp.json
        finding = Finding.create_from_json(json_data["result"][0])

        self.assertEqual(resp.status, "200 OK")
        self.assertEqual(type(json_data["result"]), list)
        self.assertEqual(finding.id, "test")
        self.assertEqual(finding.location, Location(1, 1))
        self.assertEqual(finding.image_hash, "asdfgh")

    def test_radius_empty_search(self):
        location = Location(20, 2)
        radius = 1
        payload = {"radius": radius, "longitude": location.longitude, "latitude": location.latitude}

        resp = self.__client.post("/finding/by_radius", data=json.dumps(payload), content_type="application/json")
        json_data = resp.json
        self.assertEqual(type(json_data["result"]), list)
        self.assertEqual(len(json_data["result"]), 0)


if __name__ == '__main__':
    unittest.main()
