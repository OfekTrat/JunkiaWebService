from project.src.location import Location, InvalidLocationError
import unittest


class MyTestCase(unittest.TestCase):
    VALID_LONGITUDE = 50
    VALID_LATITUDE = -30
    INVALID_LONGITUDE = -189
    INVALID_LATITUDE = 100

    def test_location_creation(self):
        location = Location(self.VALID_LONGITUDE, self.VALID_LATITUDE)
        self.assertEqual(location.longitude, self.VALID_LONGITUDE)
        self.assertEqual(location.latitude, self.VALID_LATITUDE)

        with self.assertRaises(InvalidLocationError):
            location = Location(self.VALID_LONGITUDE, self.INVALID_LATITUDE)

        with self.assertRaises(InvalidLocationError):
            location = Location(self.INVALID_LONGITUDE, self.VALID_LATITUDE)

    def test_location_to_dict(self):
        location = Location(self.VALID_LONGITUDE, self.VALID_LATITUDE)
        location_as_json = location.to_dict()

        self.assertEqual(location_as_json["longitude"], self.VALID_LONGITUDE)
        self.assertEqual(location_as_json["latitude"], self.VALID_LATITUDE)

    def test_location_creation_from_dict(self):
        location_as_dict = {
            "longitude": self.VALID_LONGITUDE,
            "latitude": self.VALID_LATITUDE
        }
        location = Location.create_from_json(location_as_dict)
        self.assertEqual(location.latitude, self.VALID_LATITUDE)
        self.assertEqual(location.longitude, self.VALID_LONGITUDE)


if __name__ == '__main__':
    unittest.main()
