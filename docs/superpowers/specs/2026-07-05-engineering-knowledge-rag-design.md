# 工程知识库 RAG Agent 设计

## 目标

在 `AiFlowScript` 仓库中创建一个新的生产化学习项目：`engineering-knowledge-rag/`。

项目面向从 Go 后端转向 AI Agent 工程的学习目标，通过一个真实案例快速实践 LangChain、LangGraph 和 LangSmith：面向研发知识库的 RAG Agent。

第一版是 CLI 应用。它需要索引仓库内指定文档，基于引用来源回答问题，用 LangGraph 暴露 RAG 状态机，并把关键节点 trace 上报到 LangSmith，用于调试和 eval 对比。后续版本可以把同一套核心 graph 暴露为 FastAPI 服务。

项目不定位为通用 LangChain 教程，而是一个可在面试中讲清楚的生产实践项目。重点不是「调用了 RAG chain」，而是检索质量、引用治理、低置信度处理、badcase 归因、eval 回归，以及从 CLI adapter 演进到 API adapter 的工程边界。

## 范围

第一版包含：

- 新的顶层子项目：`engineering-knowledge-rag/`
- 仅面向 CLI 的用户入口
- 仓库文档索引
- 本地向量索引
- chat model 和 embedding 的双 provider 支持
- 基于 LangGraph 的 RAG 工作流
- LangSmith tracing
- smoke eval 数据集与运行器
- 架构、eval 策略和面试讲法文档

第一版不包含：

- FastAPI 服务
- 代码文件索引
- PDF 解析
- 网页抓取
- 多用户鉴权
- 异步任务管理
- 生产部署配置

## 知识源

第一版只索引仓库内已经是文本形态的文档和学习笔记。

初始 allowlist：

```text
README.md
CLAUDE.md
agent-loop/README.md
fast-api-demo/README.md
learning-resources/resources.md
docs/superpowers/specs/*.md
```

这样可以让 MVP 聚焦在 RAG 工作流质量上，避免被文件解析兼容性拖慢。代码文件、PDF 文件和外部网页作为后续扩展。

## 目录结构

```text
engineering-knowledge-rag/
├── README.md
├── pyproject.toml
├── .env.example
├── docs/
│   ├── architecture.md
│   ├── interview-notes.md
│   └── eval-strategy.md
├── src/
│   └── engineering_knowledge_rag/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── documents.py
│       ├── embeddings.py
│       ├── llms.py
│       ├── vectorstore.py
│       ├── graph.py
│       ├── prompts.py
│       └── evals.py
├── tests/
│   ├── test_documents.py
│   ├── test_graph_state.py
│   └── test_citations.py
└── data/
    ├── indexes/
    └── evals/
        └── smoke.jsonl
```

`cli.py` 是 adapter，只负责命令行入口，不承载 RAG 业务逻辑。

`graph.py` 负责 LangGraph 状态机。

`documents.py` 负责文档发现、读取、归一化和 chunking。

`llms.py` 和 `embeddings.py` 负责 provider 适配。

`vectorstore.py` 负责本地索引。

这个结构为后续 FastAPI adapter 预留清晰边界。FastAPI 不需要重写 RAG 主流程，只需要复用 graph 和 provider 配置。

## 架构

三个框架的职责需要明确拆开：

- LangChain：文档加载、文本切分、embedding、向量索引集成、prompt template 和 LLM adapter。
- LangGraph：有状态的 RAG 工作流编排。
- LangSmith：trace、badcase 归因和 eval 对比。

代码和文档都要让这个分工可见。面试讲法是：LangChain 提供组件，LangGraph 提供可控的工作流状态，LangSmith 提供可观测性。

## 模型 Provider

项目需要同时支持 Ollama 和 OpenAI-compatible API。

默认开发模式：

```env
MODEL_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL=qwen3:14b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

OpenAI-compatible 模式：

```env
MODEL_PROVIDER=openai
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=
OPENAI_CHAT_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

LangSmith 配置：

```env
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=engineering-knowledge-rag
```

配置层需要把 provider 差异隔离在 `graph.py` 之外。面试讲法：本地 Ollama 适合低成本、隐私友好的开发环境；OpenAI-compatible API 更适合效果稳定的生产环境。provider 边界让同一套 graph 可以运行在两种模式下。

## CLI

第一版命令：

```bash
uv run rag ingest
uv run rag ask "这个仓库的 Agent 学习路线是什么？"
uv run rag eval
uv run rag doctor
```

`ingest` 扫描 allowlist 文档、切分文本、生成 embedding，并写入本地向量索引。

`ask` 执行 LangGraph 工作流，并在终端输出：

- answer
- citations
- confidence
- warnings
- 可用时展示 trace metadata

`eval` 运行 `data/evals/smoke.jsonl`，输出简洁报告。

`doctor` 检查：

- model provider 配置
- Ollama 或 OpenAI-compatible 连通性
- LangSmith 环境变量
- 本地索引是否存在
- eval 数据集是否存在

## LangGraph 工作流

第一版不做简单的 `retrieve -> answer` 一步式 chain，而是把 RAG 过程暴露为状态机：

```text
user question
  -> rewrite_query
  -> retrieve
  -> grade_documents
  -> generate_answer
  -> verify_citations
  -> decide_final_response
```

### Graph State

```text
question
rewritten_query
retrieved_docs
graded_docs
answer
citations
confidence
warnings
trace_metadata
```

### 节点职责

`rewrite_query`

把用户问题改写成更适合匹配仓库文档的 query。例如 `这个仓库怎么学 Agent` 可以改写为 `AiFlowScript Agent learning roadmap agent-loop learning resources`。

面试要点：query rewrite 用来缓解用户自然语言和文档表达之间的词汇不匹配。

`retrieve`

从本地向量索引召回候选 chunk。每个结果必须包含 chunk text、`source_path`、`chunk_id` 和 similarity score。

面试要点：召回结果必须携带 source metadata，否则后续无法做引用和问题归因。

`grade_documents`

在生成答案前过滤无关 chunk。第一版可以组合 similarity threshold 和轻量 LLM relevance judge。

面试要点：生产化 RAG 不能把所有召回内容都塞进模型。过滤可以减少噪声，提高答案质量。

`generate_answer`

只基于通过筛选的 chunk 生成答案。prompt 必须要求引用来源，并要求模型在仓库文档证据不足时明确说明。

面试要点：答案生成受检索证据约束，而不是依赖模型自由发挥。

`verify_citations`

检查所有引用来源是否存在于 `retrieved_docs` 或 `graded_docs` 中。第一版校验 source path 是否有效；后续版本可以增加句子级证据匹配。

面试要点：citation verification 可以防止模型编造来源，给系统增加结果治理层。

`decide_final_response`

根据检索质量、引用有效性和 warnings，返回正常答案、低置信度答案、拒答或重新索引建议。

面试要点：这类似后端服务中的结果控制层，不应该把不可靠的模型输出直接返回。

## Eval 策略

创建 `data/evals/smoke.jsonl`，包含 5 到 8 个固定问题。

初始问题覆盖：

- 仓库学习路线
- `agent-loop` 项目的目标
- 为什么仓库强调先理解 Agent Loop，再学习框架
- 已有学习资源和外部链接
- 应该触发拒答的超范围问题

Eval 不只检查是否有答案文本，还要报告可解释的质量门槛：

```text
answer_present
citation_present
citation_valid
refusal_correct
```

第一版优先使用确定性检查。LLM-as-judge 作为后续扩展。

LangSmith trace 需要和 eval run 关联，便于持续对比 badcase。

## 测试

测试聚焦以下文件：

`tests/test_documents.py`

- 只扫描 allowlist 范围
- 安全读取 Markdown 和类 HTML 文本
- 每个 chunk 都保留 `source_path` 和 `chunk_id`

`tests/test_citations.py`

- 接受来自 retrieved sources 的引用
- 标记伪造引用
- 将无引用答案标记为低置信度

`tests/test_graph_state.py`

- 创建完整的初始 graph state
- 将低召回 case 路由到低置信度或拒答行为
- 验证节点输出可以被下游节点消费

测试优先覆盖 document metadata、citation validation 和 state transition 等确定性逻辑。依赖网络的模型调用需要隔离在 provider 接口之后，单元测试使用 fake provider。

## 文档交付物

子项目必须包含面向面试复述的文档，而不只是使用说明。

`README.md`

- 项目定位
- quick start
- 命令列表
- 架构摘要
- 项目亮点
- MVP 边界

`docs/architecture.md`

- LangChain、LangGraph 和 LangSmith 的职责
- graph state 和节点设计
- 数据流
- provider 适配
- CLI 到 FastAPI 的演进边界

`docs/interview-notes.md`

需要明确覆盖：

1. 项目解决的真实问题。
2. 为什么这不是普通 RAG Demo。
3. LangChain、LangGraph 和 LangSmith 分别解决什么问题。
4. 引用溯源和低置信度处理如何工作。
5. 如何定位 badcase。
6. 真正上线生产前还需要补哪些能力。
7. 面试官可能追问的问题和回答提纲。

`docs/eval-strategy.md`

- smoke eval 设计
- citation validation
- refusal checks
- 后续 LLM-as-judge 扩展
- 后续人工标注数据集扩展

## 面试讲法

项目可以这样表达：

```text
我做了一个面向研发知识库的 RAG Agent，用来回答开发者学习仓库里的项目结构、学习路线和技术资料问题。
LangChain 负责文档处理、embedding、向量检索、prompt 和模型适配。
LangGraph 把 RAG 过程拆成可调试的状态机，包括 query rewrite、retrieval、document grading、answer generation、citation verification 和 final response control。
LangSmith 记录每个节点的 trace，所以答案质量不好时，可以判断问题出在 query rewrite、retrieval、grading、generation 还是 citation verification。
第一版暴露 CLI，便于快速迭代。核心 graph 不依赖入口层，后续 FastAPI 服务可以复用它，不需要重写 RAG 工作流。
```

面试中需要主动讲到的项目亮点：

- 项目区分了组件使用和工作流编排。
- 引用溯源是一等可靠性要求，不是展示用的小功能。
- 系统有低置信度和拒答路径，而不是任何问题都强行回答。
- Eval 会检查引用有效性和拒答行为。
- 通过配置同时支持本地模型和云端模型。
- CLI 是第一版 adapter，不是核心架构本身。

## 后续演进

Phase 2：

- FastAPI adapter，提供 `/query`、`/ingest` 和 `/health`
- streaming answer endpoint
- 结构化 response schema

Phase 3：

- 代码文件索引
- 面向代码的 chunk strategy
- 代码仓库助手用例

Phase 4：

- PDF ingestion
- 更丰富的 eval 数据集
- LLM-as-judge scoring
- 人工标注 badcase set

## 成功标准

第一版完成标准：

- `uv run rag doctor` 能清晰报告配置状态。
- `uv run rag ingest` 能基于 allowlist 文档构建本地索引。
- `uv run rag ask` 能返回带有效引用的答案。
- 超范围问题能产生低置信度或拒答响应。
- `uv run rag eval` 能运行 smoke 数据集并报告质量门槛。
- LangSmith trace 能展示节点级输入和输出。
- README 和 docs 能讲清楚项目的面试表达。
