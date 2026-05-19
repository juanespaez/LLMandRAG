import json
from back.chat_client import ChatClient
from prompts.prompts import TEMPERATURE_CLASSIFIER_SYSTEM_PROMPT

class TemperatureClassifier:

    def __init__(self, client: ChatClient):
        self.client = client

    def classify(self, user_input):
        prompt = [
            {"role": "system", "content": TEMPERATURE_CLASSIFIER_SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
        response = self.client.complete(prompt, temperature=0.0, model="gpt-4o-mini")
        try:
            result = json.loads(response.choices[0].message.content)
            temp = max(0.0, min(1.0, float(result["temperature"])))
            return temp, result.get("reason", "")
        except (json.JSONDecodeError, KeyError, ValueError):
            return 0.1, "fallback — could not parse classifier output"
