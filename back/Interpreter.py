import json
from back.ChatClient import ChatClient
from prompts.INTERPRETER_SYSTEM_PROMPT import INTERPRETER_SYSTEM_PROMPT

class Interpreter:
    def __init__(self, client: ChatClient):
        self.client = client

    def decide(self, user_input: str) -> str:
        prompt = [
            {"role": "system", "content": INTERPRETER_SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
        response = self.client.complete(prompt, temperature=0.0, model="gpt-4o-mini")
        try:
            result = json.loads(response.choices[0].message.content)
            return result.get("action", "none")
        except (json.JSONDecodeError, KeyError):
            return "none"
