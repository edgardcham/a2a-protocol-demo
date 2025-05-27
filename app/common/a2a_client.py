from typing import Any, Dict

import httpx


async def call_agent(url: str, payload: Dict[str, Any]):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, timeout=60.0)
        response.raise_for_status()
        return response.json()
