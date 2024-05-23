class UserNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UserNotFoundError(UserNotFoundException):
    def __init__(self, phone: str) -> None:
        super().__init__(f"User not found with the phone number: {phone}")
