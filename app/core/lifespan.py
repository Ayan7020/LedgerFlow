from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):  
    from .config import get_config 
    # from app.db.engine import init_db, dispose_db

    config = get_config()

    # if config.db_username and config.db_password and config.db_host and config.db_port and config.db_name:
    #     init_db(
    #         db_username=config.db_username,
    #         db_password=config.db_password,
    #         db_host=config.db_host,
    #         db_port=config.db_port,
    #         db_name=config.db_name
    #     )

    yield
 
    # await dispose_db()