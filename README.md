# 🦜🕸️LangGraph

![版本](https://img.shields.io/pypi/v/langgraph)  
[![下载量](https://static.pepy.tech/badge/langgraph/month)](https://pepy.tech/project/langgraph)  
[![开放问题](https://img.shields.io/github/issues-raw/langchain-ai/langgraph)](https://github.com/langchain-ai/langgraph/issues)  
[![文档](https://img.shields.io/badge/docs-latest-blue)](https://langchain-ai.github.io/langgraph/)

⚡ 将语言代理构建为图 ⚡

> [!注意]
> 正在寻找 JS 版本？请参见 [JS 代码仓库](https://github.com/langchain-ai/langgraphjs) 和 [JS 文档](https://langchain-ai.github.io/langgraphjs/)。

## 概述

[LangGraph](https://langchain-ai.github.io/langgraph/) 是一个用于构建有状态、多参与者 LLM 应用的库，可用于创建单代理和多代理工作流。点击 [这里](https://langchain-ai.github.io/langgraph/tutorials/introduction/) 查看入门教程。

## 快速开始

1. 克隆仓库并安装依赖:
```bash
git clone <repository-url>
cd langgraph-demo
# 安装 poetry (如果尚未安装)
curl -sSL https://install.python-poetry.org | python3 -

# 安装依赖
poetry install

# 激活虚拟环境
poetry shell
```

2. 配置环境变量:
```bash
cp .env.example .env
```

编辑 .env 文件，添加你的 API 密钥:
```
DEEPSEEK_API_KEY=your_key_here
LANGSMITH_API_KEY=your_langsmith_key_here
LANGSMITH_TRACING=true
```

3. 运行示例:
```bash
poetry run python -m langgraph_demo.examples.react_agent
```

[完整的 README 内容...]
