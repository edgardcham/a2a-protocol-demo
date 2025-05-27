import random
from datetime import datetime
from typing import Any, Dict, List

from fastmcp import FastMCP

mcp = FastMCP("Travel Tools Server")

AIRLINES = [
    "Emirates",
    "Etihad",
    "Qatar Airways",
    "Air France",
    "Delta",
    "American Airlines",
    "United Airlines",
]

HOTEL_CHAINS = [
    "Marriott",
    "Hilton",
    "Hyatt",
    "InterContinental",
    "Four Seasons",
    "Sheraton",
    "Radisson",
    "Accor",
    "IHG",
]

HOTEL_TYPES = ["Hotel", "Resort", "Boutique Hotel", "Business Hotel"]


@mcp.tool()
def get_flights(
    origin: str, destination: str, start_date: str, end_date: str, budget: float
) -> List[Dict[str, Any]]:
    """
    Get flight options between two cities.

    Args:
        origin: Departure city
        destination: Arrival city
        start_date: Departure date (YYYY-MM-DD)
        end_date: Return date for round trip (YYYY-MM-DD)
        budget: Maximum budget for flights

    Returns:
        List of flight options with details
    """

    flights = []

    num_flights = 3

    for i in range(num_flights):
        airline = random.choice(AIRLINES)

        base_price = random.randint(200, 800)

        duration = random.uniform(2.0, 10.0)

        flight = {
            "name": f"{airline} {random.randint(100, 9999)}",
            "description": f"{airline} flight from {origin} to {destination}",
            "price_estimate": base_price,
            "duration_hours": round(duration, 1),
            "airline": airline,
        }

        flights.append(flight)

    flights.sort(key=lambda x: x["price_estimate"])
    return flights


@mcp.tool()
def get_stays(
    destination: str, check_in: str, check_out: str, budget: float = 2000
) -> List[Dict[str, Any]]:
    """
    Get stay options in a city.

    Args:
        destination: City to stay in
        check_in: Check-in date (YYYY-MM-DD)
        check_out: Check-out date (YYYY-MM-DD)
        budget: Maximum budget for stays

    Returns:
        List of stay options with details
    """
    checkin_date = datetime.strptime(check_in, "%Y-%m-%d")
    checkout_date = datetime.strptime(check_out, "%Y-%m-%d")
    nights = (checkout_date - checkin_date).days

    stays = []

    num_stays = 3

    for i in range(num_stays):
        hotel_chain = random.choice(HOTEL_CHAINS)
        hotel_type = random.choice(HOTEL_TYPES)

        nightly_rate = random.randint(80, 400)
        total_price = nightly_rate * nights

        stay = {
            "name": f"{hotel_chain} {destination} {hotel_type}",
            "description": f"Modern {hotel_type.lower()} in the heart of {destination}",
            "price_estimate": total_price,
            "duration_hours": nights * 24,
            "nights": nights,
        }

        stays.append(stay)

    stays.sort(key=lambda x: x["price_estimate"])
    return stays


# This is the key part - FastMCP needs to run when the script is executed
if __name__ == "__main__":
    mcp.run()
