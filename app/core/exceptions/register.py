from fastapi import FastAPI
 
from .generic_handler import register_generic_handlers 


def register_exception_handlers(app: FastAPI,logger): 
    register_generic_handlers(app,logger)