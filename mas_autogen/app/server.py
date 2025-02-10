"""
server.py

This module starts FastAPI server for multi agent system.
Serves as an entry point for handling requests and routing
them to appropriate agents.
"""
import os
import json
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


@app.get("/zipcode")
async def get_zip_code(city: str):
    """Returns the zip code for the city.

    Arguments:
        city -- The city.

    Returns:
        The zip code.
    """
    zip_code = "30041"
    if city == "Atlanta":
        zip_code = "30041"
    if city == "New York":
        zip_code = "10012"

    response_dict = {"body": {"message": zip_code}}

    json_response = json.dumps(response_dict)

    return json_response


app.include_router(chat)

if __name__ == "__main__":
    import uvicorn

    if PORT is not None:
        uvicorn.run("server:app", host="0.0.0.0", port=int(PORT), reload=False)
    else:
        uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=False)
