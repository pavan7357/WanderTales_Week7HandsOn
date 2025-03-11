import streamlit as st
from travel_story import generate_travel_story, generate_voiceover, create_travel_video, generate_travel_plan, generate_travel_images
from utils import fetch_weather, fetch_tourist_attractions, fetch_flight_details, fetch_restaurants, fetch_hotels
import requests
from PIL import Image
from io import BytesIO
from moviepy.editor import *

st.set_page_config(page_title="✈️ AI Travel Planner", layout="wide")

st.title("✈️ AI Travel Planner 🏨")

st.sidebar.title("Plan Your Trip 🗺")
destination = st.sidebar.text_input("Enter Destination", "Paris")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
purpose = st.sidebar.selectbox("Purpose of Visit", ["Leisure", "Business", "Adventure", "Romantic", "Family"])

if st.sidebar.button("Generate Travel Plan & Details"):
    with st.spinner("🔄 Generating AI travel plan & fetching details..."):
        travel_plan_text = generate_travel_plan(destination, start_date, end_date, purpose)
        weather_info = fetch_weather(destination)
        tourist_attractions = fetch_tourist_attractions(destination)
        restaurants = fetch_restaurants(destination, purpose)
        hotels = fetch_hotels(destination)
        flights = fetch_flight_details("JFK", destination, start_date)
    
    st.subheader("📅 Your AI-Generated Travel Plan")
    st.write(travel_plan_text)
    
    st.subheader("🌦 Weather Forecast")
    st.write(weather_info)
    
    st.subheader("🏛 Tourist Attractions")
    st.write(tourist_attractions)
    
    st.subheader("🍽 Recommended Restaurants")
    st.write(restaurants)
    
    st.subheader("🏨 Hotel Recommendations")
    st.write(hotels)
    
    st.subheader("✈️ Flight Details")
    st.write(flights)

if st.sidebar.button("Generate Story & Voiceover"):
    with st.spinner("🔄 Generating AI travel story..."):
        travel_story_text = generate_travel_story(destination, start_date, end_date, purpose)
        narration_audio = generate_voiceover(travel_story_text)
    
    st.subheader("📖 Your AI-Generated Travel Story")
    st.write(travel_story_text)
    
    st.subheader("🎤 AI Voiceover")
    st.audio(narration_audio)

if st.sidebar.button("Generate Images & Video"):
    with st.spinner("🖼 Generating Travel Images..."):
        travel_images = generate_travel_images(destination, purpose)
    
    st.subheader("🖼 View Destination Images")
    if travel_images:
        for image_url in travel_images:
            response = requests.get(image_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                st.image(image, caption=f"A view of {destination}", use_column_width=True)
            else:
                st.warning("❌ Unable to fetch image. Try again later.")
    else:
        st.warning("❌ No images generated.")
    
    with st.spinner("🎥 Creating AI Travel Video..."):
        travel_story_text = generate_travel_story(destination, start_date, end_date, purpose)
        narration_audio = generate_voiceover(travel_story_text)
        travel_video = create_travel_video(travel_images, narration_audio)
    
    st.subheader("🎥 AI-Generated Travel Video")
    if travel_video:
        st.video(travel_video)
    else:
        st.warning("❌ Video generation failed.")


