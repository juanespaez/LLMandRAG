import openai
import os
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def add_system_message(messages, text):
  system_message = {"role": "system", "content": text}
  messages.append(system_message)
  return messages

def add_assistant_message(messages, text):
  assistant_message = {"role": "assistant", "content": text}
  messages.append(assistant_message)
  return messages

def add_user_message(messages, text):
  user_message = {"role": "user", "content": text}
  messages.append(user_message)
  return messages

def chat(messages,temperature = 0.1, model="gpt-4o"):

  message = client.chat.completions.create(
    model=model,
    messages= messages,
    temperature=temperature

  )
  return message

def summarizer(message_history):
    summary_prompt = [
        {"role": "system", "content": (
            "You are an expert at creating concise, high-ROI summaries. "
            "Capture all key facts, decisions, and context so someone reading "
            "only the summary can continue the conversation seamlessly."
        )},
        {"role": "user", "content": f"Summarize this conversation:{format_messages(message_history)}"}
    ]
    answer = chat(summary_prompt, temperature=0.2)
    return answer.choices[0].message.content

def format_messages(messages):
    return "\n".join(f"[{m['role']}]: {m['content']}" for m in messages) 

def interpret_temperature(user_input):

    classifier_prompt = [
        {"role": "system", "content": (
            "You are a request classifier. Analyze the user's message and decide "
            "the optimal temperature for an LLM response."
            "Rules:"
            "- Factual, analytical, code, math, lookups → 0.1"
            "- General conversation, explanations, summaries → 0.4"
            "- Brainstorming, ideas, pros/cons exploration → 0.7"
            "- Creative writing, storytelling, poetry, humor → 0.9"
            "Respond with ONLY a JSON object: {\"temperature\": <float>, \"reason\": \"<one-line>\"}"
        )},
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=classifier_prompt,
        temperature=0.0
    )

    import json
    try:
        result = json.loads(response.choices[0].message.content)
        temp = float(result["temperature"])
        temp = max(0.0, min(1.0, temp))
        reason = result.get("reason", "")
        return temp, reason
    except (json.JSONDecodeError, KeyError, ValueError):
        return 0.1, "fallback — could not parse classifier output"

def show_help():
    print("""
Available commands:
  /compact  — Summarize and compress conversation history
  /memory   — Show context window usage
  /persona  — Change system prompt (e.g. /persona You are a Python expert)
  /help     — Show this message
  quit      — Exit the chat
    """)