from back.ChatClient import ChatClient
from back.MessageList import MessageList
from back.Commander import Commander
from prompts.DEFAULT_SYSTEM_PROMPT import DEFAULT_SYSTEM_PROMPT

client = ChatClient()
commander = Commander(client)
conversation = MessageList()

conversation.add_system(DEFAULT_SYSTEM_PROMPT)
last_response = None

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    elif user_input.lower() == "/compact":
        conversation = commander.compact(conversation.messages)

    elif user_input.lower() == "/memory":
        if last_response:
            commander.memory(last_response.usage, model=client.model)
        else:
            print("[System]: No messages sent yet.")

    elif user_input.lower() == "/help":
        commander.help()

    else:
        conversation.add_user(user_input)
        last_response = client.complete(conversation.messages)
        answer = last_response.choices[0].message.content
        conversation.add_assistant(answer)
        print(f"Assistant: {answer}")
