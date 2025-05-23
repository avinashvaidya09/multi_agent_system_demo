"""This module is specifically created for observability.
Returns:
    The AgentObservability instance.
"""

import time
import asyncio
from functools import wraps
from opentelemetry.sdk.resources import Resource
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
    ConsoleSpanExporter,
    BatchSpanProcessor,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server


class AgentObservability:
    """This class contains methods for tracing agents."""

    _instances = {}  # singleton instances per service name

    def __new__(cls, service_name="default_app"):
        """Ensures only one instance of AgentObservability"""
        if service_name not in cls._instances:
            cls._instances[service_name] = super(AgentObservability, cls).__new__(cls)
            cls._instances[service_name].init_observability(service_name)
        return cls._instances[service_name]

    def __init__(self, service_name="default_app"):  # do not remove service_name parameter.
        """Define all instance attributes

        Keyword Arguments:
            service_name -- The service name (default: {"default_app"})
        """
        if not hasattr(self, "resource"):
            self.resource = None
            self.tracer = None
            self.tracer_provider = None
            self.meter_provider = None
            self.meter = None
            self.request_counter = None
            self.request_size_histogram = None

    def init_observability(self, service_name="default_app"):
        """Initializes observability attributes

        Keyword Arguments:
            service_name -- The service name (default: {"default_app"})
        """
        # Create a resource
        self.resource = Resource.create({"service.name": service_name})

        # Set up OpenTelemetry Tracing
        self.tracer_provider = TracerProvider(resource=self.resource)
        trace.set_tracer_provider(self.tracer_provider)

        # Export traces to console for debugging
        self.tracer_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

        # Export traces to Grafana Tempo
        otlp_exporter = OTLPSpanExporter(
            endpoint="http://localhost:4327", insecure=True
        )  # TBD: Remove insecure=True for production
        self.tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

        # Tracer
        self.tracer = trace.get_tracer(service_name)

        # Set up OpenTelemetry Metrics
        start_http_server(8000)  # Metrics endpoint http://localhost:8000/metrics
        prometheus_reader = PrometheusMetricReader()
        self.meter_provider = MeterProvider(
            metric_readers=[
                prometheus_reader,
                PeriodicExportingMetricReader(ConsoleMetricExporter()),
            ],
            resource=self.resource,
        )

        set_meter_provider(self.meter_provider)

        # Create a Meter
        self.meter = self.meter_provider.get_meter(service_name)

        # Define a counter metric
        self.request_counter = self.meter.create_counter(
            name="http_request_count",
            description="Counts the number of HTTP requests",
            unit="requests",
        )

        self.request_size_histogram = self.meter.create_histogram(
            name="request_size_bytes",
            description="Tracks the size of HTTP request payloads",
            unit="bytes",
        )

    def track_request(self, endpoint: str, request_size_in_bytes: int):
        """Tracks the requests.

        Arguments:
            endpoint -- API endpoint name.
        """
        self.request_counter.add(1, {"endpoint": endpoint})
        self.request_size_histogram.record(
            request_size_in_bytes, {"request_size_in_bytes": request_size_in_bytes}
        )

    def metric_collector(self, endpoint: str):
        """Decorator to capture metrics.

        Arguments:
            endpoint -- The API endpoint name.
        """

        def decorator(func):
            if asyncio.iscoroutinefunction(func=func):

                @wraps(func)
                async def async_wrapper(*args, **kwargs):
                    start_time = time.time()

                    request_payload = kwargs.get("request")
                    agent_name = getattr(request_payload, "agent_name", "NOT PROVIDED")

                    request_json_dump = request_payload.model_dump_json()
                    request_size_in_bytes = len(request_json_dump.encode("utf-8"))

                    with self.tracer.start_as_current_span(
                        endpoint, kind=trace.SpanKind.SERVER
                    ) as span:
                        span.set_attribute("api_endpoint", endpoint)
                        span.set_attribute("request_size_in_bytes", request_size_in_bytes)
                        span.set_attribute("agent_name", agent_name)
                        response = await func(*args, **kwargs)
                        end_time = time.time()
                        response_time = (end_time - start_time) * 1000
                        self.track_request(
                            endpoint,
                            request_size_in_bytes=request_size_in_bytes,
                        )
                        span.set_attribute("response_time_ms", response_time)
                        return response

                return async_wrapper
            else:

                @wraps(func)
                def sync_wrapper(*args, **kwargs):
                    start_time = time.time()
                    request_payload = kwargs.get("request")
                    agent_name = getattr(request_payload, "agent_name", "NOT PROVIDED")

                    request_json_dump = request_payload.model_dump_json()
                    request_size_in_bytes = len(request_json_dump.encode("utf-8"))

                    with self.tracer.start_as_current_span(
                        endpoint, kind=trace.SpanKind.SERVER
                    ) as span:
                        span.set_attribute("api_endpoint", endpoint)
                        span.set_attribute("request_size_in_bytes", request_size_in_bytes)
                        span.set_attribute("agent_name", agent_name)
                        response = func(*args, **kwargs)
                        end_time = time.time()
                        response_time = (end_time - start_time) * 1000
                        self.track_request(
                            endpoint,
                            request_size_in_bytes=request_size_in_bytes,
                        )
                        span.set_attribute("response_time_ms", response_time)
                        return response

                return sync_wrapper

        return decorator

    def trace_agent_function(self, function_name: str):
        """Decorator to create spans for agent functions under the API trace."""

        def decorator(func):
            if asyncio.iscoroutinefunction(func):

                @wraps(func)
                async def async_wrapper(*args, **kwargs):
                    parent_span = trace.get_current_span()  # Fetch the current span
                    print(parent_span)
                    with self.tracer.start_as_current_span(
                        function_name, context=trace.set_span_in_context(parent_span)
                    ) as span:
                        span.set_attribute("agent_function", function_name)
                        start_time = time.time()
                        response = await func(*args, **kwargs)
                        end_time = time.time()
                        response_time = (end_time - start_time) * 1000
                        span.set_attribute("response_time_ms", response_time)
                        return response

                return async_wrapper
            else:

                @wraps(func)
                def sync_wrapper(*args, **kwargs):
                    parent_span = trace.get_current_span()  # Get the API trace span
                    print(parent_span)
                    with self.tracer.start_as_current_span(
                        function_name, context=trace.set_span_in_context(parent_span)
                    ) as span:
                        span.set_attribute("agent_function", function_name)
                        start_time = time.time()
                        response = func(*args, **kwargs)
                        end_time = time.time()
                        response_time = (end_time - start_time) * 1000
                        span.set_attribute("response_time_ms", response_time)
                        return response

                return sync_wrapper

        return decorator
