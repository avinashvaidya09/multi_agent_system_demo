## Introduction

This POC focuses on code based agent evaluation with the intent to showcase: 

1. Metrics and traces collection using opentelemetry SDK.
2. Metrics storage in Prometheus.
3. Trace export to OpenTelemetry collector, eventually stored in Grafana Tempo datastore.
4. Metrics and traces visualization using Grafana dashboard.

## Tools used

**Pre-requisite:** All the below tools are installed using docker images

1. **Prometheus:** Time series data store for collecting metric data and alerting.
2. **Grafana Tempo:** A distributed tracing backend that simplifies storing and visualizing trace data.
3. **OpenTelemetry Collector:** Acts as a central hub for receiving traces and exporting telemetry data to  observability backends.
4. **Grafana:** Grafana is an interactive data visualization and monitoring platform that allows users to query, visualize, and understand data from various source.

## Block Diagram

- The below diagrams shows how the metrics and traces are collected
  and visualized.

    ```mermaid
    graph TD;
    A[Agent: Python App] -->|Generates Metrics and Traces| B[OpenTelemetry SDK];
    B -->|Scrapes Metrics| C[Prometheus: Metric Store];
    B -->|Sends Traces via OTLP| D[OpenTelemetry Collector];
    D -->|Forwards Traces| E[Grafana Tempo: Trace Store];
    C <--> |Queries Metrics| F[Grafana Dashboard];
    E <--> |Queries Traces| F[Grafana Dashboard];
    
    subgraph Observability Stack
        C
        E
        F
    end
    ```

## What you will see in the Evaluation Dashboard

### Metrics

1. Number of requests hitting the **/chat** endpoint **(http_request_count)**
2. Size of the request in bytes **(request_size_in_bytes)**

### Traces and span attributes

1. API endpoint **(api_endpoint)**
2. Agent name **(agent_name)**
3. Request size in bytes **(request_size_in_bytes)**
4. Response time in milliseconds **(response_time_ms)**

## Questions (Add questions in this section)

1. Why we used **OpenTelemetry Collector** for traces and not for prometheus?

  ```
  1. Grafana Tempo only supports OTLP, but if you were using other backends (Jaeger, Zipkin, etc.), the collector would convert OTLP to the required format.

  2. Traces can generate a huge amount of data, so the collector can sample traces, reducing storage costs.

  3. Metrics are much simpler to process compared to traces because:
    - They are structured numeric data (counters, histograms, gauges).
    - Prometheus is designed to scrape and store time-series data efficiently.
    - Prometheus pulls data instead of receiving it.
  ```