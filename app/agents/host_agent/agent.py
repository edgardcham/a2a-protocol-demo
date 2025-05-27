from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()


host_agent = Agent(
    name="host_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Coordinates travel planning by calling flight, stay and activity agents.",
    instruction=(
        "You are the host agent responsible for orchestrating trip planning tasks."
        "You call external agents to gather flights, stays and activities, then return a final result"
    ),
)

session_service = InMemorySessionService()

runner = Runner(agent=host_agent, app_name="host_app", session_service=session_service)

USER_ID = "user_host"
SESSION_ID = "session_host"


async def execute(request):
    # Create a unique session for each request
    import uuid

    unique_session_id = f"{SESSION_ID}_{uuid.uuid4().hex[:8]}"
    await session_service.create_session(
        app_name="host_app",
        user_id=USER_ID,
        session_id=unique_session_id,
    )
    prompt = (
        f"Plan a trip to {request['destination']} from {request['start_date']} to {request['end_date']}"
        f"within a total budget of {request['budget']}. Call the flights, stays and activities agents for results."
    )

    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    async for event in runner.run_async(
        user_id=USER_ID, session_id=unique_session_id, new_message=message
    ):
        if event.is_final_response():
            return {"summary": event.content.parts[0].text}
