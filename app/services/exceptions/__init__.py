# app/core/exception_handlers.py
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError

from app.services.exceptions.handlers import http_exception_handler
from app.services.exceptions.handlers import validation_exception_handler


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
