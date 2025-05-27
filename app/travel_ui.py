import requests
import streamlit as st

st.set_page_config(page_title="ADK-Powered Travel Planner", page_icon="✈️")
st.title("🌍 ADK-Powered Travel Planner")
origin = st.text_input("Where are you flying from?", placeholder="e.g., New York")
destination = st.text_input("Destination", placeholder="e.g., Paris")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
budget = st.number_input("Budget (in USD)", min_value=100, step=50)
if st.button("Plan My Trip ✨"):
    if not all([origin, destination, start_date, end_date, budget]):
        st.warning("Please fill in all the details.")
    else:
        payload = {
            "origin": origin,
            "destination": destination,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "budget": budget,
        }
        response = requests.post("http://localhost:8000/run", json=payload)
        if response.ok:
            data = response.json()

            # Display Flights
            st.subheader("✈️ Flights")
            flights_data = data.get("flights", "No flights returned.")
            if isinstance(flights_data, list):
                for flight in flights_data:
                    st.write(f"**{flight['name']}** - ${flight['price_estimate']}")
                    st.write(f"_{flight['description']}_")
                    duration = flight.get("duration_hours", "N/A")
                    st.write(f"Duration: {duration} hours")
                    st.write("---")
            else:
                st.markdown(flights_data)

            # Display Stays
            st.subheader("🏨 Stays")
            stays_data = data.get("stays", "No stays returned.")
            if isinstance(stays_data, list):
                for stay in stays_data:
                    st.write(f"**{stay['name']}** - ${stay['price_estimate']}")
                    st.write(f"_{stay['description']}_")
                    duration = stay.get("duration_hours", "N/A")
                    st.write(f"Duration: {duration} hours")
                    st.write("---")
            else:
                st.markdown(stays_data)

            # Display Activities
            st.subheader("🗺️ Activities")
            activities_data = data.get("activities", "No activities returned.")
            if isinstance(activities_data, list):
                for activity in activities_data:
                    st.write(f"**{activity['name']}** - ${activity['price_estimate']}")
                    st.write(f"_{activity['description']}_")
                    duration = activity.get("duration_hours", "N/A")
                    st.write(f"Duration: {duration} hours")
                    st.write("---")
            else:
                st.markdown(activities_data)
        else:
            st.error("Failed to fetch travel plan. Please try again.")
