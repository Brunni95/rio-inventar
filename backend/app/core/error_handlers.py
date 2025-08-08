from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
import logging

logger = logging.getLogger(__name__)

def init_error_handlers(app):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning("Validation error: %s", exc.errors())
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"status": "error", "message": "Validation failed", "details": exc.errors()}
        )

    @app.exception_handler(IntegrityError)
    async def integrity_exception_handler(request: Request, exc: IntegrityError):
        logger.error("Database integrity error: %s", exc)
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"status": "error", "message": "Database constraint violated"}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.exception("Unexpected error: %s", exc)
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": "An unexpected error occurred"}
        )
