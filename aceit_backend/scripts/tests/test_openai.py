import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a test assistant."},
        {"role": "user", "content": "Say OK if this works."}
    ]
)

print(response.choices[0].message.content)
