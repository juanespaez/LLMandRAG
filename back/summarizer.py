from back.chat_client import ChatClient

class Summarizer:
    def __init__(self, client: ChatClient):
        self.client = client

    def format(self, messages):
        return "\n".join(f"[{m['role']}]: {m['content']}" for m in messages)

    def summarize(self, message_history):
        prompt = [
            {"role": "system", "content": (
                "You are an expert at creating concise, high-ROI summaries. "
                "Capture all key facts, decisions, and context so someone reading "
                "only the summary can continue the conversation seamlessly."
            )},
            {"role": "user", "content": f"Summarize this conversation:{self.format(message_history)}"}
        ]
        answer = self.client.complete(prompt, temperature=0.2)
        return answer.choices[0].message.content
