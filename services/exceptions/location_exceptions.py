
class InvalidLocationError(Exception):
    def __init__(self, message: str = "Invalid Coordinates"):
        self.message = message
        super(InvalidLocationError, self).__init__(self.message)
