from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):  
    from .config import get_config 

    get_config() 
    yield
    # await clear_db_connection()