from typing import Any, Dict

from fastapi import FastAPI
from google.adk.agents import Agent


def create_app(agent: Agent):
    app = FastAPI()

    @app.post("/run")
    async def run(payload: Dict[str, Any]):
        return await agent.execute(payload)

    return app
