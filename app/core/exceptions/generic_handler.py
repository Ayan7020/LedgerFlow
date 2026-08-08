from fastapi import FastAPI,Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from .app_exeception import AppException

from logging import Logger

def register_generic_handlers(app: FastAPI,logger: Logger):

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request,exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "data": exc.details,
            },
        )

    @app.exception_handler(404)
    async def route_not_found_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=404,
            content={
                "success": False, 
                "message": f"Route '{request.url.path}' not found", 
                "data": {}
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