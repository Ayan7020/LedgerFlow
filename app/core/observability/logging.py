import logging 
from loguru import  logger
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
            print(frame)
            frame = frame.f_back
            depth += 1

        logger.opt(
            depth=depth,
            exception=record.exc_info
        ).log(
            level,
            record.getMessage() 
        )
        

        

def setup_logger(is_prod: bool = False):
    """"""
    logger.remove()
    if not is_prod:
        logger.add(sys.stdout)
    else:
        logger.add(sys.stdout, serialize= True)

    # UVICORN LOGGING SENDING TO THE LOGURU   
    for name in logging.root.manager.loggerDict: 
        if name in ("uvicorn"):
            uvicorn_logger = logging.getLogger(name)
            uvicorn_logger.handlers.clear() 
            uvicorn_logger.setLevel(level=logging.INFO)
            uvicorn_logger.addHandler(InterCeptHandler())
     