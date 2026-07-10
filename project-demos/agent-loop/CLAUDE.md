# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in the `agent-loop/` sub-project.

> 仓库级指南见上一级目录的 `../CLAUDE.md`（含学习者背景、两条主线 Roadmap、全仓库约定）。本文件只聚焦本子项目。

## 这个项目是什么

主线 B（AI Harness 工程师）第 1 站：**从零实现一个最小 Agent Loop**。

核心约束：**不使用任何 Agent 框架（LangChain/AutoGPT 等），也不用 ollama-python SDK**，刻意用 `httpx` 裸调本地 Ollama 的 `/api/chat`，目的是看清 tool calling 在 wire 上的真实协议和 Agent loop 的骨架。这是本项目的教学价值所在，新增代码请保持这一风格。

## 运行与命令

前提：本地已 `ollama serve`，且 pull 了支持 tool calling 的模型。

```bash
cd agent-loop
uv sync                        # 安装依赖（仅 httpx）
uv run main.py                 # 跑 demo
MODEL=qwen3:14b uv run main.py # 用环境变量切换模型
```

- 默认模型：`qwen3:14b`（本地已有，14.8B，支持 tool calling），由 `main.py` 中 `MODEL` 环境变量覆盖。
- Python 版本：>= 3.14（`.python-version` 锁定）。
- 依赖管理：`uv` + `pyproject.toml`，不要引入 pip/requirements.txt。

## 代码结构与数据流

| 文件 | 职责 |
| --- | --- |
| `ollama_client.py` | `OllamaClient`：裸调 `/api/chat`，`stream=False` 一次性返回，便于观察 |
| `tools.py` | 工具注册表 `TOOLS`（name → (函数, schema)）+ 示例工具 `get_current_time` / `calculate` |
| `agent.py` | **核心** `run_agent()`：Agent Loop 状态机 |
| `main.py` | demo 入口，组装 client + system prompt + 问题 |

数据流（一轮循环）：
```
messages ──► client.chat(messages, tools) ──► message
                                               │
              ┌────────────────────────────────┤
              │ 有 tool_calls?                  │
         是 ──┤                                 ├── 否 ──► 返回 message.content（最终答复）
              ▼                                 
        run_tool() 执行                          
              ▼                                 
   append({role:"tool", ...}) 回灌 ──► 回到顶部再问
```

## 关键约定（改代码时务必遵守）

- **每一轮模型输出必须 append 回 `messages`**，否则模型下一轮失忆。
- **工具结果以 `{"role": "tool", "content": ..., "name": ...}` 回灌**，这是 loop 闭环的关键。
- **`tool_calls` 里的 `arguments` 类型不固定**（dict 或 JSON 字符串），新增解析逻辑要两种兼容。
- **`max_steps` 护栏不能去掉**，它防止模型陷入反复调工具的死循环。
- **工具执行要兜底**：模型给的参数可能不合法，错误要以字符串形式回灌给模型（让它自我纠正），而不是让程序崩溃。
- **不要直接信任模型输出去执行危险操作**：`calculate` 已用字符白名单 + 空 `__builtins__` 兜底，新增工具同样要考虑注入风险。

## 添加一个新工具的步骤

1. 在 `tools.py` 写一个返回 `str` 的 Python 函数。
2. 在 `TOOLS` 字典里登记：`name -> (函数, schema)`，schema 用 OpenAI function-calling 格式。
3. 无需改 `agent.py`——loop 会自动通过 `get_tool_schemas()` / `run_tool()` 发现并调用。

## 学习记录约定

本项目的 `README.md` 承担「学习复盘」职责：原理、Go 类比、踩坑、面试问法、演进方向。新增重要认知或踩坑时，同步更新 README，保持其作为可复述材料的价值。
