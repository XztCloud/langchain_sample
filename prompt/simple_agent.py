import os

from langchain.chat_models import init_chat_model
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# create the agent
memory = MemorySaver()

os.environ["OPENAI_API_KEY"] = os.getenv("DASHSCOPE_API_KEY")
os.environ["OPENAI_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
model = init_chat_model(model="qwen-plus", model_provider="openai")
# model = ChatDeepSeek(
#     model="deepseek-chat",
#     api_key=os.getenv("DEEPSEEK_API_KEY"),
# )
search = TavilySearchResults(max_results=2)

# try:
#     search = TavilySearchResults(max_results=1)
#     result = search.invoke("测试")
#     print("Tavily 可用:", result)
# except Exception as e:
#     print("Tavily 不可用:", str(e))

tools = [search]

agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content="hi im bob! and i live in shanghai")]}, config
):
    print(chunk)
    print("----")

for chunk in agent_executor.stream(
        {"messages":[HumanMessage(content="whats the weather I live?")]}, config
):
    print(chunk)
    print("----")
