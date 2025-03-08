
import streamlit as st
from travel_story import generate_travel_story, generate_voiceover, create_travel_video  # Correct import
from utils import fetch_weather, fetch_tourist_attractions, fetch_flight_details, fetch_restaurants, fetch_hotels
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="✈️ AI Travel Planner", layout="wide")

st.title("✈️ AI Travel Planner 🏨")

st.sidebar.title("Plan Your Trip 🗺")
destination = st.sidebar.text_input("Enter Destination", "Paris")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
purpose = st.sidebar.selectbox("Purpose of Visit", ["Leisure", "Business", "Adventure", "Romantic", "Family"])

if st.sidebar.button("Generate Travel Story"):
    with st.spinner("🔄 Generating AI travel story..."):
        try:
            travel_story_text = generate_travel_story(destination, purpose, start_date, end_date)
        except AttributeError as e:
            st.error("⚠️ AI generation failed: Possible incorrect OpenAI API usage. Check API setup.")
            travel_story_text = "❌ Error generating AI travel story. Please try again later."

    st.subheader("📖 Your AI-Generated Travel Story")
    st.write(travel_story_text)

    st.subheader("🌦 Weather Forecast")
    st.write(fetch_weather(destination))

    st.subheader("🏛 Tourist Attractions")
    st.write(fetch_tourist_attractions(destination))

    st.subheader("🍽 Recommended Restaurants")
    st.write(fetch_restaurants(destination, purpose))

    st.subheader("🏨 Hotel Recommendations")
    st.write(fetch_hotels(destination))

    st.subheader("✈️ Flight Details")
    st.write(fetch_flight_details("JFK", destination, start_date))

    st.subheader("🖼 View Destination Image")
    image_url = f"https://source.unsplash.com/600x400/?{destination}"  # Fetch image dynamically
    response = requests.get(image_url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        st.image(image, caption=f"A view of {destination}", use_column_width=True)
    else:
        st.warning("❌ Unable to fetch image. Try again later.")

    st.subheader("🎤 Generating Voiceover...")
    narration_audio = generate_voiceover(travel_story_text)
    st.audio(narration_audio)

    st.subheader("🎥 Creating AI Travel Video...")
    travel_images = [image_url]
    travel_video = create_travel_video(travel_images, narration_audio)
    st.video(travel_video)

    st.success("✅ Travel Story & AI Narration Generated Successfully!")
