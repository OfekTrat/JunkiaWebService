

class ImageNotFoundError(Exception):
    def __init__(self):
        self.message = "Image not found"
        super(ImageNotFoundError, self).__init__(self.message)


class ImageAlreadyExistsError(Exception):
    def __init__(self):
        self.message = "Image already exists in DB"
        super(ImageAlreadyExistsError, self).__init__(self.message)
