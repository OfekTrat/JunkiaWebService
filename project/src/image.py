from dataclasses import dataclass


@dataclass
class Image:
    hash: str
    data: bytes
