from Summarizer import Summarizer
from MessageList import MessageList
from prompts.DEFAULT_SYSTEM_PROMPT import DEFAULT_SYSTEM_PROMPT

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

