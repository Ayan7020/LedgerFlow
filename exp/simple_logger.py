import logging
import sys 

logger = logging.getLogger(__name__) 
formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
) 


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(fmt=formatter)
 
logger.setLevel(level=logging.INFO)
logger.addHandler(handler)


for name in logging.root.manager.loggerDict: 
    if name in ("uvicorn"):
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers.clear()
        uvicorn_logger.addHandler(hdlr=handler)
        uvicorn_logger.setLevel(level=logging.INFO)