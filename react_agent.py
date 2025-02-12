from typing import Literal
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, create_react_agent

# 加载环境变量
load_dotenv()

# 检查必要的环境变量
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("请在 .env 文件中设置 OPENAI_API_KEY")

# 检查可选的 LangSmith 配置
if os.getenv("LANGSMITH_API_KEY") and os.getenv("LANGSMITH_TRACING"):
    print("✅ 已启用 LangSmith 追踪功能")
else:
    print("⚠️ 提示: 设置 LANGSMITH_API_KEY 和 LANGSMITH_TRACING=true 以启用追踪功能")

# Define the tools for the agent to use
@tool
def search(query: str):
    """调用网络搜索（示例）。"""
    print(f"\n🔍 执行搜索: {query}")
    if "sf" in query.lower() or "san francisco" in query.lower():
        result = "当前气温为60°F，天气多雾。"
    else:
        result = "当前气温为90°F，天气晴朗。"
    print(f"📊 搜索结果: {result}")
    return result

def main():
    print("\n🚀 初始化代理系统...")
    
    # 设置工具
    tools = [search]
    print(f"⚙️ 已加载工具: {[tool.name for tool in tools]}")
    
    # 使用 OpenAI 模型
    model = ChatOpenAI(
        model="gpt-4-turbo-preview",
        temperature=0
    )
    print("🤖 已初始化 GPT-4 模型")
    
    # 初始化内存
    checkpointer = MemorySaver()
    print("💾 已初始化内存系统")
    
    # 创建代理应用
    app = create_react_agent(model, tools, checkpointer=checkpointer)
    print("✨ 代理应用创建完成")
    
    # 测试代理
    print("\n🌟 开始第一次对话...")
    final_state = app.invoke(
        {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
        config={"configurable": {"thread_id": 42}}
    )
    print("\n🤖 代理回复:")
    print(final_state["messages"][-1].content)
    
    # 测试持久化状态
    print("\n🌟 开始第二次对话...")
    final_state = app.invoke(
        {"messages": [{"role": "user", "content": "what about ny"}]},
        config={"configurable": {"thread_id": 42}}
    )
    print("\n🤖 代理回复:")
    print(final_state["messages"][-1].content)
    
    print("\n✅ 演示完成!")

if __name__ == "__main__":
    main()