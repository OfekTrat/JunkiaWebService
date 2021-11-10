

class UserNotFoundError(Exception):
    def __init__(self):
        self.message = "User Not Found"
        super(UserNotFoundError, self).__init__(self.message)


class UserAlreadyExistsError(Exception):
    def __init__(self):
        self.message = "User already exists in database"
        super(UserAlreadyExistsError, self).__init__(self.message)
