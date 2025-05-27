import json
import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.genai import types

load_dotenv()

# Get the absolute path to the MCP server
MCP_SERVER_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "mcp", "server.py")
)

flights_agent = Agent(
    name="flight_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Suggests flights for the user using real flight data tools",
    instruction=(
        "You are a flight specialist agent. Use the get_flights tool to find real flight options "
        "for the user's travel request. Always call the get_flights tool with the provided parameters. "
        "The tool will return a JSON array of flight objects. Return ONLY valid JSON with double quotes, "
        'formatted as: {"flights": [flight_objects]}. Do not use single quotes or Python dict syntax. '
        "Do not add any explanatory text or commentary."
    ),
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command="python3",
                args=[MCP_SERVER_PATH],
            ),
            tool_filter=["get_flights"],  # Only expose the flights tool
        )
    ],
)

session_service = InMemorySessionService()

runner = Runner(
    agent=flights_agent,
    app_name="flights_app",
    session_service=session_service,
)

USER_ID = "user_flights"
SESSION_ID = "session_flights"


async def execute(request):
    # Create a unique session for each request
    import uuid

    unique_session_id = f"{SESSION_ID}_{uuid.uuid4().hex[:8]}"
    try:
        await session_service.create_session(
            app_name="flights_app",
            user_id=USER_ID,
            session_id=unique_session_id,
        )
    except Exception as e:
        print(f"Session creation failed: {e}")

    # Create a prompt that instructs the agent to use the MCP tool
    prompt = (
        f"Find flight options from {request.get('origin', 'unknown')} to {request['destination']} "
        f"departing on {request['start_date']} and returning on {request['end_date']} "
        f"with a budget of ${request['budget']}. "
        f"Use the get_flights tool with these exact parameters: "
        f"origin='{request.get('origin', 'unknown')}', destination='{request['destination']}', "
        f"start_date='{request['start_date']}', end_date='{request['end_date']}', budget={request['budget']}. "
        f"Return ONLY valid JSON with double quotes in this exact format: "
        f'{{"flights": [array_from_tool]}}. '
        f"Do not include any explanatory text, just the JSON data with double quotes."
    )

    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    async for event in runner.run_async(
        user_id=USER_ID, session_id=unique_session_id, new_message=message
    ):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            print(f"Flight agent raw response: {response_text}")

            try:
                # Remove markdown code blocks if present
                if response_text.startswith("```json"):
                    response_text = (
                        response_text.replace("```json", "").replace("```", "").strip()
                    )
                elif response_text.startswith("```"):
                    response_text = response_text.replace("```", "").strip()

                # Fix single quotes to double quotes for JSON parsing
                response_text = response_text.replace("'", '"')

                # Try to parse as JSON first
                parsed = json.loads(response_text)
                if "flights" in parsed and isinstance(parsed["flights"], list):
                    print(f"Returning parsed flights: {len(parsed['flights'])} items")
                    return {"flights": parsed["flights"]}
                else:
                    print("`flights` key missing or not a list in response JSON.")
                    # Fallback: try to extract JSON from the response
                    import re

                    json_match = re.search(r"\[.*\]", response_text, re.DOTALL)
                    if json_match:
                        flights_array = json.loads(json_match.group())
                        print(f"Extracted flights array: {len(flights_array)} items")
                        return {"flights": flights_array}
                    return {"flights": []}  # Return empty array as fallback

            except json.JSONDecodeError as e:
                print("JSON parsing failed:", e)
                print("Response content:", response_text)

                # Try to extract JSON array from the response text
                import re

                json_match = re.search(r"\[.*\]", response_text, re.DOTALL)
                if json_match:
                    try:
                        # Fix single quotes in the extracted JSON
                        json_text = json_match.group().replace("'", '"')
                        flights_array = json.loads(json_text)
                        print(
                            f"Extracted flights array from text: {len(flights_array)} items"
                        )
                        return {"flights": flights_array}
                    except:
                        pass

                return {"flights": []}  # Return empty array as final fallback
