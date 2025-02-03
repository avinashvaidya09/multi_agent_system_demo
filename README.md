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
python server.py
```

## API Endpoints
| Method | Endpoint         | Description              |
|--------|------------------|--------------------------|
| `GET`  | `/health-check`  | Health check for the API |
| `GET`  | `/chat   `       | Get response from agents     |

## Summary of OOP Features Used
# Multi-Agent System - Overview

This project implements a multi-agent system using AutoGen, following Object-Oriented Programming (OOP) principles to make the system scalable and maintainable.

## Object-Oriented Features Used

| OOP Concept       | How It’s Used |
|-------------------|---------------|
| **Abstraction**   | `AgentFramework` defines a structure but hides implementation details using `@abstractmethod`. |
| **Inheritance**   | `WeatherAgent` extends `AgentFramework`, inheriting its common logic like `start_chat()`. |
| **Encapsulation** | Each agent’s internal behavior is hidden. |
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


## Formatting & Linting
- **Black** is used for auto-formatting.
- **Pylint** is configured for linting.
- Run autoformatting manually using:


## Next Steps
- Implement AI-driven Weather & Finance agents.
- Add structured logging using `loguru`.
- Secure endpoints with authentication.

---
🚀 **Project ready for further AI integration!**

