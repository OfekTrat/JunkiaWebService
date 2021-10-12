from typing import List
from ..interfaces import IImageCommunicator
from ...image import Image
from google.cloud import storage
from .exceptions import ImageNotFoundError, ImageAlreadyExistsError


class ImageCloudCommunicator(IImageCommunicator):
    def __init__(self, bucket_name: str):
        self.__client: storage.Client = storage.Client()
        self.__bucket: storage.Bucket = self.__client.bucket(bucket_name)
        self.__tmp_filename = "./tmp_file"

    def get(self, image_hash: str) -> Image:
        try:
            blob = self.__bucket.blob(image_hash)
            image_data = blob.download_as_bytes()
            image = Image(image_hash, image_data)
            return image
        except Exception as e:
            raise ImageNotFoundError()

    def upload(self, image: Image):
        blob = self.__bucket.blob(image.hash)
        blob.upload_from_string(image.data)

    def delete(self, image_id: str):
        raise NotImplementedError()

    def delete_multiple(self, image_hashes: List[str]):
        for image_hash in image_hashes:
            blob = self.__bucket.blob(image_hash)
            blob.delete()
