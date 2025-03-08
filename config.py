import os
import streamlit as st

# ✅ Load API keys from Streamlit secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
AMADEUS_API_KEY = st.secrets["AMADEUS_API_KEY"]
GOOGLE_MAPS_API_KEY = st.secrets["GOOGLE_MAPS_API_KEY"]
WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]
SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
HUGGINGFACE_TOKEN = st.secrets["HUGGINGFACE_TOKEN"]
