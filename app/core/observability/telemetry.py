from opentelemetry.sdk.resources import Resource
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from opentelemetry.sdk._logs import LoggerProvider,LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter 

def create_resource(resource_name: str) -> Resource:
    return Resource.create({
        "service.name": resource_name,
    })

def setup_tracer_provider(resource: Resource,host: str,token: str):
    provider = TracerProvider(resource=resource)

    exporter = OTLPSpanExporter(
        endpoint=f"{host}/v1/traces",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    provider.add_span_processor(
        BatchSpanProcessor(exporter)
    )

    trace.set_tracer_provider(provider)


def setup_logger_provider(resource: Resource,host: str,token: str) -> LoggingHandler:
    provider = LoggerProvider(resource=resource)

    exporter = OTLPLogExporter(
        endpoint=f"{host}/v1/logs",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    provider.add_log_record_processor(
        BatchLogRecordProcessor(exporter)
    )

    set_logger_provider(provider)

    return LoggingHandler(
        logger_provider=provider
    )