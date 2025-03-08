
import requests
from config import google_maps_api_key, weather_api_key, amadeus_api_key, amadeus_api_secret

# ✅ Function to fetch latitude & longitude
def get_lat_lng(location):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": location, "key": google_maps_api_key}
    response = requests.get(url, params=params).json()
    if "results" in response and response["results"]:
        location_data = response["results"][0]["geometry"]["location"]
        return location_data["lat"], location_data["lng"]
    return None, None

# ✅ Function to fetch top tourist attractions dynamically
def fetch_tourist_attractions(location, top_n=5):
    lat, lng = get_lat_lng(location)
    if not lat or not lng:
        return "Could not determine the exact location."

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {"location": f"{lat},{lng}", "radius": 10000, "type": "tourist_attraction", "key": google_maps_api_key}

    response = requests.get(url, params=params).json()
    if "results" in response:
        return "\n".join(
            [f"🏛 {t['name']} ({t.get('rating', 'No rating')}⭐)" for t in response["results"][:top_n]]
        )
    return "No tourist attractions found."



# ✅ Function to fetch restaurants dynamically
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
    params = {"location": f"{lat},{lng}", "radius": 5000, "type": "restaurant", "keyword": keyword, "key": google_maps_api_key}
    
    response = requests.get(url, params=params).json()
    if "results" in response:
        return "\n".join(
            [f"🍽 {r['name']} ({r.get('rating', 'No rating')}⭐)" for r in response["results"][:top_n]]
        )
    return "No restaurants found."

# ✅ Function to fetch real-time weather details
def fetch_weather(city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": weather_api_key, "units": "metric"}
    response = requests.get(url, params=params).json()
    if "weather" in response and "main" in response:
        return f"🌤 {response['weather'][0]['description'].capitalize()}, {response['main']['temp']}°C"
    return "Weather data not available."

# ✅ Function to fetch 7-day weather forecast
def fetch_weather_forecast(city):
    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": weather_api_key, "units": "metric"}
    response = requests.get(url, params=params).json()
    
    if "list" in response:
        forecast_data = response["list"][:7]
        forecast = "\n".join(
            [f"📅 {entry['dt_txt']} - {entry['weather'][0]['description'].capitalize()}, {entry['main']['temp']}°C"
             for entry in forecast_data]
        )
        return forecast
    return "Weather forecast data not available."


# ✅ Function to fetch flight details with improved error handling
def fetch_flight_details(origin, destination, departure_date):
    try:
        response = requests.get(f"https://api.flightapi.com/{origin}/{destination}/{departure_date}", headers={"API-Key": amadeus_api_key})
        if response.status_code == 200:
            return response.json()
        return "Flight details unavailable. Please try again later."
    except Exception as e:
        return f"Error retrieving flight details: {str(e)}"

# ✅ Function to fetch a destination image with fallback options
def fetch_destination_image(destination):
    image_sources = [
        f"https://source.unsplash.com/600x400/?{destination}",
        f"https://source.unsplash.com/600x400/?travel,{destination}"
    ]
    
    for url in image_sources:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            return url
    return "Image unavailable. Please try again later."

# ✅ Function to fetch nearby hotels dynamically
def fetch_hotels(location, top_n=5):
    lat, lng = get_lat_lng(location)
    if not lat or not lng:
        return "Could not determine the exact location."

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {"location": f"{lat},{lng}", "radius": 5000, "type": "lodging", "key": google_maps_api_key}

    response = requests.get(url, params=params).json()
    if "results" in response:
        return "\n".join(
            [f"🏨 {h['name']} ({h.get('rating', 'No rating')}⭐)" for h in response["results"][:top_n]]
        )
    return "No hotels found."

# ✅ Function to fetch live currency exchange rate
def fetch_currency_exchange_rate(base_currency, target_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url).json()
    if "rates" in response and target_currency in response["rates"]:
        return f"💰 1 {base_currency} = {response['rates'][target_currency]} {target_currency}"
    return "Exchange rate data not available."

# ✅ Function to fetch top travel news & insights
def fetch_travel_news():
    url = "https://serpapi.com/search.json"
    params = {"q": "latest travel trends", "api_key": google_maps_api_key}
    response = requests.get(url, params=params).json()
    
    if "organic_results" in response:
        return "\n".join(
            [f"📰 {article['title']} - {article['link']}" for article in response["organic_results"][:5]]
        )
    return "No travel news available."

