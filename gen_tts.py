import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MY_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=MY_KEY)

def gen_tts(input_text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=input_text,
    )
    return response