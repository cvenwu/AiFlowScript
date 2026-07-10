<div align="center">

# 🌊 AiFlowScript

**从零吃透 AI Agent —— 一个项目驱动的 Agent 开发学习与实战仓库**

*不止会用框架，更能讲清 Agent Loop、Tool Calling、上下文管理与评测的底层机制*

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.14+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/built%20with-uv-DE5FE9?logo=astral&logoColor=white)](https://docs.astral.sh/uv/)
[![Ollama](https://img.shields.io/badge/LLM-Ollama-000000?logo=ollama&logoColor=white)](https://ollama.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#-贡献)

[核心理念](#-核心理念) · [快速开始](#-快速开始) · [子项目](#-子项目) · [Roadmap](#-roadmap) · [学习飞轮](#-学习飞轮)

</div>

---

## 📖 简介

**AiFlowScript** 记录仓库主理人从 **Go 服务端研发工程师** 转型为 **AI Agent 应用工程师 + AI Harness 工程师** 的全过程。每个知识点都落到一个**可运行的子项目**里，边做边学、边学边复盘。

> 💡 **一句话定位**：Roadmap 决定「学什么」，[学习飞轮](#-学习飞轮)决定「怎么学」，每个子目录都是一次飞轮的落地。

## 🎯 核心理念

| | 理念 | 含义 |
| :---: | --- | --- |
| 🧠 | **吃透原理** | 不止会调框架，能讲清 Agent loop、tool calling、上下文管理、评测等底层机制 |
| 🛠️ | **项目驱动** | 每个知识点都落到一个可运行的子项目，拒绝囤课 |
| 🎤 | **转岗就绪** | 沉淀可复述的经验、可展示的项目、可总结的方法论 |
| 📝 | **持续记录** | 代码、笔记、踩坑、复盘全部进仓库，复利积累 |

## 🚀 快速开始

仓库统一使用 [`uv`](https://docs.astral.sh/uv/) 管理 Python 依赖与虚拟环境。

```bash
# 克隆仓库
git clone git@github.com:cvenwu/AiFlowScript.git
cd AiFlowScript

# 体验「从零实现的最小 Agent Loop」（需本地先启动 ollama serve）
cd agent-loop
uv sync
uv run main.py
# 切换模型： MODEL=qwen3:14b uv run main.py
```

运行后你会看到一个同时需要「查时间 + 做计算」的问题，如何在两轮 loop 内收敛 👇

```text
用户提问：现在几点了？另外帮我算一下 (123 + 877) * 2 等于多少。

===== Step 1: 调用模型 =====
模型请求调用 2 个工具：
  -> get_current_time({})                          结果: 2026-06-28 12:18:58
  -> calculate({'expression': '(123 + 877) * 2'})  结果: 2000

===== Step 2: 调用模型 =====
模型未请求工具，得到最终答复。

===== 最终答复 =====
现在的时间是 2026 年 6 月 28 日 12 点 18 分 58 秒。
(123 + 877) * 2 的计算结果是 2000。
```

## 📦 子项目

| 目录 | 主线 | 简介 | 文档 |
| --- | :---: | --- | :---: |
| 🔁 [`agent-loop/`](project-demos/agent-loop) | B · Harness | 用 `httpx` 裸调 Ollama `/api/chat`，**不套任何框架**手写「模型 → 工具调用 → 结果回灌 → 再决策」核心循环 | [README](project-demos/agent-loop/README.md) |
| ⚡ [`fast-api-demo/`](project-demos/fast-api-demo) | A · 应用 | 主线 A「产品化 / API 服务化」练习场（FastAPI、流式接口、鉴权、限流、可观测性） | — |
| 🎡 [`learning-flywheel/`](./learning-flywheel) | 方法论 | 仓库方法论中枢，可视化「双循环能力复利飞轮」（浏览器打开 HTML 可导出 PNG/PDF） | — |
| 🗺️ [`ai-roles-roadmap/`](./ai-roles-roadmap) | 方向 | AI 岗位 JD / 技能 Roadmap 可视化页面 | — |
| 🎬 [`roadmap-video/`](./roadmap-video) | 输出 | 用 HyperFrames 制作的转型 Roadmap 概览视频（`roadmap.mp4`） | — |

## 🗺️ Roadmap

> 路线为引导，不是硬性顺序。每个里程碑对应一个或多个子项目目录。

### 🅰️ 主线 A：AI Agent 应用工程师

```
1. LLM 基础调用      补全/对话 API · 流式输出 · 参数 · 结构化输出
2. Tool Calling      让模型调用外部能力 · schema · 调用循环 · 错误回灌
3. RAG               向量化 · 检索 · 重排 · 上下文拼装 · 检索质量评估
4. Agent 编排        单 Agent → 多 Agent 协作 → 任务规划与反思
5. 产品化            FastAPI · 流式接口 · 鉴权 · 限流 · 可观测性 · 成本控制
```

### 🅱️ 主线 B：AI Harness 工程师（构建 Agent 运行时本身）

```
1. Agent Loop        从零实现「模型 → 工具调用 → 结果回灌 → 再决策」  ✅ agent-loop/
2. Tool 调度与沙箱   工具注册 · 并行/串行执行 · 超时 · 权限与隔离
3. 上下文管理        context window 预算 · 历史压缩/摘要 · 记忆机制
4. Prompt / System   system prompt 设计 · 指令分层 · 注入防护
5. 评测 Harness      测试集 · 自动化评分 · 回归对比 · Tracing
```

## 🎡 学习飞轮

本仓库所有子目录都遵循 `learning-flywheel/` 中定义的 **「双循环能力复利飞轮」** 推进 —— 核心是从「为面试而学」转向「**为解决真实问题而产出，面试只是顺带验证**」。

```
  内循环 · 周级 · 主引擎（跑能力）
  锚定目标 → 诊断 Gap → 聚焦选题 → 边学边做 → 公开输出 → 反馈复盘 ↻
                                                              │
  外循环 · 月/季级 · 方向盘（校方向）                          ▼
  真实面试 / 对外交流 → 重看市场 JD → 校准能力坐标 → 修正方向
```

**四条设计原则**：🎯 外部信号先行 · 📣 输出驱动 · 💰 每圈沉淀资产 · 🔍 单点聚焦。

> 可视化见 [`learning-flywheel/learning-flywheel-diagram.html`](./learning-flywheel/learning-flywheel-diagram.html)（浏览器直接打开，右上角 `⋯` 可导出 PNG/PDF）。

## 🧩 目录结构

```
AiFlowScript/
├── 🔁 agent-loop/         主线 B 第 1 站：从零实现最小 Agent Loop
├── ⚡ fast-api-demo/      主线 A：API 服务化练习场
├── 🎡 learning-flywheel/  方法论中枢：能力复利飞轮可视化
├── 🗺️ ai-roles-roadmap/   AI 岗位 JD / 技能 Roadmap
├── 🎬 roadmap-video/      转型 Roadmap 概览视频
├── 📄 CLAUDE.md           协作背景 · Roadmap · 约定
└── 📜 LICENSE             Apache 2.0
```

## 🧰 技术栈

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-DE5FE9?logo=astral&logoColor=white)
![httpx](https://img.shields.io/badge/httpx-2A6DB2?logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?logo=ollama&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![HyperFrames](https://img.shields.io/badge/HyperFrames-FF5A5F?logo=html5&logoColor=white)

## 🤝 贡献

这是一个**个人学习仓库**，主要沉淀学习产出与复盘。欢迎通过 Issue 交流讨论、提建议，或 Fork 后用于自己的 Agent 学习路径。

## 📜 License

本项目基于 [Apache License 2.0](./LICENSE) 开源。

---

<div align="center">

**🌊 边学边做，每圈沉淀 —— 让飞轮越转越快**

</div>
