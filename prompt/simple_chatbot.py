import os
from operator import itemgetter
from typing import List

import tiktoken
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, trim_messages, SystemMessage, AIMessage
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory, RunnablePassthrough
from langchain_deepseek import ChatDeepSeek

from utils.comm_utils import tiktoken_counter, stream_response

model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

store = {}

def get_session_history(session_id: str, max_messages=10) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    # else:
    #     # 这里如果暴力清理，可能会把system给清理掉
    #     if len(store[session_id].messages) > max_messages:
    #         store[session_id].messages = store[session_id].messages[-max_messages:]
    return store[session_id]

# with_message_history = RunnableWithMessageHistory(model, get_session_history)
#
# config = {"configurable": {"session_id": "123"}}
#
# response = with_message_history.invoke(
#     [HumanMessage(content="Hello there, i am Bob")],
#     config=config,
# )
#
# print(response.content)
# print("********************")
#
# response = with_message_history.invoke(
#     [HumanMessage(content="What's my name?")],
#     config=config,
# )
# print(response.content)
# print("********************")
#
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer all questions to the best of your ability in {language}."),
    MessagesPlaceholder(variable_name="messages"),
])
#
# chain = prompt | model
# response = chain.invoke({
#     "messages": [HumanMessage(content="hello, I'm bob")], "language": "Chinese"
# })
# print(response.content)
# print("********************")
#
# with_message_history = RunnableWithMessageHistory(
#     chain,
#     get_session_history,
#     input_messages_key="messages" # 指定 messages 这个键的值作为聊天记录保存
# )
#
# config = {"configurable": {"session_id": "456"}}
#
# response = with_message_history.invoke(
#     {"messages": [HumanMessage(content="hi! I'm Sarah")], "language": "Chinese"},
#     config=config
# )


def str_token_counter(text: str) -> int:
    enc = tiktoken.get_encoding("o200k_base")
    return len(enc.encode(text))


# 创建一个历史消息管理器
trimmer = trim_messages(
    max_tokens=99,
    strategy="last",
    token_counter=tiktoken_counter,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

messages = [
    SystemMessage(content="你是一个智能助手，回答问题很简洁"),
    HumanMessage(content="hi! I'm bob"),
    AIMessage(content="hi!"),
    HumanMessage(content="I like vanilla ice cream"),
    AIMessage(content="nice"),
    HumanMessage(content="whats 2 + 2"),
    AIMessage(content="4"),
    HumanMessage(content="thanks"),
    AIMessage(content="no problem!"),
    HumanMessage(content="having fun?"),
    AIMessage(content="yes!"),
]

# trimmer.invoke(messages)

chain = (
    RunnablePassthrough().assign(messages=itemgetter("messages") | trimmer)
    | prompt
    | model
)

# response = chain.invoke(
#     {
#         "messages": messages + [HumanMessage(content="what's my name?")],
#         "language": "Chinese"
#     }
# )
# print(response.content)



with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history=get_session_history,
    input_messages_key="messages",
)

config = {"configurable": {"session_id": "789"}}

response = with_message_history.invoke(
    {
        "messages": messages +[HumanMessage(content="你好，我是小明")],
        "language": "Chinese"
    },
    config=config,
)

print(response.content)

print("********************")
# response = with_message_history.invoke(
#     {
#         "messages": [HumanMessage(content="今天是几号")],
#         "language": "Chinese"
#     },
#     config=config,
# )
stream_response(with_message_history, config, "今天是几号")

# response = with_message_history.invoke(
#     {
#         "messages": [HumanMessage(content="我叫什么名字")],
#         "language": "Chinese"
#     },
#     config=config,
# )
# print(response.content)
stream_response(with_message_history, config, "我叫什么名字")





