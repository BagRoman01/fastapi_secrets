from fastapi import FastAPI, Request
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={'message': 'Invalid input', 'errors': exc.errors()}
    )

async def http_exception_handler(
    request: Request,
    exc: HTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={'errors': exc.detail}
    )

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
    app.add_exception_handler(
        HTTPException,
        http_exception_handler
    )
    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler
    )