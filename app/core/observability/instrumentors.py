from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

def instrument_fastapi(app: FastAPI):
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

    return FastAPIInstrumentor.instrument_app(app)


def instrument_sqlalchemy(engine: AsyncEngine):
    from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor 
    return AsyncPGInstrumentor().instrument()
