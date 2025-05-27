import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from common.a2a_client import call_agent

FLIGHT_URL = "http://localhost:8001/run"
STAY_URL = "http://localhost:8002/run"
ACTIVITIES_URL = "http://localhost:8003/run"


async def run(payload):
    # Print what the host agent is sending
    print("Incoming payload:", payload)

    print("Calling flight agent...")
    flights = await call_agent(FLIGHT_URL, payload)
    print("Flight agent response received")

    print("Calling stay agent...")
    try:
        stay = await call_agent(STAY_URL, payload)
        print("Stay agent response received")
    except Exception as e:
        print(f"Stay agent failed: {e}")
        stay = {}

    print("Calling activities agent...")
    activities = await call_agent(ACTIVITIES_URL, payload)
    print("Activities agent response received")

    # Log outputs
    print("flights:", flights)
    print("stay:", stay)
    print("activities:", activities)

    # Ensure all are dicts
    flights = flights if isinstance(flights, dict) else {}
    stay = stay if isinstance(stay, dict) else {}
    activities = activities if isinstance(activities, dict) else {}

    return {
        "flights": flights.get("flights", "No flights returned."),
        "stays": stay.get("stays", "No stays returned."),
        "activities": activities.get("activities", "No activities returned."),
    }
