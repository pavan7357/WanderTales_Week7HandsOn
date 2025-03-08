
import os

# ✅ Check if all necessary files exist
required_files = ["config.py", "utils.py", "travel_story.py", "app.py"]
missing_files = [file for file in required_files if not os.path.exists(file)]

if missing_files:
    print(f"❌ ERROR: Missing files: {missing_files}. Ensure all required files are present.")
else:
    print("✅ All necessary files exist.")

# ✅ Verify `config.py` imports
try:
    from config import google_maps_api_key, serpapi_key, weather_api_key
    print("✅ Successfully imported API keys from config.py")
    print(f"Google Maps API Key: {google_maps_api_key[:5]}******")
    print(f"SerpAPI Key: {serpapi_key[:5]}******")
    print(f"Weather API Key: {weather_api_key[:5]}******")
except ModuleNotFoundError:
    print("❌ ERROR: 'config.py' not found.")
except ImportError:
    print("❌ ERROR: Could not import variables from 'config.py'.")

# ✅ Verify `utils.py` imports
try:
    from utils import get_lat_lng, fetch_restaurants, fetch_weather
    print("✅ Successfully imported functions from utils.py")
    print(f"get_lat_lng function exists: {callable(get_lat_lng)}")
    print(f"fetch_restaurants function exists: {callable(fetch_restaurants)}")
    print(f"fetch_weather function exists: {callable(fetch_weather)}")
except ModuleNotFoundError:
    print("❌ ERROR: 'utils.py' not found.")
except ImportError:
    print("❌ ERROR: Could not import functions from 'utils.py'.")

# ✅ Verify `purpose.py` imports
try:
    from travel_story import generate_travel_story, generate_voiceover, create_travel_video
    print("✅ Successfully imported functions from purpose.py")
    print(f"generate_travel_story function exists: {callable(generate_travel_story)}")
    print(f"generate_voiceover function exists: {callable(generate_voiceover)}")
    print(f"create_travel_video function exists: {callable(create_travel_video)}")
except ModuleNotFoundError:
    print("❌ ERROR: 'purpose.py' not found.")
except ImportError:
    print("❌ ERROR: Could not import functions from 'purpose.py'.")

# ✅ Verify `app.py` existence
if os.path.exists("app.py"):
    print("✅ 'app.py' exists and is ready to run.")
else:
    print("❌ ERROR: 'app.py' is missing.")
