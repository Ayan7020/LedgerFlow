from fastapi import FastAPI


from app.core import Config,get_config,lifespan,setup_logger,app_logger
from app.core.observability import Observability
from app.core.exceptions import register_exception_handlers

def build_app(config: Config):
    app = FastAPI(
        title=config.app_name,
        lifespan=lifespan
    )
    return app 

config = get_config() 
app = build_app(config)
register_exception_handlers(app,app_logger)
if(config.is_prod):
    obs = Observability(config.app_name,config.better_stack_host,config.better_stack_source_token)
    obs.setup()
    obs.instrument(app)

    setup_logger(True,obs.get_logging_handler())
else:
    setup_logger()