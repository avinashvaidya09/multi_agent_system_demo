# Multi-Agent System Demo

## Introduction
This project is my effort to demonstrate a **multi agent system** using **Microsoft AutoGen** for AI-driven automation. 

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

### 1. Install Poetry & Dependencies
```
poetry install
```

### 2. Activate Virtual Environment
```
poetry shell
```

### 3. Run FastAPI Server
```
cd mas_autogen/app

python server.py
```

## API Endpoints
| Method | Endpoint         | Description              |
|--------|------------------|--------------------------|
| `GET`  | `/health-check`  | Health check for the API |
| `GET`  | `/chat   `       | Get response from agents     |

## BTP Deployment

1. Build project
```
mbt build
```

2. Deploy project
```
cf deploy mta_archives/multi_agent_system_demo_1.0.0.mtar
```

## OOPs conecpts leveraged

| OOP Concept       | How It’s Used |
|-------------------|---------------|
| **Abstraction**   | `AgentFramework` defines a structure and hides implementation details using `@abstractmethod`. |
| **Inheritance**   | `WeatherAgent` extends `AgentFramework`, inheriting its common logic like `start_chat()`. |
| **Encapsulation** | Each agent’s internal behavior is hidden from the caller. |
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


## References
1. https://microsoft.github.io/autogen/0.2/docs/tutorial/introduction
2. https://microsoft.github.io/autogen/0.2/blog/2024/01/26/Custom-Models
3. https://github.com/microsoft/autogen/issues/2929


