from typing import List, Union, Dict, Optional, Any
from services.exceptions import WrongFindingInputError
from datetime import datetime
from models.location import Location


class Finding:
    def __init__(self, location: Location, tags: List[str], image_hash: Optional[str] = None,
                 finding_id: Optional[str] = None):
        self.__id = self.__set_id(finding_id)
        self.__location = location
        self.__tags: List[str] = self.__validate_tags(tags)
        self.__image_hash: str = image_hash

    def __set_id(self, finding_id: Optional[str]) -> str:
        if finding_id is not None:
            return finding_id
        else:
            return str(int(datetime.now().timestamp()))

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, finding_id: str):
        self.__id = finding_id

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
    def __validate_tags(tags: Any) -> List[str]:
        if not tags or not isinstance(tags, list):
            raise WrongFindingInputError("Missing Tags")

        return tags

    def to_dict(self):
        return {
            "id": self.id,
            "longitude": self.location.longitude,
            "latitude": self.location.latitude,
            "tags": self.tags,
            "image_hash": self.image_hash
        }

    @classmethod
    def create_from_json(cls, finding_as_json: Dict[str, Union[str, float, List[str],
                                                               Dict[str, float], None]]) -> 'Finding':
        if cls.__validate_json(finding_as_json) and cls.__validate_tags(finding_as_json['tags']):
            location = Location(finding_as_json["longitude"], finding_as_json["latitude"])
            finding_id = finding_as_json["id"]
            tags = finding_as_json["tags"]
            image_hash = finding_as_json["image_hash"]
            return Finding(location, tags, image_hash, finding_id)
        else:
            raise WrongFindingInputError("Wrong Json")

    @classmethod
    def __validate_json(cls, finding_json: Dict[str, Union[str, float, List[str], Dict[str, float], None]]) -> bool:
        return "id" in finding_json and "image_hash" in finding_json and "longitude" in finding_json and \
               "latitude" in finding_json and "tags" in finding_json
