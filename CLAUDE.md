# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

AiFlowScript 是一个 **AI Agent 开发学习与实战记录仓库**（`agent 开发学习仓库`）。仓库主理人正在从 **Go 服务端研发工程师** 转型为 **AI Agent 应用工程师 + AI Harness 工程师**，目标是：

1. **吃透原理** —— 不止会用框架，还能讲清 Agent loop、tool calling、上下文管理、评测等底层机制。
2. **项目驱动** —— 每个知识点都落到一个可运行的子项目里，边做边学。
3. **面试 / 转岗就绪** —— 沉淀可复述的经验、可展示的项目和可总结的方法论。
4. **持续记录** —— 所有学习产出（代码、笔记、踩坑、复盘）都进这个仓库。

仓库按子项目组织，每个独立方向放在自己的顶层目录下。

> **方法论统领**：本仓库所有子目录、所有学习与项目，都遵循 `learning-flywheel/` 中定义的「双循环能力复利飞轮」来推进。下面的 Roadmap 是“学什么”，飞轮是“怎么学”。

## Learner Profile（与 Claude Code 协作时的重要背景）

- **已有能力**：Go 服务端开发、并发、微服务、API/RPC、工程化与部署。可类比迁移到 Agent 工程。
- **目标能力**：见下方 Roadmap。
- **协作偏好**：
  - 优先讲**原理和取舍**，再给代码；能用 Go 的概念类比时多类比（如 goroutine vs async、middleware vs Agent 中间层）。
  - 代码要**可运行、可逐步演进**，避免一次性堆砌大框架。
  - 涉及新概念时，主动补充「为什么这样设计 / 业界还有哪些做法 / 面试常被怎么问」。

## Learning Flywheel（方法论 · 所有子目录都按此推进）

可视化见 `learning-flywheel/learning-flywheel-diagram.html`（浏览器打开，右上角 `⋯` 可导出 PNG/PDF）。

核心理念：**从「为面试而学」转向「为解决真实问题而产出，面试只是顺带验证」**。飞轮分内外两层，中心是「复利资产引擎」（知识库 / 代码模板 / 作品集 / 个人品牌 / 人脉），每转一圈都向中心沉淀资产，让下一圈更省力、越转越快。

### 内循环 · 周级 · 主引擎（跑能力）

1. **锚定目标**：先看市场信号（JD 聚类）→ 转成能力坐标。方向先行，不拍脑袋。
2. **诊断 Gap**：对比目标列出差距清单，排优先级。
3. **聚焦选题**：选 1 个真实项目，一题覆盖多个 Gap。
4. **边学边做**：学了立刻用在项目里，拒绝囤课。
5. **公开输出**：文章 / 开源 / Demo，用产出换高频真实反馈。
6. **反馈·复盘**：每周复盘，把经验提炼成可复用资产 → 回到 1。

### 外循环 · 月/季级 · 方向盘（校方向）

真实面试 / 对外交流 → 重看市场 JD → 校准能力坐标 → 修正内循环方向。**面试是周期性验证，不是引擎。**

### 四条设计原则（对每个子项目都适用）

- **外部信号先行**：市场 / JD 决定方向。
- **输出驱动**：以公开产出换真实反馈，而非自嗨或纯刷题。
- **每圈沉淀资产**：复利积累是飞轮加速的真正动力。
- **单点聚焦**：每圈只锁 1 个主题，对抗 AI 信息过载。

> **对 Claude Code 的要求**：开启任何新方向 / 新子目录时，按飞轮推进——先锚定市场目标与 Gap，再聚焦单一可运行项目，边学边做并产出可展示成果，最后在子项目 `README.md` 复盘沉淀。

## Roadmap（两条主线，项目驱动）

> 路线为引导，不是硬性顺序。每个里程碑对应一个或多个子项目目录。

### 主线 A：AI Agent 应用工程师

1. **LLM 基础调用**：补全/对话 API、流式输出、参数（temperature/top_p）、结构化输出（JSON mode / function schema）。
2. **Tool Calling / Function Calling**：让模型调用外部能力，理解 schema、调用循环、错误回灌。
3. **RAG**：向量化、检索、重排、上下文拼装；评估检索质量。
4. **Agent 编排**：单 Agent 工作流 → 多 Agent 协作 → 任务规划与反思。
5. **产品化**：API 服务化（FastAPI）、流式接口、鉴权、限流、可观测性、成本控制。

### 主线 B：AI Harness 工程师（构建 Agent 运行时本身）

1. **Agent Loop**：从零实现「模型 → 工具调用 → 结果回灌 → 再决策」的最小循环。
2. **Tool 调度与沙箱**：工具注册、并行/串行执行、超时、权限与隔离。
3. **上下文管理**：context window 预算、历史压缩/摘要、记忆机制。
4. **Prompt / System 工程**：system prompt 设计、指令分层、注入防护。
5. **评测 Harness（Eval）**：构造测试集、自动化评分、回归对比、可观测/Tracing。

## Sub-projects

### learning-flywheel/

仓库的**方法论中枢**，定义并可视化「双循环能力复利飞轮」（详见上方 Learning Flywheel 章节）。内含 `learning-flywheel-diagram.html`——自包含的可视化图，浏览器直接打开，右上角 `⋯` 可导出 PNG/PDF。本仓库所有子目录都按此飞轮推进。

### agent-loop/

主线 B 第 1 站：**从零实现最小 Agent Loop**。用 `httpx` 裸调本地 Ollama 的 `/api/chat`（不套任何 Agent 框架），亲手实现「模型 → tool calling → 结果回灌 → 再决策」核心循环。本地默认模型 `qwen3:14b`（支持 tool calling），可用 `MODEL` 环境变量覆盖。

Common commands (run from `agent-loop/`):

```bash
uv sync          # install deps (httpx)
uv run main.py   # 跑 demo（需本地 ollama serve）
MODEL=qwen3:14b uv run main.py
```

代码结构：`ollama_client.py`（HTTP 客户端）/ `tools.py`（工具注册表）/ `agent.py`（核心 loop）/ `main.py`（入口）。详见其 `README.md`。

### fast-api-demo/

A Python project managed with [uv](https://docs.astral.sh/uv/). Requires Python >= 3.14 (pinned via `.python-version`). Currently a minimal scaffold (`main.py` prints a hello message); FastAPI itself is not yet a dependency. 定位：主线 A 的「产品化 / API 服务化」练习场。

Common commands (run from `fast-api-demo/`):

```bash
uv sync          # install/sync dependencies into .venv
uv run main.py   # run the entry script
uv add <pkg>     # add a dependency (e.g. uv add fastapi)
```

## Conventions

- **目录结构**：每个新方向/项目放在仓库根目录下独立的顶层目录中。
- **飞轮统领**：所有子目录都按 `learning-flywheel/` 的双循环飞轮推进（市场锚定 → 聚焦单一项目 → 边学边做 → 公开输出 → 复盘沉淀）。
- **Python 工具链**：统一用 `uv` 管理依赖与虚拟环境（`pyproject.toml`，不用 pip/requirements.txt）。
- **学习记录**：每个子项目的 `README.md` 记录「学到了什么 / 原理要点 / 踩坑 / 面试问法」，作为可复述的复盘材料。
- **渐进式提交**：以可运行的小步迭代为单位提交，commit message 体现学习里程碑。
