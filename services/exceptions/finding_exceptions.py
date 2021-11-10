

class WrongFindingInputError(Exception):
    def __init__(self, message: str = "Wrong input for finding"):
        self.message = message
        super(WrongFindingInputError, self).__init__(self.message)


class FindingNotFoundError(Exception):
    def __init__(self):
        self.message = "Finding not found"
        super(FindingNotFoundError, self).__init__(self.message)
