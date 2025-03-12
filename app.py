import streamlit as st
from travel_story import generate_travel_story, generate_voiceover, create_travel_video, generate_travel_plan, generate_travel_images
from utils import fetch_weather, fetch_tourist_attractions, fetch_flight_details, fetch_restaurants, fetch_hotels
import requests
from PIL import Image
from io import BytesIO
from moviepy.editor import AudioFileClip

# ✅ Set up Streamlit Page
st.set_page_config(page_title="✈️ AI Travel Planner", layout="wide")

st.title("✈️ AI Travel Planner 🏨")

# ✅ Sidebar Inputs
st.sidebar.title("Plan Your Trip 🗺")
origin = st.sidebar.text_input("Enter Origin City", "New York")  # ✅ Added Origin
destination = st.sidebar.text_input("Enter Destination", "Paris")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
purpose = st.sidebar.selectbox("Purpose of Visit", ["Leisure", "Business", "Adventure", "Romantic", "Family"])

# ✅ Generate Travel Plan & Fetch Details
if st.sidebar.button("Generate Travel Plan & Details"):
    with st.spinner("🔄 Generating AI travel plan & fetching details..."):
        travel_plan_text = generate_travel_plan(origin, destination, start_date, end_date, purpose)  # ✅ Pass Origin
        weather_info = fetch_weather(destination)
        tourist_attractions = fetch_tourist_attractions(destination)
        restaurants = fetch_restaurants(destination, purpose)
        hotels = fetch_hotels(destination)
        flights = fetch_flight_details(origin, destination, start_date, return_date=None, max_price=None, airline_name =None)  # ✅ Pass Origin

    st.subheader("📅 Your AI-Generated Travel Plan")
    st.write(travel_plan_text)
    
    st.subheader(f"🌦 Weather Forecast in {destination}")
    st.write(weather_info)
    
    st.subheader(f"🏛 Top Attractions in {destination}")
    st.write(tourist_attractions)
    
    st.subheader(f"🍽 Best Restaurants in {destination}")
    st.write(restaurants)
    
    st.subheader(f"🏨 Recommended Hotels in {destination}")
    st.write(hotels)
    
    st.subheader(f"✈️ Flights from {origin} to {destination}")
    st.write(flights)

# ✅ Generate Travel Story & Voiceover
if st.sidebar.button("Generate Story & Voiceover"):
    with st.spinner("🔄 Generating AI travel story..."):
        travel_story_text = generate_travel_story(origin, destination, purpose, start_date, end_date)  # ✅ Pass Origin
        narration_audio = generate_voiceover(travel_story_text)

    st.subheader("📖 Your AI-Generated Travel Story")
    st.write(travel_story_text)
    
    st.subheader("🎤 AI Voiceover")
    st.audio(narration_audio)

# ✅ Generate Images & Video
if st.sidebar.button("Generate Images & Video"):
    with st.spinner("🖼 Generating Travel Images..."):
        travel_images = generate_travel_images(destination, purpose)
    
    st.subheader("🖼 View Destination Images")
    if travel_images:
        for image_url in travel_images:
            response = requests.get(image_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                st.image(image, caption=f"A view of {destination}", use_container_width=True)
            else:
                st.warning("❌ Unable to fetch image. Try again later.")
    else:
        st.warning("❌ No images generated.")

    with st.spinner("🎥 Creating AI Travel Video..."):
        travel_story_text = generate_travel_story(origin, destination, purpose, start_date, end_date)  # ✅ Pass Origin
        narration_audio = generate_voiceover(travel_story_text)
        travel_video = create_travel_video(travel_images, narration_audio)
    
    st.subheader("🎥 AI-Generated Travel Video")
    if travel_video:
        st.video(travel_video)
    else:
        st.warning("❌ Video generation failed.")

st.success("✅ AI Travel Planner is ready!")
