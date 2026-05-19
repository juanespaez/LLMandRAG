import openai
import os
from dotenv import load_dotenv
load_dotenv()

class ChatClient:
    def __init__(self, model="gpt-4o"):
        self.model = model
        self._client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def complete(self, messages, temperature=0.1, model=None):
        return self._client.chat.completions.create(
            model=model or self.model,
            messages=messages,
            temperature=temperature
        )
