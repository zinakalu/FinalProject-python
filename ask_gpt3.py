import openai
from dotenv import load_dotenv
import os



load_dotenv()
openai.api_key = os.getenv("GPT3API")

def ask_gpt3(question):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=question,
        temperature=0.5,
        max_tokens=100
    )

    return response.choices[0].text.strip()