from .telemetry import (
    create_resource,

    setup_logger_provider,
    setup_tracer_provider
)

from .instrumentors import (
    instrument_fastapi,
    instrument_sqlalchemy
)

class Observability:
    def __init__(self, app_name, host, token): 
        self._host = host
        self._token = token

        self.__resource = create_resource(app_name)

    def setup(self):
        setup_tracer_provider(resource=self.__resource,host=self._host,token=self._token)
        self.__loging_handler = setup_logger_provider(resource=self.__resource,host=self._host,token=self._token)

    def get_logging_handler(self):  
        return self.__loging_handler
    
    def instrument(self,app,engine):
        instrument_fastapi(app=app)
        instrument_sqlalchemy(engine=engine)