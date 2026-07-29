from .logging import logger as app_logger,setup_logger

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor as AppInstrumentor
