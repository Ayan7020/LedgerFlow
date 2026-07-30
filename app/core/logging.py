import logging 
from loguru import  logger
import logging
import sys

class InterCeptHandler(logging.Handler):
    def emit(self, record) -> None: 
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame,depth = logging.currentframe(),2 
        while frame and frame.f_code.co_filename == logging.__file__:  
            frame = frame.f_back
            depth += 1

        logger.bind(
            source_logger=record.name
        ).opt(
            depth=depth,
            exception=record.exc_info
        ).log(
            level,
            record.getMessage() 
        )
        

        

def setup_logger(is_prod: bool = False,obs_handler = None):
    """"""
    logger.remove()
    if not is_prod:
        logger.add(sys.stdout)
        # UVICORN LOGGING SENDING TO THE LOGURU   
        for name in logging.root.manager.loggerDict: 
            if name in ("uvicorn"):
                uvicorn_logger = logging.getLogger(name)
                uvicorn_logger.handlers.clear() 
                uvicorn_logger.setLevel(level=logging.INFO)
                uvicorn_logger.addHandler(InterCeptHandler())
    else:
        logger.add(sys.stdout, serialize=True)
        if obs_handler is not None:
            obs_logger = logging.getLogger("obs")
            obs_logger.handlers.clear()
            obs_logger.addHandler(obs_handler)
            obs_logger.propagate = False
            obs_logger.setLevel(logging.INFO)

            def obs_sink(message):  
                record = message.record 
                obs_logger.log(
                    level=record["level"].no,
                    exc_info=record["exception"],
                    msg=record["message"]
                )
            logger.add(obs_sink)
     