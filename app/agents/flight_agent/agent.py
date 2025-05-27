import json

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()

flights_agent = Agent(
    name="flight_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Suggests flights for the user",
    instruction=(
        "Given a destination, dates, and budget, suggest a few flight options."
        "For each flight, provide a name, a short description, price estimate, and duration in hours"
        "Respond in plain English. Keep it concise and well-formatted."
    ),
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
    await session_service.create_session(
        app_name="flights_app",
        user_id=USER_ID,
        session_id=unique_session_id,
    )
    prompt = (
        f"User is flying to {request['destination']} from {request['start_date']} to {request['end_date']}."
        f"User has a budget of {request['budget']}. Suggest 2-3 flight options."
        f"Respond in JSON format using the key `flights` with a list of flight objects. "
        f"Each flight object must have exactly these fields: "
        f"'name' (string), 'description' (string), 'price_estimate' (number), 'duration_hours' (number)."
        f"Example: {{'flights': [{{'name': 'Air France Direct', 'description': 'Non-stop flight', 'price_estimate': 800, 'duration_hours': 8.5}}]}}"
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
                if "flights" in parsed and isinstance(parsed["flights"], list):
                    return {"flights": parsed["flights"]}
                else:
                    print("`flights` key missing or not a list in response JSON.")
                    return {"flights": response_text}  # fallback
            except json.JSONDecodeError as e:
                print("JSON parsing failed:", e)
                print("Response content:", response_text)
                return {"flights": response_text}  # fallback to raw text
