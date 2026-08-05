from opentelemetry import trace
from functools import wraps
import inspect


_tracer = trace.get_tracer("ledgerflow")

def get_tracer():
    return _tracer

def tracing(name: str | None = None):
    def decorator(fn):
        span_name = name or f"{fn.__qualname__}"

        if inspect.iscoroutinefunction(fn):
            @wraps(fn)
            async def async_wrapper(*args,**kwargs):
                with _tracer.start_as_current_span(span_name):
                    return await fn(*args, **kwargs)
            return async_wrapper

        @wraps(fn)
        def sync_wrapper(*args, **kwargs):
            with _tracer.start_as_current_span(span_name):
                return fn(*args, **kwargs)
        return sync_wrapper

    return decorator