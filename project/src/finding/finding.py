from typing import List, Tuple, Union, Dict, Optional
from .finding_exceptions import WrongFindingInputError
from datetime import datetime
from src.location import Location


class Finding:
    LONGITUDE_RANGE = (-180, 180)
    LATITUDE_RANGE = (-90, 90)

    def __init__(self, location: Location, tags: List[str], image_hash: Optional[str] = None):
        self.__finding_id = datetime.now().timestamp()
        self.__location = location
        self.__tags: List[str] = self.__validate_tags(tags)
        self.__image_hash: str = image_hash

    @property
    def finding_id(self):
        return self.__finding_id

    @property
    def location(self) -> Location:
        return self.__location

    @property
    def tags(self) -> List[str]:
        return self.__tags

    @property
    def image_hash(self) -> str:
        return self.__image_hash

    @image_hash.setter
    def image_hash(self, image_hash: str):
        self.__image_hash = image_hash

    @staticmethod
    def __validate_range(value: float, range: Tuple[int, int]) -> float:
        if value < range[0] or value > range[1]:
            raise WrongFindingInputError(f"Value {value} not in the right range {range}")

        return value

    @staticmethod
    def __validate_tags(tags: List[str]) -> List[str]:
        if not tags:
            raise WrongFindingInputError("Missing Tags")

        return tags

    def to_dict(self):
        return {
            "location": self.location.to_dict(),
            "tags": self.tags,
            "image_hash": self.image_hash
        }

    @staticmethod
    def create_from_json(finding_as_json: Dict[str, Union[str, float, List[str], Dict[str, float]]]) -> 'Finding':
        if "image_hash" not in finding_as_json.keys():
            finding_as_json["image_hash"] = None

        location = Location.create_from_json(finding_as_json["location"])

        return Finding(
            location,
            finding_as_json["tags"],
            finding_as_json["image_hash"]
        )
