# Go 服务端工程师转型 AI Agent 应用 + AI Harness 工程师 · 完整路线设计

## 1. 背景与定位

- **当前身份**：Go 服务端研发工程师，能看懂/编写简单 Python 脚本，熟悉后端系统设计、并发、状态管理、可观测性。
- **AI 基础**：几乎零基础（用过 ChatGPT/Claude 产品，未系统写过调 LLM API 的代码）。
- **目标身份**：AI Agent 应用工程师 + AI Harness 工程师。
- **时间预算**：高强度冲刺，每周 20 小时以上，目标周期 2-3 个月达到「可面试 / 可转岗」水平。
- **目的**：快速了解原理 + 项目实践驱动 + 通过转岗或外部招聘面试 + 积累深刻可讲述的经验。
- **载体仓库**：`AiFlowScript`（本仓库），主线产出直接沉淀于此。

### 关于 "AI Harness" 的澄清

AI Harness = 让模型能真正干活的那层工程系统。模型本身只是 `text in → text out` 的函数；Claude Code、Cursor、Devin 这类产品的强大之处不在模型，而在外面包的 harness：

- **运行时（Runtime）**：Agent 循环（ReAct / Plan-Execute）、工具调度、上下文窗口管理、会话压缩、子 agent 派发。
- **评测（Eval harness）**：用基准任务自动跑 Agent，打分、回归、防止改一处崩一片（如 SWE-bench、Terminal-bench）。
- **工程基设**：沙箱执行、prompt/上下文流水线、可观测性（trace / token 成本）、缓存。

**核心洞察**：作为 Go 后端工程师，最大差异化优势在 harness 而非模型。harness 比拼的是系统设计、并发调度、状态管理、工程健壮性、成本与可观测性——后端工程师的主场，而非算法/调参。因此路线重心是「应用层快速入门 → 重仓 harness」，不卷 Transformer 数学。

## 2. 最终方案

- **路线组织方式**：方案 A（能力螺旋式）为主线 + 方案 B（面试驱动逆推）为辅助。
- **能力螺旋**：按「原理 → 应用 → harness → 评测」四个圈层层叠加，每圈层用递进项目串起。
- **重心分配**：应用与 harness 并重。
- **技术栈**：Python 写应用层（生态最全）+ Go 写 harness 内核（差异化主场），两者通过 OpenAI-compatible API + 工具协议解耦。

### 主线大项目（贯穿全程，简历核心）

> **`AiFlowScript` —— 自研 Agent Harness（mini Claude Code）**
> - **harness 内核用 Go**：Agent 循环、工具调度、上下文管理、会话压缩、可观测性、成本控制。
> - **应用层用 Python**（延展 fast-api-demo）：RAG、工具生态、workflow 编排、Web/API 接入。
> - 两者通过明确接口解耦。

## 3. 四阶段螺旋总览

| 阶段 | 主题 | 能力圈 | 主线项目里程碑 | B 线辅助 |
|---|---|---|---|---|
| 0. 原理打底 | LLM/Agent 第一性原理 | 够用就好，不卷数学 | 跑通最小 Agent 循环 | 收集 JD + 高频题清单 |
| 1. 应用层 | RAG + 工具调用 + 编排 | Python 生态 | Python 应用层成型 | 应用类面试题 |
| 2. harness 内核 | Go 自研运行时 | 系统设计主场 | Go harness MVP | 系统设计/源码题 |
| 3. 评测与硬化 | eval + 可观测 + 成本 | 工程深度 | 接入 benchmark + trace | 项目深挖模拟面 |

**核心原则**：每阶段「先读最小必要原理 → 立刻动手做项目 → 用 B 线面试题检验是否真懂」，绝不停留在纯看文档。

## 4. 阶段 0 — 原理打底（约 1-1.5 周）

### 最小必要原理（够用就走，绝不卷数学）

- LLM 本质：`token in → token 概率分布 → 采样 out`；context window、temperature、tokenizer。
- 为什么需要 Agent：LLM 无状态、无记忆、不能执行 → harness 补足这三点。
- 核心范式：ReAct（Reason+Act）、Function/Tool Calling 的请求-响应协议。
- Prompt 工程基础：system/user/assistant 角色、few-shot、结构化输出。
- 必读：ReAct 论文（只读思想）+ Anthropic「Building effective agents」博客。

### 阶段 0 项目（主线起点）

> **手写最小 Agent 循环**（Python，50 行内）
> 直接调 LLM API，实现 `while(未完成){ 思考→调工具→喂回结果 }` 循环，挂 1 个计算器工具。**禁用任何框架**，纯手撸，目的是看穿 Agent 本质 = while 循环 + 工具路由。

### 验收标准

- 能解释「Agent 循环里每一步 prompt 长什么样」「工具调用结果如何拼回上下文」。

## 5. 阶段 1 — 应用层（约 2 周，Python）

### 原理 + 技能

- RAG 全链路：分块(chunking) → 向量化(embedding) → 检索(vector db) → 重排(rerank) → 注入 prompt。
- 工具生态：工具定义规范、参数校验、错误处理、多工具路由。
- Workflow 编排：LangGraph 的图模型（节点/边/状态），对比手写循环。
- 记忆：短期（会话）vs 长期（向量库）。

### 技术栈（经调研确定）

> **LangGraph（编排主框架）+ LlamaIndex（RAG 检索）+ PydanticAI（对照学习 + 工具类型契约）**

选型理由摘要：
- **LangGraph**：把 Agent 显式建模为「状态 + 节点 + 条件边 + checkpoint」，与后端状态机/工作流思维一致；暴露的概念（状态持久化、中断恢复、循环/分支控制）正是阶段 2 自研 harness 要解决的问题，是天然参照系；面试热度第一。
- **PydanticAI**：类型安全 + 结构化输出 + 可测试，与 Go 强类型背景共鸣，对阶段 2 设计 Go harness 的工具协议/接口契约有参考价值。
- **LlamaIndex**：RAG/数据接入最强，做检索链路比 LangGraph 顺手，二者可组合。
- **不选** CrewAI/AutoGen：role-based 高层封装把底层 API 藏太深，不利于看穿原理与做 harness。

### 阶段 1 项目（应用层成型，挂到主线 repo）

> **「文档问答 + 工具增强」Agent 应用**
> - 用 LlamaIndex 搭 RAG：导入一批文档（如 Go 项目源码或技术文档）做问答。
> - 用 LangGraph 编排多步 workflow：检索 → 判断是否需要工具 → 调工具 → 综合回答。
> - 暴露成 FastAPI 接口（复用 fast-api-demo）。
> - 至少 3 个工具：检索、计算、外部 API 调用。

### 验收标准

- 能讲清 RAG 每环节设计权衡（chunk 大小、检索 topK、为何 rerank）。
- 能对比「手写循环 vs LangGraph」的取舍（阶段 2 伏笔）。
- B 线检验：能答「RAG 召回率低怎么排查」「幻觉怎么缓解」。

## 6. 阶段 2 — Go 自研 Harness 内核（约 3 周，重头戏）

**目标**：用 Go 从零写 mini Agent runtime，把阶段 1 用 LangGraph「用过」的能力自己「造」一遍。简历最硬部分。

### 核心问题（每个都是面试深挖点）

- **Agent 循环引擎**：ReAct 主循环、停机条件、最大步数/超时控制。
- **工具调度**：工具注册表、JSON Schema 参数校验、并发工具调用（goroutine 主场）、错误重试。
- **上下文管理**：token 计数、上下文窗口裁剪策略、会话压缩（超长对话摘要）。
- **LLM 接入层**：抽象 provider 接口（OpenAI 兼容），流式输出（SSE），重试/退避。
- **子 Agent 派发**（弹性进阶）：主 Agent 拆任务给子 Agent，结果回收。

### 阶段 2 项目（主线 MVP，纯 Go）

> **`AiFlowScript` harness 内核 v1**
> - 完整 Agent 循环，挂载工具（文件读写、shell 执行、HTTP 调用）。
> - provider 抽象层 + 流式输出。
> - 上下文裁剪 + 会话压缩。
> - 通过 OpenAI-compatible API 暴露，让阶段 1 的 Python 应用层调用它。
> - 沙箱执行：工具调用（尤其 shell）在受限环境跑（harness 安全核心）。

### 验收标准

- 能画 harness 架构图，讲清每个模块职责和接口。
- 能对比「Go 实现 vs LangGraph」的设计取舍（并发、状态、性能）。
- B 线检验：能答「上下文爆了怎么办」「工具调用失败如何优雅降级」「如何控制 Agent 死循环」。

## 7. 阶段 3 — 评测与工程硬化（约 2-3 周，拉开差距）

**目标**：把 harness 从「能跑」变成「可信、可观测、可控成本」——harness 工程师区别于调包侠的分水岭。

### 原理 + 技能

- **Eval harness**：为何需要评测、benchmark 设计、自动打分（LLM-as-judge）、回归测试防止改一处崩一片。
- **可观测性**：trace（每步 LLM/工具调用链路）、token 成本统计、延迟监控。
- **成本与性能**：prompt 缓存、并发控制、模型路由（简单任务用小模型）。

### 阶段 3 项目（主线硬化，挂到 repo）

> **给 harness 加上 eval + 可观测层**
> - 自建小型 benchmark：10-20 个任务（如「读文件改 bug」「多步检索回答」），自动跑 + 打分。
> - 接入 trace：记录每次 run 的完整调用链 + token 成本（可对接 OpenTelemetry，后端熟）。
> - 跑「改进前/改进后」对比，用数据说明优化效果。
> - **接入业界 benchmark（弹性进阶）**：如 SWE-bench Lite 子集刷分。

### 验收标准

- 能用数据讲「我优化了 X，eval 分数从 A 到 B，成本降 C%」的故事（面试金句）。
- 能讲清「如何评测一个 Agent 好不好」「LLM-as-judge 的坑」。
- B 线检验：「Agent 上线后怎么监控」「如何做 A/B 评测」。

## 8. 理论补充模块（贯穿全程，面试能答 + 浅度实践）

**原则**：不卷数学推导、不训模型，目标是面试能讲清概念+权衡，并在实践中能用上。穿插在阶段 0/3 的碎片时间，每个概念限时 ≤ 半天。

### 必懂概念清单（面试高频）

- **Transformer/注意力**：scaled dot-product attention 思想、为何能并行、KV cache 是什么（与 harness 上下文管理直接相关）。
- **MoE（混合专家）**：稀疏激活原理、router/gating、为何省算力、推理时负载均衡问题。了解 Mixtral/DeepSeek-MoE 调用特点。
- **强化学习对齐**：RLHF 全流程（SFT → 奖励模型 → PPO）、DPO vs RLHF 区别、GRPO 新趋势、reward hacking（奖励黑客）高频坑。
- **微调**：SFT、LoRA/QLoRA、PEFT 为何主流、何时该微调 vs RAG vs prompt。

### 实践锚点（让理论落地）

- 在阶段 2 的 provider 层接入一个 MoE 模型（如 Mixtral/DeepSeek），实测对比成本/延迟，能讲「为什么 MoE 适合做 Agent 后端」。
- 用 LoRA 对小模型做一次极简微调（弹性进阶），体感「微调 vs RAG」取舍。

## 9. B 线面试准备体系（贯穿全程）

| 维度 | 内容 | 何时做 |
|---|---|---|
| JD 逆推 | 收集 10+ 目标岗 JD，提炼能力关键词，对照路线查漏 | 阶段 0 启动，每阶段更新 |
| 题库分层 | 应用题（RAG/工具）、系统设计题（harness 架构）、原理题（MoE/RL/Transformer） | 每阶段末刷对应层 |
| 项目深挖稿 | 为主线项目准备「STAR + 架构图 + 取舍 + 数据」讲解稿 | 阶段 2/3 |
| 模拟面试 | 用 AI 做模拟面试官，压测项目深度和原理 | 阶段 3 |

**核心面试叙事**：「我用 Go 自研了一个 Agent harness，对标 LangGraph 但在并发工具调度和成本控制上做了 X 优化，eval 分数从 A 到 B」——后端转 AI 的最强叙事。

## 10. 整体时间线（2-3 个月高强度）

```
周 1       阶段0：原理打底 + 手撸 Agent 循环 + JD 收集
周 2-3     阶段1：LangGraph+LlamaIndex 应用层 + RAG
周 4-6     阶段2：Go harness 内核 MVP（重头戏）
周 7-9     阶段3：eval + 可观测 + 成本优化
全程穿插   理论模块（MoE/RL/Transformer）+ B 线刷题
弹性进阶   子 Agent 派发 / SWE-bench / LoRA 微调
周 9-10    项目深挖稿 + 模拟面试 + 投递
```

## 11. 风险预案

- **理论拖累进度**：理论模块严格限时（每概念 ≤ 半天），只求「能讲+能用」，不深挖数学。
- **Go harness 卡壳**：阶段 1 的 LangGraph 是参照系，卡住时回看它怎么做。
- **贪多求全**：弹性进阶项「核心做完才碰」，宁可主线深、不要支线散。
- **零基础焦虑**：每阶段都有可演示产出，用「做出来了」对冲焦虑。

## 12. 最终交付物

1. `AiFlowScript`：Go harness 内核 + Python 应用层的完整可运行项目。
2. 一份自建 eval benchmark + trace/成本可观测层及优化对比数据。
3. 一套「Go → AI Agent / Harness」面试讲述材料（JD 逆推清单 + 分层题库 + 项目深挖稿）。
4. 理论模块（MoE/RL/Transformer/微调）面试速答笔记。

## 13. 弹性进阶项（核心完成后再做）

- 子 Agent 派发（阶段 2）。
- SWE-bench Lite 子集刷分（阶段 3）。
- LoRA 极简微调实践（理论模块）。
