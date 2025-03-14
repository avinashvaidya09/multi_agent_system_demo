"""This module is specifically created for observability.
Returns:
    The AgentObservability instance.
"""

import time
import asyncio
from functools import wraps
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader


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
            self.response_time_histogram = None

    def init_observability(self, service_name="default_app"):
        """Initializes observability attributes

        Keyword Arguments:
            service_name -- The service name (default: {"default_app"})
        """
        # Create a resource
        self.resource = Resource.create({"service.name": service_name})

        # Set up a meter provider for metric collection
        self.meter_provider = MeterProvider(
            metric_readers=[PeriodicExportingMetricReader(ConsoleMetricExporter())],
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

        # Define a histogram metric for response time (latency)
        self.response_time_histogram = self.meter.create_histogram(
            name="http_response_time",
            description="Records the response time of HTTP requests",
            unit="ms",
        )

    def track_request(self, endpoint: str, response_time: str):
        """Tracks the requests.

        Arguments:
            endpoint -- API endpoint name.
        """
        self.request_counter.add(1, {"endpoint": endpoint})
        self.response_time_histogram.record(response_time, {"endpoint": endpoint})

    def metric_decorator(self, endpoint: str):
        """Decorator to capture metrics.

        Arguments:
            endpoint -- The API endpoint name.
        """

        def decorator(func):
            if asyncio.iscoroutinefunction(func=func):

                @wraps(func)
                async def async_wrapper(*args, **kwargs):
                    start_time = time.time()
                    response = await func(*args, **kwargs)
                    end_time = time.time()
                    response_time = (end_time - start_time) * 1000
                    self.track_request(endpoint, response_time=response_time)
                    return response

                return async_wrapper
            else:

                @wraps(func)
                def sync_wrapper(*args, **kwargs):
                    start_time = time.time()
                    response = func(*args, **kwargs)
                    end_time = time.time()
                    response_time = (end_time - start_time) * 1000
                    self.track_request(endpoint, response_time=response_time)
                    return response

                return sync_wrapper

        return decorator
