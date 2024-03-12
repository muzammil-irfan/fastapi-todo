# Custom exception for authentication error
class AuthenticationError(Exception):
    def __init__(self, message):
        self.message = message

# Custom exception for validation error
class ValidationError(Exception):
    def __init__(self, message):
        self.message = message

# Custom exception for general error
class AppError(Exception):
    def __init__(self, message):
        self.message = message
