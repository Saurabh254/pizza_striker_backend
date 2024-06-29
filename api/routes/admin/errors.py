class AdminNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class AdminNotFoundError(AdminNotFoundException):
    def __init__(self, phone: str) -> None:
        super().__init__(
            f"Admin not found with the phone number associated with {phone}"
        )
