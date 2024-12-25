import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MY_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=MY_KEY)

# alloy, echo, fable, onyx, nova, and shimmer.
def gen_tts(input_text: str,
            voiceId: str,
            speed: float
):
    response = client.audio.speech.create(
        model="tts-1",
        voice=voiceId,
        speed=speed,
        input=input_text,
    )
    return response