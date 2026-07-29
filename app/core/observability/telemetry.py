from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

def setup_telemetry(app_name: str,host: str,token: str):
    resource = Resource.create({
        "service.name": app_name
    })

    provider = TracerProvider