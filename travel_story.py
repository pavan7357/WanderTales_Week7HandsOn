
import openai
import requests
import wikipediaapi
import io
import time
import onnx
import numpy as np
from PIL import Image
from moviepy.editor import *  # For video editing
from gtts import gTTS  # For text-to-speech
from onnxruntime import InferenceSession
from transformers import AutoModelForCausalLM, AutoTokenizer
from config import OPENAI_API_KEY # Import the latest API key from config.py
from config import llm, amadeus
import openai

# ✅ Ensure OpenAI API is using the latest key
openai.api_key = OPENAI_API_KEY  # This ensures the latest key is used every time

# ✅ Initialize OpenAI Client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# ✅ Wikipedia API Setup
wiki = wikipediaapi.Wikipedia(user_agent="MyTravelApp/1.0", language="en")

# ✅ Function to fetch travel data from Wikipedia
def get_wikipedia_summary(place):
    page = wiki.page(place)
    return page.summary[:500] if page.exists() else "No Wikipedia summary found."

def generate_travel_story(origin, destination, purpose, start_date, end_date):
    wikipedia_info = get_wikipedia_summary(destination)

    purpose_templates = {
      "leisure": f"You are about to embark on a relaxing leisure trip starting from {origin} to {destination} from {start_date} to {end_date}. Describe your journey, including your departure experience, flight details, and how you arrive at {destination}. Highlight the famous landmarks, scenic parks, and peaceful experiences during your visit.",
    
      "food": f"As a food lover, you're traveling from {origin} to {destination} from {start_date} to {end_date} to explore its vibrant culinary scene. Describe the unique food experiences from the departure airport to your destination, including delicious street food, high-end restaurants, and bustling food markets in {destination}. Mention iconic cafés and dishes travelers should not miss.",
    
      "adventure": f"You're departing from {origin} to {destination} for an adrenaline-filled adventure from {start_date} to {end_date}. Describe your travel experience, flight, and arrival at {destination}. Highlight the thrilling activities such as hiking, surfing, skydiving, and other outdoor experiences that make this trip exhilarating.",
    
      "business": f"You're traveling from {origin} to {destination} for a business trip from {start_date} to {end_date}. Describe your departure from {origin}, your flight experience, and how you arrive at {destination}. Detail your meetings, networking events, and the city's corporate atmosphere. Also, mention after-hours dining or sightseeing to balance work and leisure.",
    
      "romantic": f"You're setting off from {origin} to {destination} for a romantic getaway from {start_date} to {end_date}. Describe the journey from {origin}, including your travel experience and how you and your partner arrive at {destination}. Highlight intimate dinners, scenic walks, breathtaking sunset views, and special moments shared during this trip.",
    
      "spiritual": f"You're traveling from {origin} to {destination} for a spiritual retreat from {start_date} to {end_date}. Describe your departure experience from {origin}, flight details, and arrival at {destination}. Mention meditation spots, temples, churches, and peaceful landscapes that provide a sense of tranquility and reflection.",
    
      "family": f"You're taking a family trip from {origin} to {destination} from {start_date} to {end_date}, creating memorable bonding moments. Describe your journey, including how you and your family prepare for the trip, your flight experience, and your arrival at {destination}. Highlight amusement parks, kid-friendly attractions, and activities that make this a joyful and unforgettable experience for everyone."
    }


    purpose_prompt = purpose_templates.get(purpose, purpose_templates["leisure"])

    full_prompt = f"""
    {purpose_prompt}

    Be immersive, engaging, and detailed. Use vivid descriptions and include unique aspects of {destination}.

    Wikipedia Summary: {wikipedia_info}

    Travel Story:
    """

    response = llm.invoke(full_prompt)
    return response.content if hasattr(response, 'content') else str(response)

# ✅ Function to generate a travel plan
def generate_travel_plan(origin, destination, start_date, end_date, purpose):
    prompt = f"""
    Generate a detailed travel itinerary for a trip starting from {origin} to {destination} from {start_date} to {end_date} for {purpose}.
    
    Include the following details:
    - **Departure details** from {origin}, including flight or transportation options.
    - **Arrival experience** in {destination} and first impressions.
    - **Accommodation recommendations** suitable for {purpose}.
    - **Top attractions** in {destination} that match {purpose}.
    - **Food and dining recommendations**, including famous restaurants.
    - **Local transportation options** to navigate within {destination}.
    - **Return trip details** from {destination} back to {origin} (if applicable).
    
    Ensure the itinerary is engaging and structured as a day-by-day plan.
    """
    response = llm.invoke(prompt)
    return response.content if hasattr(response, 'content') else str(response)


# ✅ Function to generate exactly 5 travel images based on purpose with timeout & retry
def generate_travel_images(destination, purpose):
    prompt_templates = {
        "leisure": [
            f"A breathtaking aerial view of {destination} at sunset, ultra-HD",
            f"A famous landmark in {destination} with tourists exploring",
            f"A peaceful park or nature spot in {destination}",
            f"A vibrant street with people walking in {destination}",
            f"A scenic sunset view from a rooftop in {destination}"
        ],
        "food": [
            f"A vibrant street food market in {destination}, filled with people enjoying local delicacies",
            f"A famous restaurant in {destination} serving authentic dishes",
            f"A cozy café in {destination}, perfect for food lovers",
            f"A chef cooking a signature dish in {destination}",
            f"A table full of delicious traditional food in {destination}"
        ],
        "adventure": [
            f"An exciting mountain hiking trail in {destination}, breathtaking views",
            f"A water sport activity like surfing or rafting in {destination}",
            f"A deep forest trekking scene in {destination}, wild nature",
            f"A scenic road trip along the coast in {destination}",
            f"A person skydiving over {destination}, adrenaline rush"
        ],
        "business": [
            f"A futuristic business district in {destination} with skyscrapers",
            f"A conference hall with professionals networking in {destination}",
            f"A co-working space with laptops and professionals working in {destination}",
            f"A businessperson having a coffee meeting in {destination}",
            f"A night view of {destination} with lights from corporate buildings"
        ],
        "romantic": [
            f"A romantic couple watching the sunset in {destination}, cinematic lighting",
            f"A candlelit dinner with a scenic view in {destination}",
            f"A dreamy evening walk in {destination}, beautiful city lights",
            f"A couple holding hands in front of a famous monument in {destination}",
            f"A cozy picnic in a park at {destination}, romantic atmosphere"
        ],
        "spiritual": [
            f"A peaceful Buddhist temple in {destination}, monks meditating",
            f"A yoga retreat in {destination} surrounded by nature",
            f"A quiet and scenic meditation spot in {destination}",
            f"A historical church or mosque in {destination}, spiritual atmosphere",
            f"A sunrise view from a hill in {destination}, peaceful and calm"
        ],
        "family": [
            f"A fun amusement park in {destination}, families enjoying rides",
            f"A zoo or aquarium in {destination}, children looking at animals",
            f"A large family picnic in {destination}, happy and cheerful atmosphere",
            f"A family exploring a famous museum in {destination}",
            f"A scenic beach in {destination} with kids playing in the sand"
        ],
    }

    selected_prompts = prompt_templates.get(purpose, prompt_templates["leisure"])
    image_urls = []

    for prompt in selected_prompts[:5]:  # Ensure we get exactly 5 images

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"

        )

        image_urls.append(response.data[0].url)
    return image_urls


# ✅ Function to create a voice-over for the travel story
def generate_voiceover(story_text, output_audio="travel_narration.mp3"):
    tts = gTTS(text=story_text, lang="en", slow=False)
    tts.save(output_audio)
    return output_audio

def create_travel_video(image_urls, narration_audio, output_video="travel_story.mp4"):
    audio_clip = AudioFileClip(narration_audio)
    total_audio_duration = audio_clip.duration
    image_duration = total_audio_duration / 5  # Divide equally among 5 images

    image_clips = []
    for i, url in enumerate(image_urls):
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
        image_path = f"travel_image_{i}.jpg"
        image.save(image_path)

        clip = ImageClip(image_path, duration=image_duration).set_fps(24)
        clip = clip.resize(lambda t: 1 + 0.01 * t)  # Slow zoom-in effect
        image_clips.append(clip)

    video_clip = concatenate_videoclips(image_clips, method="compose")
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_video, codec="libx264", fps=24, audio_codec="aac")
    print("🎬 Travel story animation created successfully!")


# ✅ Execution for Testing
if __name__ == "__main__":
    origin = "New York"
    destination = "Hyderabad"
    purpose = "Family"
    start_date = "2025-04-15"
    end_date = "2025-04-20"

    print("📅 Generating Travel Plan...")
    travel_plan = generate_travel_plan(origin, destination, start_date, end_date, purpose)
    print(f"📝 Travel Plan:\n{travel_plan}")

    print("🔄 Fetching data and generating travel story...")
    travel_story_text = generate_travel_story(origin, destination, purpose, start_date, end_date)
    print(f"📖 Travel Story:\n{travel_story_text}")

    print("🖼 Generating Travel Images...")
    image_urls = generate_travel_images(destination, purpose)
    print(f"Generated Images: {image_urls}")

    print("🎤 Generating voiceover...")
    narration_file = generate_voiceover(travel_story_text)

    print("🎥 Creating travel video...")
    travel_video = create_travel_video(image_urls, narration_file)
    print(f"✅ Travel video saved as {travel_video}")
