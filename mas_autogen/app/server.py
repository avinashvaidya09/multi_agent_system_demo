"""
server.py

This module starts FastAPI server for multi agent system.
Serves as an entry point for handling requests and routing
them to appropriate agents.
"""
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from mas_autogen.app.utils.config import load_environment_variables
from mas_autogen.app.services.agent_service import router as chat

# Load environment variables
load_environment_variables()

PORT = os.getenv("PORT")

app = FastAPI()


@app.get("/")
async def health_check():
    """
    Health check api for the multi agent system.

    Returns:
        JSONResponse: JSON response with a message.
    """
    return JSONResponse(
        content={"message": "Hello Again! Your Multi Agent System is up and running"}
    )

app.include_router(chat)

if __name__ == "__main__":
    import uvicorn

    if PORT is not None:
        uvicorn.run("server:app", host="0.0.0.0", port=int(PORT), reload=False)
    else:
        uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=False)
