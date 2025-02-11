from typing import Literal

from langchain_openai import  ChatOpenAI
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import  END,START,StateGraph,MessagesState
from langgraph.prebuilt import  ToolNode


#定义工具
@tool
def search(query:str):
    """call to surf the web."""
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy"
    return "It's 90 degrees and sunny"

tools=[search]

tool_node=ToolNode(tools)

model=ChatOpenAI(model="gpt-4-turbo-preview",temperature=0).bind_tools(tools)

# 定义决定是否继续的函数
def should_continue(state:MessagesState) -> Literal["tools",END]:
    messages=state["messages"]
    last_message=messages[-1]
    # 如果LLM进行工具调用，那么我们路由到“tool”节点
    if last_message.tool_calls:
        return "tools"
    # 否则，我们停止（回复用户）
    return END


#定义调用模型的函数
def call_model(state:MessagesState):
    messages=state["messages"]
    response=model.invoke(messages)
    # 我们返回一个列表，因为这将被添加到现有列表中
    return {"messages":{response}}


# 定义一个新图
workflow=StateGraph(MessagesState)

#定义我们将在之间循环的两个节点
workflow.add_node("agent",call_model)
workflow.add_node("tools",tool_node)

#将入口点设置为“agent”
#这意味着这个节点是第一个被调用的节点
workflow.add_edge(START,"agent")

# 添加一个条件边
workflow.add_conditional_edges(
    #首先，我们定义开始节点。我们使用“代理”。
    #这意味着这些是调用“代理”节点后获取的边。
    "agent",
    # 接下来，我们传入一个函数，这个函数将决定接下来调用哪个节点。
    should_continue
)

#我们现在添加一个从'tools'到'agent'的普通边。
#这意味着调用'tools'后，接下来调用'agent'节点。
workflow.add_edge("tools","agent")

#初始化内存以在图形运行之间持久化状态
checkpointer=MemorySaver()

#最后，我们编译它！
#这会将其编译成LangChain Runnable，
#意味着你可以像使用任何其他可运行的一样使用它。
#请注意，我们在编译图时（可选地）传递内存
app=workflow.compile(checkpointer=checkpointer)

#使用代理
final_state=app.invoke(
    {
        "messages":[{"role":"user","content":"what is the weather in sf"}]
    },
    config={"configurable":{"thread_id":42}}
)
print(final_state["messages"][-1].content)