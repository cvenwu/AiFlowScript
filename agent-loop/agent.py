"""
Agent Loop —— 整个项目的核心。

一句话原理：
    把对话历史发给模型 -> 模型要么直接回答，要么要求调用工具 ->
    如果要求调工具，就执行工具、把结果作为一条新消息塞回历史 -> 再发给模型 ->
    如此循环，直到模型不再要求工具、给出最终答复。

这就是 Claude Code / Cursor / 各类 Agent 框架最底层的那个「壳」。
高层框架（LangChain、AutoGPT 等）做的事，本质都是在这个循环上加东西
（记忆、规划、多 Agent、可观测性……）。理解了这个 loop，就理解了 Agent 的骨架。

Go 类比：像一个 for 循环里的状态机——每轮根据模型返回的「指令类型」
（回答 or 调工具）决定下一步，直到到达终止态。
"""

from __future__ import annotations

import json
from typing import Any

from ollama_client import OllamaClient
from tools import get_tool_schemas, run_tool


def run_agent(
    client: OllamaClient,
    user_input: str,
    system_prompt: str | None = None,
    max_steps: int = 10,
    verbose: bool = True,
) -> str:
    """运行一次完整的 Agent 任务，返回模型最终的自然语言答复。

    参数
    ----
    max_steps: 安全阀。防止模型陷入「反复调工具」的死循环，
        耗尽 token / 时间。这是 Harness 工程里必备的护栏。
    verbose: 打印每一步的内部状态，方便观察 loop 是怎么转的。
    """
    # 1) 初始化对话历史
    messages: list[dict[str, Any]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_input})

    tools = get_tool_schemas()

    # 2) 进入主循环
    for step in range(1, max_steps + 1):
        if verbose:
            print(f"\n===== Step {step}: 调用模型 =====")

        message = client.chat(messages, tools=tools)
        # 模型本轮的输出要先存进历史，否则下一轮模型「看不到自己说过的话」
        messages.append(message)

        tool_calls = message.get("tool_calls")

        # 2a) 终止条件：模型不再要求调用工具 -> 它给出的就是最终答复
        if not tool_calls:
            final = message.get("content", "")
            if verbose:
                print("模型未请求工具，得到最终答复。")
            return final

        # 2b) 模型要求调用工具：逐个执行，并把结果回灌
        if verbose:
            print(f"模型请求调用 {len(tool_calls)} 个工具：")

        for call in tool_calls:
            fn = call["function"]
            name = fn["name"]
            # Ollama 返回的 arguments 可能是 dict，也可能是 JSON 字符串，做下兼容
            raw_args = fn.get("arguments", {})
            if isinstance(raw_args, str):
                try:
                    arguments = json.loads(raw_args) if raw_args else {}
                except json.JSONDecodeError:
                    arguments = {}
            else:
                arguments = raw_args

            if verbose:
                print(f"  -> {name}({arguments})")

            result = run_tool(name, arguments)

            if verbose:
                print(f"     结果: {result}")

            # 关键：把工具结果作为一条 role=tool 的消息塞回历史。
            # 模型下一轮会读到它，据此继续推理。
            messages.append(
                {
                    "role": "tool",
                    "content": result,
                    "name": name,
                }
            )
        # for 循环回到顶部，带着工具结果再次询问模型

    # 3) 超过 max_steps 仍未收敛
    return f"（已达到最大步数 {max_steps}，未能得到最终答复，可能存在循环）"
