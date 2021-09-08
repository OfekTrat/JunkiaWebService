from dataclasses import dataclass
from typing import List
from .location import Location


@dataclass
class User:
    id: str
    tags: List[str]
    location: Location
    radius: int
    last_notified: str
