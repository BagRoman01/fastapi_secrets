from fastapi import HTTPException, FastAPI
from starlette import status
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from src.base.exc_handlers import http_exception_handler
from src.base.exc_handlers import validation_exception_handler

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

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError,
                              validation_exception_handler)