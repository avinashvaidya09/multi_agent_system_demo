# Multi Agent System Demo

## Introduction
This project is my effort to demonstrate a **Agentic AI** using **Microsoft AutoGen** for AI-driven intelligence. 
In this project you will learn

1. Create autonomous agents using LLMs and functions
2. Integrate with custom LLM models
3. Leverage APIs and LLMs as tools
4. Create multi agent systems
5. Expose multi agent systems as REST APIs

As part of this project you will also learn

1. A clean python project structure
2. Leveraging Python OOP and structural programming paradigms.
3. Why use FAST API?

Note: 
- Persisting chat history is not implemented as part of this project.
- Agentic REST API is not authenticated [not recommended in production scenarios]

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

#### 2. Create your own .env file and add the value for the below properties.
```
WEATHER_API_URL: https://api.weatherapi.com/v1/current.json
OPENAI_API_KEY: <OPENAI_API_KEY>
WEATHER_API_KEY: <WEATHER_API_KEY>
AICORE_AUTH_URL: <AICORE_AUTH_URL>
AICORE_CLIENT_ID: <AICORE_CLIENT_ID>
AICORE_CLIENT_SECRET: <AICORE_CLIENT_SECRET>
AICORE_RESOURCE_GROUP: default
AICORE_BASE_URL: <AICORE_BASE_URL>
```
- If you are using OPENAI API you have to update the LLM configuration accordingly. I have kept the key attribute here but as I am using custom model, I am not using it.
- If you are using AICORE client as custom model, you have to update the AICORE properties required by generative AI hub sdk.

#### 3. Install Poetry & Dependencies
```
poetry install
```

#### 4. Activate Virtual Environment
```
poetry shell
```

#### 5. Run FastAPI Server
```
cd mas_autogen/app && python server.py
```

#### 6. Test your application

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


## References
1. https://microsoft.github.io/autogen/0.2/docs/tutorial/introduction
2. https://microsoft.github.io/autogen/0.2/blog/2024/01/26/Custom-Models
3. https://github.com/microsoft/autogen/issues/2929


