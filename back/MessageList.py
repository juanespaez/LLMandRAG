class MessageList:
    def __init__(self):
        self.messages = []

    def add_system(self, text):
        self.messages.append({"role": "system", "content": text})
        return self

    def add_user(self, text):
        self.messages.append({"role": "user", "content": text})
        return self

    def add_assistant(self, text):
        self.messages.append({"role": "assistant", "content": text})
        return self
