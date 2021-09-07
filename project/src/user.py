from dataclasses import dataclass
from typing import List
from src.location import Location


@dataclass
class User:
    id: str
    follows: List[str]
    notifiable_location: Location
    notifiable_radius: int
