
import requests
import wikipediaapi
from gtts import gTTS
from moviepy import *
from config import llm
from utils import fetch_weather, fetch_tourist_attractions, fetch_flight_details, fetch_restaurants, fetch_hotels, fetch_currency_exchange_rate, fetch_travel_news


# ✅ Wikipedia API Setup
wiki = wikipediaapi.Wikipedia(user_agent="WanderTales/1.0", language="en")

# ✅ Function to fetch Wikipedia summary dynamically
def get_wikipedia_summary(place):
    page = wiki.page(place)
    return page.summary[:500] if page.exists() else "No Wikipedia summary found."

# ✅ Function to generate a travel story based on purpose and dates
def generate_travel_story(destination, purpose, start_date, end_date):
    wikipedia_info = get_wikipedia_summary(destination)

    purpose_templates = {
        "leisure": f"You are about to explore {destination} on a relaxing leisure trip from {start_date} to {end_date}. Describe your experiences as you visit famous landmarks, stroll through parks, and enjoy the peaceful atmosphere.",
        "food": f"As a food lover, you're in {destination} from {start_date} to {end_date} to explore its delicious street food, high-end restaurants, and unique local flavors. Describe the dishes you'll taste, the bustling food markets, and the famous cafés you’ll visit.",
        "adventure": f"You're visiting {destination} for an adrenaline-filled adventure from {start_date} to {end_date}. Describe thrilling activities such as hiking, surfing, skydiving, and other outdoor experiences in the area.",
        "business": f"You're traveling to {destination} for a business trip from {start_date} to {end_date}. Describe your meetings, networking events, and the city's corporate atmosphere. Also, mention any work-life balance experiences, like after-hours dining or sightseeing.",
        "romantic": f"You're in {destination} for a romantic getaway from {start_date} to {end_date}. Describe the intimate dinners, scenic walks, and breathtaking sunset views you'll experience with your partner.",
        "spiritual": f"You're visiting {destination} for a spiritual retreat from {start_date} to {end_date}. Describe the meditation spots, temples, churches, and peaceful landscapes where you'll find tranquility and reflection.",
        "family": f"You're on a family trip to {destination} from {start_date} to {end_date}, filled with fun and bonding moments. Describe the amusement parks, kid-friendly attractions, and the joy of exploring new places together."
    }

    purpose_prompt = purpose_templates.get(purpose, purpose_templates["leisure"])

    full_prompt = f"""
    {purpose_prompt}

    Be immersive, engaging, and detailed. Use vivid descriptions and include unique aspects of {destination}.

    Wikipedia Summary: {wikipedia_info}

    Travel Story:
    """

    try:
        response = llm.invoke(full_prompt)
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        return f"Error: OpenAI API call failed. Check your model name and API key: {str(e)}"

# ✅ Function to generate a voice-over for the travel story
def generate_voiceover(text, output_audio="travel_narration.mp3"):
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(output_audio)
        return output_audio
    except Exception as e:
        return f"Error generating voiceover: {str(e)}"

# ✅ Function to create a dynamic travel video with AI narration
def create_travel_video(image_urls, narration_audio, output_video="travel_story.mp4"):
    try:
        if not os.path.exists(narration_audio):
            raise FileNotFoundError(f"Audio file '{narration_audio}' not found.")
        
        audio_clip = AudioFileClip(narration_audio)
        image_duration = max(audio_clip.duration / max(len(image_urls), 1), 2)  # Ensure minimum duration per image
        
        image_clips = []
        for url in image_urls:
            try:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    image_clips.append(ImageClip(response.raw, duration=image_duration).set_fps(24).resize(1.05))
            except Exception as img_err:
                print(f"Skipping image due to error: {img_err}")
        
        if not image_clips:
            raise ValueError("No valid images retrieved for video generation.")
        
        video_clip = concatenate_videoclips(image_clips, method="compose").set_audio(audio_clip)
        video_clip.write_videofile(output_video, codec="libx264", fps=24, audio_codec="aac")

        return output_video
    except Exception as e:
        return f"Error creating video: {str(e)}"


# ✅ Testing the script (Example Execution)
if __name__ == "__main__":
    destination = "Paris"
    purpose = "Leisure"
    start_date = "2025-04-10"
    end_date = "2025-04-20"

    print("🔄 Fetching data and generating travel story...")
    travel_story_text = generate_travel_story(destination, purpose, start_date, end_date)
    print(f"📖 Travel Story:\n{travel_story_text}")

    print("🎤 Generating voiceover...")
    narration_file = generate_voiceover(travel_story_text)

    print("🎥 Creating travel video...")
    travel_images = ["https://source.unsplash.com/600x400/?Paris", "https://source.unsplash.com/600x400/?EiffelTower"]
    travel_video = create_travel_video(travel_images, narration_file)

    print(f"✅ Travel video saved as {travel_video}")
