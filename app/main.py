from fastapi import FastAPI


from app.core import Config,get_config,lifespan
from app.core.observability import setup_logger,app_logger,AppInstrumentor

def build_app(config: Config):
    app = FastAPI(
        title=config.app_name,
        lifespan=lifespan
    )
    return app 

config = get_config() 
setup_logger(config.is_prod)


app = build_app(config)
AppInstrumentor(app)

@app.get("/HOME")
async def HOME():
    app_logger.info("HOME ROUTE")
    return None