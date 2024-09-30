# chainlit run demo.py -w   開始


from openai import AsyncOpenAI
import chainlit as cl
from typing import Optional

client = AsyncOpenAI(api_key="")
@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="gpt-4o-mini",
            markdown_description="The underlying LLM model is **GPT-3.5**.",
            icon="https://static.vecteezy.com/system/resources/previews/021/059/825/original/chatgpt-logo-chat-gpt-icon-on-green-background-free-vector.jpg",
        ),
        cl.ChatProfile(
            name="gpt-4o",
            markdown_description="The underlying LLM model is **GPT-4o**.",
            icon="https://static.vecteezy.com/system/resources/previews/021/059/827/original/chatgpt-logo-chat-gpt-icon-on-white-background-free-vector.jpg",
        ),
    ]

@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )

@cl.on_message
async def main(message: cl.Message):
    chat_profile = cl.user_session.get("chat_profile")
    if chat_profile == "gpt-4o-mini":
        settings = {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "max_tokens": 500,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }
    elif chat_profile == "gpt-4o":
        settings = {
            "model": "gpt-4o",
            "temperature": 0.7,
            "max_tokens": 500,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})
    

    msg = cl.Message(content="")
    await msg.send()
    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    print('=====================', message_history)
    await msg.update()
