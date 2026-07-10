"""
Ollama 客户端：裸调 HTTP /api/chat 接口。

为什么不用 ollama-python SDK？
- 本项目的目标是「看清 Agent Loop 的真实协议」。SDK 会把请求/响应包装成对象，
  反而藏起了 messages、tool_calls、role 这些关键字段。
- 用 httpx 直接打 JSON，你能完整看到「发给模型什么、模型回了什么」，
  这正是 AI Harness 工程师每天要 debug 的东西。

Go 类比：相当于你不用 kitex/hertz 的高层封装，而是直接 net/http 手写一个 RPC 调用，
为的是理解 wire 上的协议长什么样。
"""

from __future__ import annotations

from typing import Any

import httpx

# Ollama 默认本地地址
DEFAULT_BASE_URL = "http://localhost:11434"


class OllamaClient:
    """对 Ollama /api/chat 的极简封装。"""

    def __init__(
        self,
        model: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 120.0,
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        # 本地模型推理可能较慢，超时给宽一点
        self._client = httpx.Client(timeout=timeout)

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """发送一轮对话请求，返回模型这一轮的 message。

        参数
        ----
        messages: 完整的对话历史。每条形如：
            {"role": "user"/"assistant"/"tool"/"system", "content": "...", ...}
        tools: 工具的 JSON schema 列表（OpenAI function-calling 格式）。
            传 None 表示本轮不允许调用工具。

        返回
        ----
        模型这一轮产出的 message dict，可能包含 "content"，
        也可能包含 "tool_calls"（模型要求调用工具）。
        """
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            # stream=False：一次性拿到完整结果，便于教学时打印观察。
            # 生产环境通常 stream=True 做流式输出。
            "stream": False,
        }
        if tools:
            payload["tools"] = tools

        resp = self._client.post(f"{self.base_url}/api/chat", json=payload)
        resp.raise_for_status()
        data = resp.json()
        # Ollama 的 /api/chat 把模型本轮输出放在 data["message"]
        return data["message"]

    def close(self) -> None:
        self._client.close()
