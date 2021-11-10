import os
from typing import List
from models.image import Image
from services.image_service import ImageNotFoundError, ImageAlreadyExistsError
from ..interfaces import IImageCommunicator


class SimpleImageCommunicator(IImageCommunicator):
    PATH = "images"

    def __init__(self):
        if not os.path.exists(self.PATH):
            os.mkdir(self.PATH)

    def get(self, image_hash: str) -> Image:
        path = self.__get_path(image_hash)

        try:
            with open(path, "rb") as f:
                image_data = f.read()
        except FileNotFoundError:
            raise ImageNotFoundError()

        return Image(image_hash, image_data)

    def upload(self, image: Image):
        path = self.__get_path(image.hash)

        if not os.path.exists(path):
            with open(path, "wb") as f:
                f.write(image.data)
        else:
            raise ImageAlreadyExistsError()

    def delete(self, image_hash: str):
        self.delete_multiple([image_hash])

    def delete_multiple(self, image_hashes: List[str]):
        for image_hash in image_hashes:
            try:
                path = self.__get_path(image_hash)
                self.__remove_path(path)
            except ImageNotFoundError:
                continue

    @staticmethod
    def __remove_path(path: str):
        try:
            os.remove(path)
        except FileNotFoundError:
            raise ImageNotFoundError()

    def __get_path(self, image_hash: str) -> str:
        return os.path.join(self.PATH, image_hash)
