from src.finding import Finding, WrongFindingInputError
from src.location import Location
import unittest


class MyTestCase(unittest.TestCase):
    GOOD_LONGITUDE = 100.0
    GOOD_LATITUDE = 60.0
    GOOD_LOCATION = Location(GOOD_LONGITUDE, GOOD_LATITUDE)
    GOOD_TAGS = ["Tag1", "Tag2"]
    BAD_TAGS = []
    IMAGE_HASH = "abcdef"

    def test_finding_creation(self):
        finding = Finding(self.GOOD_LOCATION, self.GOOD_TAGS, self.IMAGE_HASH)
        self.assertEqual(finding.location, self.GOOD_LOCATION)
        self.assertEqual(finding.tags, self.GOOD_TAGS)
        self.assertEqual(finding.image_hash, self.IMAGE_HASH)

        finding = Finding(self.GOOD_LOCATION, self.GOOD_TAGS)
        self.assertEqual(finding.location, self.GOOD_LOCATION)
        self.assertEqual(finding.tags, self.GOOD_TAGS)
        self.assertEqual(finding.image_hash, None)

    def test_wrong_input(self):
        with self.assertRaises(WrongFindingInputError):
            finding = Finding(self.GOOD_LOCATION, self.BAD_TAGS)

    def test_change_attrs(self):
        finding = Finding(self.GOOD_LOCATION, self.GOOD_TAGS)

        with self.assertRaises(AttributeError):
            finding.location = Location(1,1)

        with self.assertRaises(AttributeError):
            finding.tags = ["123", "sdf"]

    def test_finding_creation_from_json(self):
        finding_as_json = {
            "location": {
                "longitude": self.GOOD_LONGITUDE,
                "latitude": self.GOOD_LATITUDE
            },
            "tags": self.GOOD_TAGS
        }

        finding_as_json2 = {
            "location": {
                "longitude": self.GOOD_LONGITUDE,
                "latitude": self.GOOD_LATITUDE
            },
            "tags": self.GOOD_TAGS,
            "image_hash": self.IMAGE_HASH
        }
        finding = Finding.create_from_json(finding_as_json)
        self.assertEqual(finding.location, self.GOOD_LOCATION)
        self.assertEqual(finding.tags, self.GOOD_TAGS)
        self.assertEqual(finding.image_hash, None)


        finding2 = Finding.create_from_json(finding_as_json2)
        self.assertEqual(finding2.location, self.GOOD_LOCATION)
        self.assertEqual(finding2.tags, self.GOOD_TAGS)
        self.assertEqual(finding2.image_hash, self.IMAGE_HASH)


    def test_finding_to_dict(self):
        finding = Finding(self.GOOD_LOCATION, self.GOOD_TAGS)
        finding_as_json = finding.to_dict()

        self.assertEqual(finding_as_json["location"]["longitude"], self.GOOD_LONGITUDE)
        self.assertEqual(finding_as_json["location"]["latitude"], self.GOOD_LATITUDE)
        self.assertEqual(finding_as_json["tags"], self.GOOD_TAGS)
        self.assertEqual(finding_as_json["image_hash"], None)


if __name__ == '__main__':
    unittest.main()
