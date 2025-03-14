# Multi Agent System Demo

## Introduction
This project is my effort to demonstrate a **Agentic AI** using **Microsoft AutoGen** for AI-driven intelligence. 
In this project you will learn

1. Create autonomous agents using LLMs and functions
2. Integrate with custom llm models
3. Leverage APIs and LLMs as tools
4. Create multi agent systems
5. Expose multi agent systems as REST APIs

As part of this project you will also learn

1. A clean python project structure
2. Leveraging Python OOP and structural programming paradigms.
3. Why use FAST API?

## Project Structure
```
multi_agent_system_demo/
│── mas_autogen/
|   |__ app                 
|   |   │── agents/                 
|   |   │── functions/                  
|   |   │── services/               
|   |   │── utils/                  
|   │── server.py                   
|__ pyproject.toml                    
│── README.md                     
```

## Setup Instructions
**Pre-requisites** - Install Poetry on you machine - https://python-poetry.org/docs/

#### 1. Clone the github repo

#### 2. Install Poetry & Dependencies
```
poetry install
```

#### 3. Activate Virtual Environment
```
poetry shell
```

#### 4. Run FastAPI Server
```
cd mas_autogen/app && python server.py
```

#### 5. Test your application

1. Pre-requisite: **REST Client** extension for visual studio code.
2. Open [requests.http](/requests.http)
3. Click of **Send Request** on any of the available sample requests

## API Endpoints
| Method | Endpoint         | Description              |
|--------|------------------|--------------------------|
| `GET`  | `/health-check`  | Health check for the API |
| `GET`  | `/chat   `       | Get response from agents |

## BTP Deployment

#### 1. Build project
```
mbt build
```

#### 2. Deploy project
```
cf deploy mta_archives/multi_agent_system_demo_1.0.0.mtar
```

## OOPs concepts 

| OOP Concept       | Usage         |
|-------------------|---------------|
| **Abstraction**   | `SuperAgent` defines a structure and hides implementation details using `@abstractmethod`. |
| **Inheritance**   | `WeatherAgent` extends `SuperAgent`, inheriting its common logic like `start_chat()`. |
| **Encapsulation** | Each agent’s internal behavior is hidden from the caller |
| **Polymorphism**  | `start_chat()` is generic and works with different agents that implement `create_ai_agents()`. |


## Why use FastAPI

| Feature                    | FastAPI                       | Flask                  |
|----------------------------|-------------------------------|------------------------|
| **Performance**            | ✅ Faster (ASGI-based)        | ❌ Slower (WSGI-based) |
| **Async Support**          | ✅ Built-in `async/await`     | ❌ Requires workarounds|                  
| **Auto Docs**              | ✅ Swagger & Redoc by default | ❌ Needs third-party  tools                        |
| **WebSockets**             | ✅ Fully supported            | ❌ Limited support     |
| **Data Validation**        | ✅ Automatic with Pydantic    | ❌ Manual validation required                     |
| **Production Ready**       | ✅ Scales well with Uvicorn & Gunicorn | ✅ Stable but synchronous                  |


## Formatting & Linting VS code plugins
- **Black** is used for auto-formatting.
- **Pylint** is configured for linting.
- **Rest Client** is configured for API testing.

## Agent Evaluation
1. Lets evaluate agents with the help of open telemetry.
2. Import below libraries
    ```
    poetry add opentelemetry-sdk
    poetry add opentelemetry-api
    poetry add opentelemetry-exporter-prometheus
    ```
3. The above libraries provide below features 
    - opentelemetry-api → API interface for traces and metrics.
    - opentelemetry-sdk → SDK for collecting and processing data.
    - opentelemetry-exporter-prometheus → Exporter to view metrics locally.   

4. Created a observability class - [agent_observability.py](/mas_autogen/app/utils/agent_observability.py)

5. Add decorator on the api endpoint in agent_service.py
    ```
    @router.post("/chat")
    @agent_observability.metric_decorator(endpoint="/chat")
    async def chat(request: ChatRequest):
    ...
    ...
    ```

## References
1. https://microsoft.github.io/autogen/0.2/docs/tutorial/introduction
2. https://microsoft.github.io/autogen/0.2/blog/2024/01/26/Custom-Models
3. https://github.com/microsoft/autogen/issues/2929


