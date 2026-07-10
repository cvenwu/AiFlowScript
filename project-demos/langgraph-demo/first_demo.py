import openai
import re
import httpx
import os
from dotenv import load_dotenv, find_dotenv

# 我们使用的代码是基于这篇文章的，是一个很好的介绍如何在python中实现REACT模式的文章
# based on https://til.simonwillison.net/llms/python-react-pattern
# Agent 由LLM + 围绕LLM构建的各种组件（可以统称为运行时）
_ = load_dotenv(find_dotenv())
from openai import OpenAI

client = OpenAI()

chat_completion = client.chat.completions.create(
    model="deepseek-ai/deepseek-v4-pro",
    messages=[{"role": "user", "content": "hello world"}],
)

print(chat_completion.choices[0].message.content)
