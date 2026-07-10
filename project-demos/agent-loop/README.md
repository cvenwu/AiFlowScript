# agent-loop · 从零实现一个最小 Agent Loop

> 主线 B（AI Harness 工程师）第 1 站。目标：**不靠任何 Agent 框架**，用裸 HTTP 调本地 Ollama，
> 亲手实现「模型 → 工具调用 → 结果回灌 → 再决策」这个所有 Agent 的核心循环。

## 它做了什么

跑一个同时需要「查时间」+「做计算」的问题，观察 loop 如何在两轮内收敛：

```
用户提问：现在几点了？另外帮我算一下 (123 + 877) * 2 等于多少。

===== Step 1: 调用模型 =====
模型请求调用 2 个工具：
  -> get_current_time({})        结果: 2026-06-28 12:18:58
  -> calculate({'expression': '(123 + 877) * 2'})   结果: 2000

===== Step 2: 调用模型 =====
模型未请求工具，得到最终答复。

===== 最终答复 =====
现在的时间是2026年6月28日12点18分58秒。
(123 + 877) * 2 的计算结果是 2000。
```

## 运行

前提：本地已启动 Ollama（`ollama serve`），并 pull 了支持 tool calling 的模型。

```bash
cd agent-loop
uv sync
uv run main.py
# 换模型： MODEL=qwen3:14b uv run main.py
```

## 代码结构（建议按此顺序读）

| 文件 | 职责 | 读它能学到 |
| --- | --- | --- |
| `ollama_client.py` | 裸调 `/api/chat` 的 HTTP 客户端 | tool calling 在 wire 上的真实协议 |
| `tools.py` | 工具注册表 + 示例工具（时间、计算器） | schema（给模型的契约）与实现如何分离 |
| `agent.py` | **核心**：Agent Loop 状态机 | 整个 Agent 的骨架 |
| `main.py` | demo 入口 | 把上面三者串起来 |

## 核心原理

### 1. Agent Loop 本质是一个带终止条件的 for 循环

```
loop:
    message = 模型(messages, tools)      # 问模型
    messages.append(message)            # 存进历史（关键：模型要能看到自己说过的话）
    if message 没有 tool_calls:          # 终止条件
        return message.content          # 这就是最终答复
    for call in tool_calls:             # 否则执行工具
        result = run_tool(call)
        messages.append({role:"tool", content:result})   # 把结果回灌
    # 回到 loop 顶部，带着工具结果再问一次
```

LangChain / AutoGPT / Claude Code 最底层都是这个循环，区别只是在它之上加了
记忆、规划、多 Agent、可观测性等。**理解这个 loop = 理解 Agent 的地基。**

### 2. tool calling 的两半

- **schema**：JSON 描述「工具叫什么、干什么、要什么参数」，发给模型。模型据此决定调不调、怎么调。
- **实现**：真正执行的 Python 函数。模型不执行代码，它只「请求」调用，执行由我们的 harness 完成。

### 3. 消息角色（role）

| role | 含义 |
| --- | --- |
| `system` | 系统指令，定义助手行为 |
| `user` | 用户输入 |
| `assistant` | 模型输出（可能含 `tool_calls`） |
| `tool` | **工具执行结果**，回灌给模型的关键一环 |

## Go 工程师视角的类比

| Agent 概念 | Go 类比 |
| --- | --- |
| 裸调 `/api/chat` 而非 SDK | 不用 kitex/hertz，直接 `net/http` 看 wire 协议 |
| tool schema | IDL / proto 里的方法签名（给调用方的契约） |
| tool 实现 | handler（真正干活的代码） |
| Agent loop | `for` 里的状态机，按返回类型决定下一步直到终止态 |
| 模型 | 「调用方」，按契约发起 RPC |
| `max_steps` 护栏 | 防死循环 / 超时熔断 |

## 踩坑记录

- **`arguments` 的类型不固定**：Ollama 返回的工具参数有时是 `dict`，有时是 JSON 字符串，
  解析时要两种都兼容（见 `agent.py`）。
- **模型输出必须存回历史**：忘了 `messages.append(message)`，下一轮模型会「失忆」，
  无法基于工具结果继续推理。
- **`eval` 是注入风险**：`calculate` 用了字符白名单 + 空 `__builtins__` 兜底；
  生产环境应改用 `ast` 解析或专用表达式引擎，绝不能直接 eval 模型输出。
- **本地 14B 模型慢**：httpx 超时要给宽（这里 120s），否则容易误判失败。

## 面试可能怎么问

- 「请描述一个 Agent 的执行循环」 → 上面的伪代码 + 终止条件 + 回灌机制。
- 「function calling 的时候，函数是模型执行的吗？」 → 不是。模型只产出调用请求，执行由 harness 完成，结果再回灌。
- 「怎么防止 Agent 陷入死循环 / 失控？」 → `max_steps` 步数上限、超时、工具权限/沙箱、成本预算。
- 「`role=tool` 这条消息的作用是什么？」 → 把工具结果带回模型上下文，让它据此产出下一步决策或最终答复。
- 「为什么要把 assistant 的输出也加回 messages？」 → 维持对话状态，模型无状态，全靠历史还原上下文。

## 下一步可演进方向（对应主线 B 后续里程碑）

- [ ] 流式输出（`stream=True`）
- [ ] 多轮交互式 CLI（持续对话）
- [ ] 上下文长度预算与历史压缩/摘要
- [ ] 工具并行执行、超时与沙箱隔离
- [ ] 给 loop 加 tracing / 可观测性
- [ ] 简单的 eval：固定测试集 + 自动评分
