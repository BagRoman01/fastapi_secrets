from fastapi.responses import JSONResponse
from starlette import status


async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={'message': 'Invalid input', 'errors': exc.errors()},
    )


async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={'errors': exc.detail})
