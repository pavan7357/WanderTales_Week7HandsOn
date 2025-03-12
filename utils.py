
import requests
from config import OPENAI_API_KEY, GOOGLE_MAPS_API_KEY, WEATHER_API_KEY, AMADEUS_API_KEY, AMADEUS_API_SECRET, llm
from amadeus import Client, ResponseError
import os
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage 
import re

amadeus = Client(client_id=AMADEUS_API_KEY, client_secret=AMADEUS_API_SECRET)

# ✅ Function to fetch latitude & longitude
def get_lat_lng(location):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": location, "key": GOOGLE_MAPS_API_KEY}
    response = requests.get(url, params=params).json()
    if "results" in response and response["results"]:
        location_data = response["results"][0]["geometry"]["location"]
        return location_data["lat"], location_data["lng"]
    return None, None

# ✅ Function to fetch tourist attractions
def fetch_tourist_attractions(location, top_n=5):
    lat, lng = get_lat_lng(location)
    if not lat or not lng:
        return "Could not determine the exact location."

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {"location": f"{lat},{lng}", "radius": 10000, "type": "tourist_attraction", "key": GOOGLE_MAPS_API_KEY}

    response = requests.get(url, params=params).json()
    if "results" in response:
        return [f"{t['name']} ({t.get('rating', 'No rating')}⭐)" for t in response["results"][:top_n]]
    return "No tourist attractions found."

# ✅ Function to fetch restaurants
def fetch_restaurants(location, purpose, top_n=5):
    lat, lng = get_lat_lng(location)
    if not lat or not lng:
        return "Could not determine the exact location."

    keyword = {
        "Leisure": "casual dining",
        "Business": "fine dining",
        "Family": "family-friendly",
        "Adventure": "unique cuisine",
        "Romantic": "romantic restaurant"
    }.get(purpose, "restaurant")

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {"location": f"{lat},{lng}", "radius": 5000, "type": "restaurant", "keyword": keyword, "key": GOOGLE_MAPS_API_KEY}

    response = requests.get(url, params=params).json()
    if "results" in response:
        return [f"{r['name']} ({r.get('rating', 'No rating')}⭐)" for r in response["results"][:top_n]]
    return "No restaurants found."

# ✅ Function to fetch real-time weather details
def fetch_weather(city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
    response = requests.get(url, params=params).json()
    if "weather" in response and "main" in response:
        return f"{response['weather'][0]['description'].capitalize()}, {response['main']['temp']}°C"
    return "Weather data not available."

def get_airport_code(city_name):
    """
    Convert a city name to an airport code using the Amadeus API.
    """
    try:
        response = amadeus.reference_data.locations.get(
            keyword=city_name,
            subType='AIRPORT'
        )
        # Extract the airport code from the response
        for location in response.data:
            if location['subType'] == 'AIRPORT':
                return location['iataCode']
        return None
    except ResponseError as error:
        print(f"Error fetching airport code for {city_name}: {error}")
        return None


# Helper Function to get full airline names from its codes using OpenAI
def get_airline_full_name(airline_code):
    prompt = f"Please provide only the full name for the airline '{airline_code}'."
    response = llm([HumanMessage(content=prompt)])
    return response.content.strip() if response else airline_code  # Return the code if response is empty

def format_duration(iso_duration):
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?', iso_duration)
    hours = match.group(1) if match.group(1) else "0"
    minutes = match.group(2) if match.group(2) else "0"
    return f"{int(hours)} hours {int(minutes)} minutes"

# Function to fetch Flights information
def fetch_flight_details(origin, destination, start_data, return_date=None, max_price=None, airline_name =None):
    try:
        origin_code = get_airport_code(origin)
        destination_code = get_airport_code(destination)
        # Set a high default max_price if not provided
        max_price = max_price if max_price else 20000
        params = {
            "originLocationCode": origin_code,
            "destinationLocationCode": destination_code,
            "departureDate": start_data,
            "adults": 1,
            "maxPrice": max_price
        }

        if return_date:
            params["returnDate"] = return_date  # Include return date for round-trip flights

        # Fetch flights from Amadeus API
        response = amadeus.shopping.flight_offers_search.get(**params)
        flights = response.data

        if flights:
            result = []
            for flight in flights[:5]:  # Limit to top 5 results
                if float(flight['price']['total']) <= max_price:
                    # Outbound flight details
                    segments = flight['itineraries'][0]['segments']
                    airline_code = segments[0]['carrierCode']
                    airline = get_airline_full_name(airline_code)  # Get full airline name
                    # Only add flights that match the specified airline, if provided
                    if airline_name and airline and airline.lower() not in airline_name.lower():
                        continue
                    departure_time = segments[0]['departure']['at']
                    arrival_time = segments[-1]['arrival']['at']
                    flight_duration = format_duration(flight['itineraries'][0]['duration'])

                    # Only include return details if a return date is provided
                    if return_date and len(flight['itineraries']) > 1:
                        return_segments = flight['itineraries'][1]['segments']
                        return_departure_time = return_segments[0]['departure']['at']
                        return_arrival_time = return_segments[-1]['arrival']['at']
                        return_duration = format_duration(flight['itineraries'][1]['duration'])
                        return_info = (
                            f"\nReturn Departure: {return_departure_time}\n"
                            f"Return Arrival: {return_arrival_time}\n"
                            f"Return Duration: {return_duration}\n"
                        )
                    else:
                        return_info = ""

                    # Append both outbound and return information (if available) to results
                    result.append(
                        f"Airline: {airline}\nPrice: ${flight['price']['total']}\n"
                        f"Departure: {departure_time}\nArrival: {arrival_time}\n"
                        f"Duration: {flight_duration}{return_info}"
                        "\n----------------------------------------"
                    )
            return "\n\n".join(result) if result else "No flights found within the budget."
        return "No flights found."
    except ResponseError as error:
        return f"An error occurred: {error.response.result}"

# ✅ Function to fetch hotels
def fetch_hotels(location, top_n=5):
    lat, lng = get_lat_lng(location)
    if not lat or not lng:
        return "Could not determine the exact location."

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {"location": f"{lat},{lng}", "radius": 5000, "type": "lodging", "key": GOOGLE_MAPS_API_KEY}

    response = requests.get(url, params=params).json()
    if "results" in response:
        return [f"{h['name']} ({h.get('rating', 'No rating')}⭐)" for h in response["results"][:top_n]]
    return "No hotels found."

