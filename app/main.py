from typing import Optional

from fastapi import FastAPI

from app.core import get_config, lifespan, setup_logger, app_logger
from app.core.observability import Observability
from app.core.exceptions import register_exception_handlers
from app.api.v1 import V1Router

def create_app() -> FastAPI: 
    config = get_config()

    obs: Optional[Observability] = None

     
    if config.is_prod:
        obs = Observability(config.app_name, config.better_stack_host, config.better_stack_source_token)
        obs.setup()
        setup_logger(is_prod=True, obs_handler=obs.get_logging_handler())
    else:
        setup_logger()

    app = FastAPI(title=config.app_name, lifespan=lifespan)
    register_exception_handlers(app, app_logger) 

    if config.db_username and config.db_password and config.db_host and config.db_port and config.db_name:
        from app.db import init_db,get_engine
        init_db(
            db_username=config.db_username,
            db_password=config.db_password,
            db_host=config.db_host,
            db_port=config.db_port,
            db_name=config.db_name
        )
        
        if obs is not None and get_engine() is not None: 
            obs.instrument(app, get_engine())

    app.include_router(V1Router)

    return app


app = create_app() 