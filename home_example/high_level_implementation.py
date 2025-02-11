from langgraph.prebuilt import  create_react_agent
from langgraph.checkpoint.memory import  MemorySaver
from  langchain_openai import  ChatOpenAI
from langchain_core.tools import tool



#定义工具
@tool
def search(query:str):
    """call to surf the web"""
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy"
    return "It's 90 degree and sunny"

tools=[search]
model=ChatOpenAI(model="gpt-4-turbo-preview",temperature=0)

# 初始化内存以在图形运行之间持久化状态
checkpointer=MemorySaver()

app=create_react_agent(model, tools, checkpointer=checkpointer)

#使用代理
final_state=app.invoke(
    {"messages":[{"role":"user","content":"what is the weather in sf"}]},
    config={"configurable":{"thread_id":42}}
)
print(final_state["messages"][-1].content)