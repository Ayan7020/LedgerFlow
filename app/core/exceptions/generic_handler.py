from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from .app_exeception import AppException

from logging import Logger

def register_generic_handlers(app: FastAPI,logger: Logger):

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request,exc: AppException):
        logger.opt(exception=exc).warning("App Exception")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "data": exc.details,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request,exc: Exception):
        logger.opt(exception=exc).critical("Unhandled exception")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal Server Error",
                "data": {},
            },
        )