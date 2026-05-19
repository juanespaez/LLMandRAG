from back.ChatClient import ChatClient
from back.MessageList import MessageList
from back.Interpreter import Interpreter
from back.Summarizer import Summarizer
from prompts.DEFAULT_SYSTEM_PROMPT import DEFAULT_SYSTEM_PROMPT
from back.strings.HELP_TEXT import HELP_TEXT

client = ChatClient()
conversation = MessageList()
interpreter = Interpreter(client)
summarizer = Summarizer(client)

conversation.add_system(DEFAULT_SYSTEM_PROMPT)

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    action = interpreter.decide(user_input)

    if action == "compact":
        summary = summarizer.summarize(conversation.messages)
        conversation = MessageList()
        conversation.add_system(DEFAULT_SYSTEM_PROMPT)
        conversation.add_system(f"Conversation so far:\n{summary}")
        print("[System]: Conversation compacted.")
        continue

    elif action == "memory":
        total = sum(len(m["content"]) for m in conversation.messages)
        print(f"[System]: ~{total} characters in context across {len(conversation.messages)} messages.")
        continue

    elif action == "help":
        print(HELP_TEXT)
        continue

    conversation.add_user(user_input)
    response = client.complete(conversation.messages)
    answer = response.choices[0].message.content
    conversation.add_assistant(answer)
    print(f"Assistant: {answer}")
