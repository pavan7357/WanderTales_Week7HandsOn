import streamlit as st
import os
from amadeus import Client
from langchain_openai.chat_models import ChatOpenAI

# ✅ Load API keys from Streamlit secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
AMADEUS_API_KEY = st.secrets["AMADEUS_API_KEY"]
GOOGLE_MAPS_API_KEY = st.secrets["GOOGLE_MAPS_API_KEY"]
WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]
SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
HUGGINGFACE_TOKEN = st.secrets["HUGGINGFACE_TOKEN"]

# ✅ Initialize OpenAI GPT-4 Model with the latest API key
llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY)
