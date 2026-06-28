"""
工具（Tools）：把普通 Python 函数暴露给模型调用。

一个工具由两部分组成：
1. schema —— 用 JSON 描述「这个工具叫什么、干什么、需要哪些参数」，发给模型看。
   模型靠这段描述来决定「要不要调、怎么调」。
2. 实现 —— 真正执行的 Python 函数，吃模型给的参数、返回字符串结果。

Go 类比：schema 像 IDL/proto 里的方法签名（给调用方看的契约），
实现像 handler（真正干活的代码）。模型扮演「调用方」，按契约发起调用。
"""

from __future__ import annotations

import datetime
from typing import Any, Callable

# ---- 工具实现 ----------------------------------------------------------------


def get_current_time() -> str:
    """返回当前本地时间。模型自己不知道「现在几点」，必须靠工具。"""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def calculate(expression: str) -> str:
    """计算一个数学表达式，例如 "2 * (3 + 4)"。

    注意：这里用了一个**受限**的 eval（只放行数字与运算符）。
    真实生产环境绝不能直接 eval 模型输出——这是典型的注入风险，
    应改用 ast 解析或专用表达式引擎。这里为教学保持简单，并做了字符白名单。
    """
    allowed = set("0123456789+-*/()., ")
    if not set(expression) <= allowed:
        return f"拒绝执行：表达式包含不允许的字符 -> {expression!r}"
    try:
        # __builtins__ 置空，禁止调用任何内置函数
        result = eval(expression, {"__builtins__": {}}, {})
    except Exception as exc:  # noqa: BLE001 - 工具错误要回灌给模型，不能崩
        return f"计算出错：{exc}"
    return str(result)


# ---- 工具注册表 --------------------------------------------------------------
# name -> (python 函数, 给模型看的 schema)

TOOLS: dict[str, tuple[Callable[..., str], dict[str, Any]]] = {
    "get_current_time": (
        get_current_time,
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "获取当前的本地日期和时间。当用户问『现在几点/今天几号』时使用。",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
    ),
    "calculate": (
        calculate,
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "计算一个数学表达式并返回结果。当用户需要算术运算时使用。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "要计算的数学表达式，例如 '2 * (3 + 4)'",
                        },
                    },
                    "required": ["expression"],
                },
            },
        },
    ),
}


def get_tool_schemas() -> list[dict[str, Any]]:
    """收集所有工具的 schema，发给模型。"""
    return [schema for _, schema in TOOLS.values()]


def run_tool(name: str, arguments: dict[str, Any]) -> str:
    """按名字执行工具。模型给的参数可能不靠谱，要兜底。"""
    entry = TOOLS.get(name)
    if entry is None:
        return f"未知工具：{name}"
    func, _ = entry
    try:
        return func(**arguments)
    except TypeError as exc:
        # 模型传错了参数名/数量，把错误回灌给它，让它下一轮自我纠正
        return f"工具 {name} 参数错误：{exc}"
