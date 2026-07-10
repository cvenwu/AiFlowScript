"""
demo 入口：跑通一个「必须调用工具才能回答」的问题，观察 Agent Loop 全过程。

运行：
    cd agent-loop
    uv run main.py
    # 指定模型： MODEL=qwen3:14b uv run main.py

前提：本地 Ollama 已启动（ollama serve），且已 pull 一个支持 tool calling 的模型，
例如：ollama pull qwen3:14b
"""

from __future__ import annotations

import os

from agent import run_agent
from ollama_client import OllamaClient

# 本地已有 qwen3:14b（支持 tool calling）；可用环境变量覆盖
MODEL = os.environ.get("MODEL", "qwen3:14b")

SYSTEM_PROMPT = (
    "你是一个有用的助手。当问题需要实时信息或计算时，"
    "请调用提供的工具，而不要凭空编造答案。"
)


def main() -> None:
    client = OllamaClient(model=MODEL)
    try:
        # 这个问题同时需要『查当前时间』和『做计算』两个工具，
        # 能很好地展示 loop 多轮调用的过程。
        question = "现在几点了？另外帮我算一下 (123 + 877) * 2 等于多少。"
        print(f"用户提问：{question}")

        answer = run_agent(
            client,
            user_input=question,
            system_prompt=SYSTEM_PROMPT,
            verbose=True,
        )

        print("\n===== 最终答复 =====")
        print(answer)
    finally:
        client.close()


if __name__ == "__main__":
    main()
