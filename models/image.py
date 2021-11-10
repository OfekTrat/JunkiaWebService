import base64
from dataclasses import dataclass
from typing import Dict


@dataclass
class Image:
    hash: str
    data: bytes

    def to_json(self) -> Dict[str, str]:
        return {
            "hash": self.hash,
            "data": base64.b64encode(self.data).decode()
        }

    @staticmethod
    def from_json(json) -> 'Image':
        return Image(json['hash'], base64.b64decode(json["data"]))
