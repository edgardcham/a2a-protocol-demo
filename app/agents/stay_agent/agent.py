import json

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()


stays_agent = Agent(
    name="stay_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Suggests stays for the user",
    instruction=(
        "Given a destination, dates, and budget, suggest a few stay options."
        "For each stay, provide a name, a short description, price estimate, and duration in hours"
        "Respond in plain English. Keep it concise and well-formatted."
    ),
)

session_service = InMemorySessionService()

runner = Runner(
    agent=stays_agent,
    app_name="stays_app",
    session_service=session_service,
)

USER_ID = "user_stays"
SESSION_ID = "session_stays"


async def execute(request):
    # Create a unique session for each request
    import uuid

    unique_session_id = f"{SESSION_ID}_{uuid.uuid4().hex[:8]}"
    await session_service.create_session(
        app_name="stays_app",
        user_id=USER_ID,
        session_id=unique_session_id,
    )
    prompt = (
        f"User is staying in {request['destination']} from {request['start_date']} to {request['end_date']}."
        f"User has a budget of {request['budget']}. Suggest 2-3 accommodation options."
        f"Respond in JSON format using the key `stays` with a list of stay objects. "
        f"Each stay object must have exactly these fields: "
        f"'name' (string), 'description' (string), 'price_estimate' (number), 'duration_hours' (number - total hours for the entire stay)."
        f"Example: {{'stays': [{{'name': 'Hotel Paris', 'description': 'Luxury hotel in city center', 'price_estimate': 1200, 'duration_hours': 144}}]}}"
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
                if "stays" in parsed and isinstance(parsed["stays"], list):
                    return {"stays": parsed["stays"]}
                else:
                    print("`stays` key missing or not a list in response JSON.")
                    return {"stays": response_text}  # fallback
            except json.JSONDecodeError as e:
                print("JSON parsing failed:", e)
                print("Response content:", response_text)
                return {"stays": response_text}  # fallback to raw text
