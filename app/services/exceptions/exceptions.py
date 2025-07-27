from fastapi import HTTPException
from starlette import status


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class SecretNotFoundException(CustomHTTPException):
    def __init__(self, detail: str = 'Secret with this id was not found!'):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class WrongSecretPasswordException(CustomHTTPException):
    def __init__(self, detail: str = 'Wrong password for the secret!'):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class ErrorDecryptSecretException(CustomHTTPException):
    def __init__(self, detail: str = 'Could not decrypt secret!'):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
