import os
from typing import List
from project.src.image import Image
from .exceptions import ImageNotFoundError
from project.src.db_communicators.interfaces.idbcommunicator import IDBCommunicator
from project.src.db_communicators.interfaces.imultiple_delete_communicator import IMultipleDeleteCommunicator


class ImageCommunicator(IDBCommunicator, IMultipleDeleteCommunicator):
    PATH = r"d:\git\JunkiaWebService\project\images"

    @classmethod
    def get(cls, image_hash: str) -> Image:
        path = cls.__get_path(image_hash)

        try:
            with open(path, "rb") as f:
                image_data = f.read()
        except FileNotFoundError:
            raise ImageNotFoundError()

        return Image(image_hash, image_data)

    @classmethod
    def upload(cls, image: Image):
        path = cls.__get_path(image.hash)

        with open(path, "wb") as f:
            f.write(image.data)

    @classmethod
    def delete(cls, image_hash: str):
        cls.delete_multiple([image_hash])

    @classmethod
    def delete_multiple(cls, image_hashes: List[str]):
        for image_hash in image_hashes:
            try:
                path = cls.__get_path(image_hash)
                cls.__remove_path(path)
            except ImageNotFoundError:
                continue

    @classmethod
    def __remove_path(cls, path: str):
        try:
            os.remove(path)
        except FileNotFoundError:
            raise ImageNotFoundError()

    @classmethod
    def __get_path(cls, image_hash: str) -> str:
        return os.path.join(cls.PATH, image_hash)
