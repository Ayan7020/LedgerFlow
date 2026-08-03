from logging import Logger

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import (
    IntegrityError,
    MultipleResultsFound,
    NoResultFound,
    OperationalError,
    SQLAlchemyError,
)


def _map_sqlalchemy_error(exc: SQLAlchemyError) -> tuple[int, str]:
    if isinstance(exc, IntegrityError):
        return 409, "Integrity constraint violation"
    if isinstance(exc, NoResultFound):
        return 404, "Resource not found"
    if isinstance(exc, MultipleResultsFound):
        return 500, "Multiple records found"
    if isinstance(exc, OperationalError):
        return 503, "Database unavailable"
    return 500, "Database error"


def register_sqlalchemy_handlers(app: FastAPI, logger: Logger):
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        status_code, message = _map_sqlalchemy_error(exc)

        if status_code >= 500:
            logger.opt(exception=exc).error("SQLAlchemy error")
        else:
            logger.opt(exception=exc).warning("SQLAlchemy error")

        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "message": message,
                "data": {},
            },
        )
