from fastapi import FastAPI

def instrument_fastapi(app: FastAPI):
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

    return FastAPIInstrumentor.instrument_app(app)
