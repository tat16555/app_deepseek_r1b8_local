import chainlit as cl
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

@cl.on_chat_start
async def on_chat_start():
    elements = [cl.Image(name="image1", display="inline", path="DeepSeek.webp")]
    await cl.Message(content="Hello there, I am deepseek. How can I help you?", elements=elements).send()

    model = Ollama(
        model="deepseek-r1:8b",
        base_url="http://host.docker.internal:11434"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful and intelligent assistant who can answer questions on any topic clearly and accurately."),
        ("human", "{question}"),
    ])

    
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()

if __name__ == "__main__":
    cl.run()
