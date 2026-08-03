from fastapi import FastAPI

from .generic_handler import register_generic_handlers
from .sql_alchemy_handler import register_sqlalchemy_handlers


def register_exception_handlers(app: FastAPI, logger):
    register_sqlalchemy_handlers(app, logger)
    register_generic_handlers(app, logger)