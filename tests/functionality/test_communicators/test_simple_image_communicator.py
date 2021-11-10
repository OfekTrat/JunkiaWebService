import os
import unittest
from models.image import Image
from communicators.image_communicators import SimpleImageCommunicator
from services.exceptions import ImageNotFoundError


class TestImageCommunicator(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestImageCommunicator, self).__init__(*args, **kwargs)
        self.__image_comm = SimpleImageCommunicator()

    def test_get_image(self):
        image_hash = "test"
        image = self.__image_comm.get(image_hash)

        assert image.hash == image_hash
        assert image.data == "test_image_data".encode()

    def test_upload_image(self):
        image = Image("test_upload", "test_upload_image".encode())
        self.__image_comm.upload(image)
        path = os.path.join(self.__image_comm.PATH, image.hash)

        assert os.path.exists(path)

        with open(path, "rb") as f:
            assert f.read() == image.data

        os.remove(path)

    def test_delete_image(self):
        path = os.path.join(self.__image_comm.PATH, "test_delete")

        with open(path, "wb") as f:
            f.write("test_delete".encode())

        self.__image_comm.delete("test_delete")

        assert not os.path.exists(path)

    def test_get_nonexistant_image(self):
        with self.assertRaises(ImageNotFoundError):
            self.__image_comm.get("3456ujnkp")


if __name__ == '__main__':
    unittest.main()
