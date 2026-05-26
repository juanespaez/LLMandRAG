from Summarizer import Summarizer
from MessageList import MessageList
from prompts.DEFAULT_SYSTEM_PROMPT import DEFAULT_SYSTEM_PROMPT
from strings.HELP_TEXT import HELP_TEXT

# Maximum context window sizes (in tokens) per model, as published by OpenAI.
# Update here if OpenAI changes limits: https://platform.openai.com/docs/models
MODEL_CONTEXT_LIMITS = {
    "gpt-4o": 128_000,
    "gpt-4o-mini": 128_000,
}

class Commander:
    def __init__(self, client):
        self.client = client
        
    def compact(self, messages):
        summarizer = Summarizer(self.client)
        summary = summarizer.summarize(messages)
        conversation = MessageList()
        conversation.add_system(DEFAULT_SYSTEM_PROMPT)
        conversation.add_system(f"Conversation so far:\n{summary}")
        print("[System]: Conversation compacted.")
        return conversation

    def help(self):
        print(HELP_TEXT)

    def memory(self, usage, model="gpt-4o"):
        limit = MODEL_CONTEXT_LIMITS.get(model, 128_000)
        used = usage.prompt_tokens
        percentage = used / limit * 100
        print(f"[System]: {used} / {limit} tokens used ({percentage:.1f}%)")
        return percentage

