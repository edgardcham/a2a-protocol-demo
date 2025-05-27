import json

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()

activities_agent = Agent(
    name="activities_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Suggests interesting activities for the user at a destination",
    instruction=(
        "Given a destination, dates, and budget, suggest a few engaging tourist or cultural activities."
        "For each activity, provide a name, a short description, price estimate, and duration in hours"
        "Respond in plain English. Keep it concise and well-formatted."
    ),
)

session_service = InMemorySessionService()

runner = Runner(
    agent=activities_agent,
    app_name="activities_app",
    session_service=session_service,
)

USER_ID = "user_activities"
SESSION_ID = "session_activities"


async def execute(request):
    # Create a unique session for each request
    import uuid

    unique_session_id = f"{SESSION_ID}_{uuid.uuid4().hex[:8]}"
    await session_service.create_session(
        app_name="activities_app",
        user_id=USER_ID,
        session_id=unique_session_id,
    )
    prompt = (
        f"User is visiting {request['destination']} from {request['start_date']} to {request['end_date']}."
        f"User has a budget of {request['budget']}. Suggest 2-3 engaging tourist or cultural activities."
        f"Respond in JSON format using the key `activities` with a list of activity objects. "
        f"Each activity object must have exactly these fields: "
        f"'name' (string), 'description' (string), 'price_estimate' (number), 'duration_hours' (number)."
        f"Example: {{'activities': [{{'name': 'Eiffel Tower Tour', 'description': 'Visit the iconic tower', 'price_estimate': 25, 'duration_hours': 2.5}}]}}"
    )

    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    async for event in runner.run_async(
        user_id=USER_ID, session_id=unique_session_id, new_message=message
    ):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            try:
                # Remove markdown code blocks if present
                if response_text.startswith("```json"):
                    response_text = (
                        response_text.replace("```json", "").replace("```", "").strip()
                    )
                elif response_text.startswith("```"):
                    response_text = response_text.replace("```", "").strip()

                parsed = json.loads(response_text)
                if "activities" in parsed and isinstance(parsed["activities"], list):
                    return {"activities": parsed["activities"]}
                else:
                    print("`activities` key missing or not a list in response JSON.")
                    return {"activities": response_text}  # fallback
            except json.JSONDecodeError as e:
                print("JSON parsing failed:", e)
                print("Response content:", response_text)
                return {"activities": response_text}  # fallback to raw text
