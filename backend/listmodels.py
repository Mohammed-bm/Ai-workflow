import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

print("Loaded key:", os.getenv("GOOGLE_API_KEY")[:6], "...")

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

for m in client.models.list():
    print(m.name)
