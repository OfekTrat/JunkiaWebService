from dataclasses import dataclass
from typing import List, Any, Dict
from .location import Location


@dataclass
class User:
    id: str
    tags: List[str]
    location: Location
    radius: int
    last_notified: str

    @staticmethod
    def create_from_json(user_as_json: Dict[str, Any]) -> 'User':
        location = Location(user_as_json["longitude"], user_as_json["latitude"])

        return User(user_as_json["id"], user_as_json["tags"], location,
                    user_as_json["radius"], user_as_json["last_notified"])

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "tags": self.tags,
            "longitude": self.location.longitude,
            "latitude": self.location.latitude,
            "radius": self.radius,
            "last_notified": self.last_notified
        }
