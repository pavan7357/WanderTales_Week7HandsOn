
import requests
from config import GOOGLE_MAPS_API_KEY, WEATHER_API_KEY, AMADEUS_API_KEY

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

# ✅ Function to fetch flight details
def fetch_flight_details(origin, destination, departure_date):
    try:
        response = requests.get(f"https://api.flightapi.com/{origin}/{destination}/{departure_date}", headers={"API-Key": AMADEUS_API_KEY})
        if response.status_code == 200:
            return response.json()
        return "Flight details unavailable. Please try again later."
    except Exception as e:
        return f"Error retrieving flight details: {str(e)}"

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
