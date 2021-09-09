import json
from typing import List, Dict, Union
from project.app import app
from project.src.db_communicator.communicator_exceptions import FindingNotFoundError
from project.src.finding import Finding
from project.src.location import Location
import unittest
from flask import Response
from project.src.db_communicator.mysql_communicator import MySQLCommunicator


class MyTestCase(unittest.TestCase):
    @staticmethod
    def __get_client():
        return app.test_client()

    @staticmethod
    def __load_response(resp: Response) -> Union[Dict, List]:
        return json.loads(resp.data.decode())

    def test_getting_finding(self):
        finding_id = "test"
        client = self.__get_client()

        resp = client.get(f"/finding/{finding_id}")
        finding_as_json = self.__load_response(resp)
        finding = Finding.create_from_json(finding_as_json)

        self.assertEqual(finding.id, "test")
        self.assertEqual(finding.tags, ["tag1", "tag2"])
        self.assertEqual(finding.location, Location(1, 1))
        self.assertEqual(finding.image_hash, "asdfgh")

    def test_delete_finding(self):
        client = self.__get_client()
        finding = Finding(Location(1, 1), tags=list("abc"), finding_id="test_api_delete")
        MySQLCommunicator.upload_finding(finding)
        resp = client.delete(f"/finding/{finding.id}")

        self.assertEqual(resp.status, "200 OK")

        with self.assertRaises(FindingNotFoundError):
            MySQLCommunicator.get_finding(finding.id)

    def test_upload_finding(self):
        client = self.__get_client()
        finding = Finding(Location(1, 1), tags=list("abc"), finding_id="test_api_upload")
        resp = client.post("/finding", data=json.dumps(finding.to_dict()), content_type="application/json")

        gotten_finding = MySQLCommunicator.get_finding(finding.id)
        MySQLCommunicator.delete_finding(finding.id)

        self.assertEqual(resp.status, "200 OK")
        self.assertEqual(gotten_finding.id, finding.id)
        self.assertEqual(gotten_finding.location, finding.location)
        self.assertEqual(gotten_finding.tags, finding.tags)
        self.assertEqual(gotten_finding.image_hash, str(finding.image_hash))

    def test_get_nonexistant_finding(self):
        client = self.__get_client()
        finding_id = "test_nonexistant"

        resp = client.get(f"/finding/{finding_id}")
        data = resp.json
        self.assertEqual(resp.status, "404 NOT FOUND")
        self.assertEqual(list(data.keys()), ["error"])
        self.assertEqual(data["error"], f"finding id {finding_id} not found")

    def test_find_by_radius(self):
        client = self.__get_client()
        location = Location(1,2)
        radius = 1
        payload = {"radius": radius, "longitude": location.longitude, "latitude": location.latitude}

        resp = client.post("/finding/by_radius", data=json.dumps(payload), content_type="application/json")
        json_data = resp.json
        finding = Finding.create_from_json(json_data[0])

        self.assertEqual(resp.status, "200 OK")
        self.assertEqual(type(json_data), list)
        self.assertEqual(finding.id, "test")
        self.assertEqual(finding.location, Location(1, 1))
        self.assertEqual(finding.image_hash, "asdfgh")

    def test_radius_empty_search(self):
        client = self.__get_client()
        location = Location(20, 2)
        radius = 1
        payload = {"radius": radius, "longitude": location.longitude, "latitude": location.latitude}

        resp = client.post("/finding/by_radius", data=json.dumps(payload), content_type="application/json")
        json_data = resp.json
        self.assertEqual(type(json_data), list)
        self.assertEqual(len(json_data), 0)




if __name__ == '__main__':
    unittest.main()
