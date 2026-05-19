import json
from back.chat_client import ChatClient

class TemperatureClassifier:
    _SYSTEM_PROMPT = (
        "You are a request classifier. Analyze the user's message and decide "
        "the optimal temperature for an LLM response."
        "Rules:"
        "- Factual, analytical, code, math, lookups → 0.1"
        "- General conversation, explanations, summaries → 0.4"
        "- Brainstorming, ideas, pros/cons exploration → 0.7"
        "- Creative writing, storytelling, poetry, humor → 0.9"
        "Respond with ONLY a JSON object: {\"temperature\": <float>, \"reason\": \"<one-line>\"}"
    )

    def __init__(self, client: ChatClient):
        self.client = client

    def classify(self, user_input):
        prompt = [
            {"role": "system", "content": self._SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
        response = self.client.complete(prompt, temperature=0.0, model="gpt-4o-mini")
        try:
            result = json.loads(response.choices[0].message.content)
            temp = max(0.0, min(1.0, float(result["temperature"])))
            return temp, result.get("reason", "")
        except (json.JSONDecodeError, KeyError, ValueError):
            return 0.1, "fallback — could not parse classifier output"
