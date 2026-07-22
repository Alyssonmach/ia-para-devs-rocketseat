from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_key)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",

    contents="Explique como a Inteligência Artificial funciona em poucas palavras.",

    config=types.GenerateContentConfig(
        system_instruction="""
        Você é um professor de Inteligência Artificial.
        Responda sempre em português.
        """,

        temperature=0.4,
    ),
)

print(response.text)