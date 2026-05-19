from back.ChatClient import ChatClient
from back.MessageList import MessageList
from prompts.prompts import DEFAULT_SYSTEM_PROMPT

client = ChatClient()
conversation = MessageList()

conversation.add_system(DEFAULT_SYSTEM_PROMPT)
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    conversation.add_user(user_input)

    response = client.complete(conversation.messages)
    answer = response.choices[0].message.content

    conversation.add_assistant(answer)
    print(f"Assistant: {answer}")
