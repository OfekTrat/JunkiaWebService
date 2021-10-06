import os
import unittest
from project.src.image import Image
from project.src.db_communicators.image_communicator import ImageCommunicator
from project.src.db_communicators.image_communicator.exceptions import ImageNotFoundError


class TestImageCommunicator(unittest.TestCase):
    def test_get_image(self):
        image_hash = "test"
        image = ImageCommunicator.get(image_hash)

        assert image.hash == image_hash
        assert image.data == "test_image_data".encode()

    def test_upload_image(self):
        image = Image("test_upload", "test_upload_image".encode())
        ImageCommunicator.upload(image)
        path = os.path.join(ImageCommunicator.PATH, image.hash)

        assert os.path.exists(path)

        with open(path, "rb") as f:
            assert f.read() == image.data

        os.remove(path)

    def test_delete_image(self):
        path = os.path.join(ImageCommunicator.PATH, "test_delete")

        with open(path, "wb") as f:
            f.write("test_delete".encode())

        ImageCommunicator.delete("test_delete")

        assert not os.path.exists(path)

    def test_get_nonexistant_image(self):
        with self.assertRaises(ImageNotFoundError):
            ImageCommunicator.get("3456ujnkp")



if __name__ == '__main__':
    unittest.main()
