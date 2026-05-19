from back.chat_client import ChatClient
from back.message_list import MessageList
from prompts.prompts import DEFAULT_SYSTEM_PROMPT

client = ChatClient()
conversation = MessageList()

conversation.add_system(DEFAULT_SYSTEM_PROMPT)

user_input = input("You: ")
conversation.add_user(user_input)

response = client.complete(conversation.messages)
answer = response.choices[0].message.content

conversation.add_assistant(answer)
print(f"Assistant: {answer}")
