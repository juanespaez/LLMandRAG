from back.chat_client import ChatClient
from back.message_list import MessageList

client = ChatClient()
conversation = MessageList()

conversation.add_system("You are a helpful assistant.")

user_input = input("You: ")
conversation.add_user(user_input)

response = client.complete(conversation.messages)
answer = response.choices[0].message.content

conversation.add_assistant(answer)
print(f"Assistant: {answer}")
