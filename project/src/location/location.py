from typing import Tuple, Dict, Union
from .location_exceptions import InvalidLocationError


class Location:
    LONGITUDE_RANGE = (-180, 180)
    LATITUDE_RANGE = (-90, 90)

    def __init__(self, longitude: Union[float, int], latitude: Union[float, int]):
        self.__longitude = self.__validate_range(longitude, self.LONGITUDE_RANGE)
        self.__latitude = self.__validate_range(latitude, self.LATITUDE_RANGE)

    @property
    def longitude(self) -> float:
        return self.__longitude

    @property
    def latitude(self) -> float:
        return self.__latitude

    @staticmethod
    def __validate_range(value: float, valid_range: Tuple[int, int]) -> float:
        if value < valid_range[0] or value > valid_range[1]:
            raise InvalidLocationError

        return value

    def to_dict(self) -> Dict[str, float]:
        return {
            "longitude": self.longitude,
            "latitude": self.latitude
        }

    @staticmethod
    def create_from_json(location_as_json: Dict[str, float]) -> 'Location':
        return Location(location_as_json["longitude"], location_as_json["latitude"])

    def __eq__(self, other: 'Location'):
        return other.longitude == self.longitude and other.latitude == self.latitude