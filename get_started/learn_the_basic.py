from typing import  Annotated

from typing_extensions import  TypedDict
from langchain_core.tools import  tool
from langgraph.graph import  StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import  TavilySearchResults
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.checkpoint.memory import  MemorySaver

from langgraph.types import Command,interrupt


class State(TypedDict):
    # 消息类型为"list"。'add_messages'函数
    # 在注释中定义了这个状态键应该如何更新
    # （在这种情况下，它将消息附加到列表中，而不是覆盖它们）
    messages:Annotated[list,add_messages]
    name:str
    birthday:str

graph_builder=StateGraph(State)

@tool
def human_assistance(query:str)->str:
    """请求人类的协助"""
    human_response=interrupt({"query":query})
    return human_response["data"]

web_search=TavilySearchResults(max_results=2)
tools=[web_search,human_assistance]
# web_search.invoke("what is a 'node' in LangGraph?")

llm=ChatOpenAI(model="o3-mini")
llm_with_tools=llm.bind_tools(tools)

def chatbot(state:State):
    message=llm_with_tools.invoke(state["messages"])
    assert len(message.tool_calls)<=1
    return {"messages":message}

#第一个参数是唯一的节点名称
#第二个参数是随时调用的函数或对象
#使用节点。
graph_builder.add_node("chatbot",chatbot)

tool_node=ToolNode(tools=tools)
graph_builder.add_node("tools",tool_node)

#添加边
#条件边
graph_builder.add_conditional_edges("chatbot",
                                    tools_condition)
#任何时候调用一个工具，我们都返回到聊天机器人来决定下一步。
graph_builder.add_edge("tools","chatbot")
graph_builder.add_edge(START,"chatbot")

#添加内存记忆
memory=MemorySaver()

#完成图
graph=graph_builder.compile(checkpointer=memory)

config={"configurable":{"thread_id":"1"}}

#call chatbot
user_input="I need some expert guidance for building an AI agent. Could you request assistance for me?"

# The config is the **second positional argument** to stream() or invoke()!
events=graph.stream(
    {"messages":[{"role":"user","content":user_input}]},
    config=config,
    stream_mode="values",
)
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

human_response = (
    "We, the experts are here to help! We'd recommend you check out LangGraph to build your agent."
    " It's much more reliable and extensible than simple autonomous agents."
)
human_command=Command(resume={"data":human_response})
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

