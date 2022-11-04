from fastapi import HTTPException


class GeneralException(HTTPException):
    def __init__(self, status_code: int, message: str, detail: dict = None):
        super().__init__(
            status_code=status_code, detail=dict(message=message, detail=detail)
        )


# ======================== DB ============================
class DatabaseException(GeneralException):
    def __init__(self, message: str, detail: dict = None):
        super().__init__(status_code=500, message=message, detail=detail)


class DatabaseItemNotFoundException(GeneralException):
    def __init__(self, message: str, detail: dict = None):
        super().__init__(status_code=404, message=message, detail=detail)


# ======================== CRUD ==========================
class CrudException(GeneralException):
    def __init__(self, message: str, detail: dict = None):
        super().__init__(status_code=500, message=message, detail=detail)


class CrudItemNotFoundException(GeneralException):
    def __init__(self, message: str, detail: dict = None):
        super().__init__(status_code=404, message=message, detail=detail)

# ======================== USER ==========================
class UnauthorizedException(GeneralException):
    def __init__(self, message: str, detail: dict = None):
        super().__init__(status_code=401, message=message, detail=detail)