# Go 服务端工程师的 FastAPI Agent Backend 进阶路线设计

## 1. 背景与定位

当前项目 `fast-api-demo` 是一个轻量 Python 脚手架：包含 `main.py`、`pyproject.toml`、空 `README.md` 和 Python 3.14 虚拟环境。当前 `main.py` 仅打印 Hello，`pyproject.toml` 还没有 FastAPI 依赖。

用户背景是普通 Go 服务端开发工程师，能看懂和编写简单 Python 脚本，但不熟 Python 工程化、异步模型、测试体系和 FastAPI。学习目标是快速从 0 开始精通 FastAPI，为后续 AI Agent 学习打基础，并形成面试或转岗时可讲述的项目经验。

本设计采用「渐进式工程化 Agent Backend」路线：先从普通 CRUD 服务开始掌握 FastAPI 基础，再重构为标准后端工程结构，最后自然演进为简化版 AI Agent 后端。

## 2. 最终方案

- 方案名称：Go 服务端工程师的 FastAPI Agent Backend 进阶路线。
- 副标题：用 4 周时间，从 FastAPI CRUD 演进到简化版 AI Agent 后端。
- 路线选择：渐进式工程化 Agent Backend 路线。
- 节奏选择：每天约 2 小时，持续 3-4 周，以 4 周完整路线为主。
- 项目定位：面试 / 转岗可讲述项目。

最终输出：

1. 一个可运行的 FastAPI Agent Backend Demo。
2. 一个本地单文件 HTML 学习路线设计稿。
3. 一套 Go → Python/FastAPI → Agent Backend 的面试讲述材料。

## 3. 学习目标

### 3.1 能写

学习完成后，应能独立实现：

- FastAPI 应用入口。
- APIRouter 路由拆分。
- Pydantic 请求和响应模型。
- Task CRUD API。
- service / repository 分层。
- SQLite 持久化。
- 配置、日志、异常处理。
- pytest + TestClient 测试。
- Conversation / Message API。
- Tool API。
- AgentRun API。
- SSE 流式事件接口。

### 3.2 能讲

学习完成后，应能讲清楚：

- FastAPI 和 Go Web 框架的异同。
- Pydantic 和 Go struct binding 的对应关系。
- FastAPI Depends 和 Go 显式依赖传递的差异。
- Python async/await 和 Go goroutine 的差异。
- 为什么 Agent 后端需要 conversation、message、run、tool、event。
- 为什么 SSE 适合 token streaming。
- 为什么先 mock LLM，再接真实 LLM。

### 3.3 能扩展

本项目完成后，可以自然扩展到真实 LLM Provider、LangGraph / LangChain、RAG、向量数据库、Redis 队列、Celery / Dramatiq、用户鉴权、WebSocket 和多 Agent 工作流。

## 4. 4 周学习路线

### 第 1 周：FastAPI 基础 + Python 工程补齐

目标：把当前 `fast-api-demo` 从 Hello 脚本变成能运行、能测试、结构清晰的 FastAPI 服务。

学习重点：虚拟环境和依赖管理、`pyproject.toml`、Python 包结构和 import 机制、类型注解、Pydantic 模型、`FastAPI()` 应用实例、path/query/body 参数、HTTPException、OpenAPI 自动文档、pytest 和 TestClient。

阶段 API：

```text
GET    /api/v1/health
GET    /api/v1/tasks
POST   /api/v1/tasks
GET    /api/v1/tasks/{task_id}
PUT    /api/v1/tasks/{task_id}
DELETE /api/v1/tasks/{task_id}
```

第 1 周先使用内存存储，不接数据库。重点是掌握 FastAPI 的基本开发模型。

每日安排：

- Day 1：安装 FastAPI / Uvicorn / pytest，写 `/health`，本地启动，打开 `/docs`。
- Day 2：学习 Pydantic，写 TaskCreate / TaskRead / TaskUpdate，实现内存版 Task CRUD。
- Day 3：学习 APIRouter，拆分 `app/main.py` 和 `app/api/routes`。
- Day 4：学习 HTTPException，统一错误响应格式，增加边界测试。
- Day 5：学习 pytest + TestClient，给 health 和 task CRUD 写测试。
- Day 6：复盘 Go 视角下的 FastAPI 基础，整理第一版面试讲法。

### 第 2 周：工程化分层 + 数据库 + 配置

目标：把第 1 周的内存 CRUD 重构成可维护的后端工程结构，引入数据库、配置、日志和分层。

学习重点：settings 配置管理、service / repository 分层、SQLite 开发环境、SQLAlchemy 或 SQLModel、Alembic 基础迁移、数据库 session 管理、FastAPI dependency injection、日志与异常边界。

阶段结构：

```text
app/
  main.py
  core/
    config.py
    logging.py
    exceptions.py
  api/
    deps.py
    routes/
      health.py
      tasks.py
  models/
  schemas/
  services/
  repositories/
  db/
tests/
```

每日安排：

- Day 1：重构项目结构，拆分 router、schema、service，保持测试通过。
- Day 2：引入配置系统，区分 dev / test 配置。
- Day 3：引入 SQLAlchemy / SQLModel，建 Task 表，实现 repository。
- Day 4：service 层调用 repository，API 层只负责协议转换，测试从内存改为测试数据库。
- Day 5：增加日志和统一异常处理，明确错误码和响应格式。
- Day 6：复盘 FastAPI 项目为什么要分层，输出第二版面试讲法。

### 第 3 周：Agent Backend 雏形

目标：在标准后端项目基础上，引入 Agent 所需的核心领域模型：Conversation、Message、Tool、AgentRun。

学习重点：会话建模、消息建模、工具抽象、mock LLM Provider、agent service 编排、背景任务、状态查询、SSE 基础。

阶段 API：

```text
POST /api/v1/conversations
GET  /api/v1/conversations/{conversation_id}
GET  /api/v1/conversations/{conversation_id}/messages
POST /api/v1/conversations/{conversation_id}/messages

GET  /api/v1/tools
POST /api/v1/agent/runs
GET  /api/v1/agent/runs/{run_id}
```

每日安排：

- Day 1：设计 Conversation / Message schema，实现会话和消息 API。
- Day 2：设计 Tool 抽象，内置当前时间、计算器、短文本总结 3 个 mock tool。
- Day 3：设计 mock LLM Provider，输入 messages，返回 assistant message。
- Day 4：设计 AgentRun，实现 run 创建和状态查询。
- Day 5：引入 BackgroundTasks 或 asyncio task，让 AgentRun 从 pending → running → succeeded / failed。
- Day 6：复盘 Agent Backend 和普通 CRUD 后端的差异，输出第三版面试讲法。

### 第 4 周：流式响应 + 测试完善 + 面试叙事

目标：把项目打磨成一个小而完整、能展示、能讲述的 FastAPI Agent Backend Demo。

学习重点：SSE StreamingResponse、流式 token 返回、异步生成器、错误处理、集成测试、HTML 学习路线设计稿、面试讲述结构。

阶段 API：

```text
POST /api/v1/agent/chat
GET  /api/v1/agent/runs/{run_id}/events
```

每日安排：

- Day 1：学习 StreamingResponse，实现最小 SSE demo。
- Day 2：把 mock LLM 改成 token generator，返回流式 token。
- Day 3：agent run 接入 SSE 事件，支持 run_started / token / run_succeeded。
- Day 4：补充 Agent 相关测试，测试异常场景。
- Day 5：整理项目结构，删除过度设计，固化最终接口说明。
- Day 6：形成 30 秒、2 分钟、深挖版本面试讲法，生成 HTML 学习路线设计稿。

## 5. 最终项目结构

最终建议演进成：

```text
fast-api-demo/
  pyproject.toml
  README.md
  app/
    __init__.py
    main.py
    api/
      __init__.py
      deps.py
      routes/
        __init__.py
        health.py
        tasks.py
        conversations.py
        agent.py
        tools.py
    core/
      __init__.py
      config.py
      logging.py
      exceptions.py
      responses.py
    db/
      __init__.py
      session.py
      base.py
    models/
      __init__.py
      task.py
      conversation.py
      message.py
      agent_run.py
    schemas/
      __init__.py
      task.py
      conversation.py
      message.py
      agent.py
      tool.py
    repositories/
      __init__.py
      task_repository.py
      conversation_repository.py
      message_repository.py
      agent_run_repository.py
    services/
      __init__.py
      task_service.py
      conversation_service.py
      agent_service.py
      tool_service.py
    llm/
      __init__.py
      base.py
      mock.py
    tools/
      __init__.py
      base.py
      builtin.py
  tests/
    test_health.py
    test_tasks.py
    test_conversations.py
    test_agent.py
```

## 6. 模块职责边界

- `app/main.py`：创建 FastAPI 应用、注册路由、异常处理器、中间件和生命周期事件，不写具体业务逻辑。
- `app/api/routes/`：HTTP 协议层，负责 URL、request、response、service 调用和业务异常到 HTTP 响应的映射。
- `app/schemas/`：API 输入输出模型、请求体、响应体、参数校验和 OpenAPI 文档生成。
- `app/models/`：数据库模型、表结构、字段类型和关系映射。
- `app/repositories/`：数据访问，封装数据库 session 和 CRUD 查询，不知道 HTTP，也不决定业务规则。
- `app/services/`：业务逻辑和业务编排，包括 Task、Conversation / Message、AgentRun、LLM Provider、ToolService 和业务异常。
- `app/core/`：配置、日志、异常、统一响应格式和常量。
- `app/db/`：engine、session factory、session dependency、base model 和 migration 支撑。
- `app/llm/`：LLM Provider 抽象，第一版实现 mock provider，后续可扩展真实模型。
- `app/tools/`：Agent 工具系统，包括 Tool 定义、输入 schema、执行逻辑和内置工具注册。

边界原则：API 层处理 HTTP，schema 层处理输入输出，service 层处理业务编排，repository 层处理数据访问，llm/tools 层提供 Agent 可替换能力，core/db 层提供基础设施。

## 7. 核心 API 设计

最终 API 分为 5 组：

```text
/api/v1/health
/api/v1/tasks
/api/v1/conversations
/api/v1/tools
/api/v1/agent
```

### 7.1 Health API

```text
GET /api/v1/health
```

响应：

```json
{
  "status": "ok",
  "service": "fast-api-agent-demo"
}
```

### 7.2 Task API

字段：

```text
Task
  - id: string
  - title: string
  - description: string | null
  - completed: bool
  - created_at: datetime
  - updated_at: datetime
```

接口：

```text
GET    /api/v1/tasks
POST   /api/v1/tasks
GET    /api/v1/tasks/{task_id}
PUT    /api/v1/tasks/{task_id}
DELETE /api/v1/tasks/{task_id}
```

### 7.3 Conversation / Message API

字段：

```text
Conversation
  - id: string
  - title: string
  - created_at: datetime
  - updated_at: datetime

Message
  - id: string
  - conversation_id: string
  - role: user | assistant | tool
  - content: string
  - created_at: datetime
```

接口：

```text
POST /api/v1/conversations
GET  /api/v1/conversations/{conversation_id}
GET  /api/v1/conversations/{conversation_id}/messages
POST /api/v1/conversations/{conversation_id}/messages
```

### 7.4 Tool API

字段：

```text
Tool
  - name: string
  - description: string
  - input_schema: dict
```

接口：

```text
GET /api/v1/tools
```

第一版内置工具：`get_current_time`、`calculator`、`summarize_text`。

### 7.5 Agent API

接口：

```text
POST /api/v1/agent/chat
POST /api/v1/agent/runs
GET  /api/v1/agent/runs/{run_id}
GET  /api/v1/agent/runs/{run_id}/events
```

AgentRun 状态机：

```text
pending -> running -> succeeded
pending -> running -> failed
```

第一版不做 cancel / retry。

## 8. Agent 内部流程

### 8.1 非流式 Chat 流程

```text
1. Client 调 POST /agent/chat
2. API 层校验请求
3. AgentService 保存 user message
4. AgentService 读取 conversation 历史消息
5. 调用 MockLLMProvider.generate()
6. 判断是否需要工具调用
7. 如需要，调用 ToolService.execute()
8. 生成 assistant message
9. 保存 assistant message
10. 返回响应
```

第一版规则：如果 message 包含「几点」「时间」，调用 `get_current_time`；如果 message 包含简单算式，调用 `calculator`；否则 mock LLM 返回普通文本。

### 8.2 异步 AgentRun 流程

```text
1. Client 调 POST /agent/runs
2. 创建 AgentRun，状态 pending
3. 后台任务开始执行
4. 状态改为 running
5. 保存 user message
6. 调用 mock LLM / tool
7. 保存 assistant message
8. 状态改为 succeeded
9. Client 通过 GET /agent/runs/{run_id} 查询结果
```

失败时，状态从 running 变为 failed，并写入 error。

### 8.3 SSE 流程

```text
1. Client 先 POST /agent/runs 创建 run
2. Client 连接 GET /agent/runs/{run_id}/events
3. 服务端持续发送 run_started、token、tool_called、tool_result、run_succeeded
4. Client 收到 run_succeeded 后关闭连接
```

第一版 SSE 可以不做复杂事件存储。可先用简单异步生成器模拟 token 流，后续再和 AgentRun 状态打通。

## 9. 测试策略

第 1 周测试 API 基础：`/health`、Task CRUD、404、422。

第 2 周测试分层和数据库：service 层业务逻辑、repository 层数据库操作、API 层集成测试、测试数据库隔离。

第 3 周测试 Agent 领域：创建 Conversation、保存 Message、Tool 列表、Tool 执行、mock LLM 生成、AgentRun 状态流转。

第 4 周测试流式和端到端：SSE media type、run_started / token / run_succeeded 事件、Agent Chat 端到端流程、异常场景下返回 run_failed。

## 10. 错误处理设计

错误处理分三层：API 参数错误、业务错误、系统错误。

API 参数错误由 Pydantic / FastAPI 自动处理，通常返回 422。validation 是 schema 层职责，不在 service 层重复校验所有字段。

业务错误由 service 抛出业务异常，再由 API 层或全局 exception handler 转成 HTTP 响应。典型业务错误包括 TaskNotFound、ConversationNotFound、AgentRunNotFound、ToolNotFound、ToolExecutionFailed。

统一业务错误响应：

```json
{
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task not found"
  }
}
```

系统错误包括数据库连接失败、未捕获异常、LLM Provider 失败、工具执行异常。处理原则是不把堆栈返回给客户端，服务端日志记录完整异常，客户端只收到统一错误结构。

统一系统错误响应：

```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "Internal server error"
  }
}
```

## 11. 阶段验收标准

第 1 周验收：服务可通过 `uvicorn app.main:app --reload` 启动，`GET /api/v1/health` 和 `GET /docs` 可访问，`pytest` 通过；能讲清楚 FastAPI app、APIRouter、Pydantic/OpenAPI、TestClient。

第 2 周验收：项目具备 `api -> service -> repository -> db` 分层，Task CRUD 使用数据库持久化；能讲清楚 API 层为什么不直接访问数据库、service 和 repository 边界、Depends 如何注入数据库 session、测试数据库如何隔离。

第 3 周验收：项目具备 Conversation、Message、Tool、MockLLMProvider、AgentRun；能讲清楚 Agent 后端为什么需要会话和消息、Tool abstraction 意义、AgentRun 状态、mock LLM 的学习价值。

第 4 周验收：项目具备 `GET /api/v1/agent/runs/{run_id}/events` 流式响应；能讲清楚 SSE 和 WebSocket 区别、StreamingResponse、异步生成器和 Agent 事件流。

## 12. 面试表达设计

### 12.1 30 秒版本

我做了一个渐进式 FastAPI Agent Backend Demo。项目从 Task CRUD 开始，先掌握 FastAPI 路由、Pydantic 校验和测试；然后重构为 API、service、repository、model 分层，并接入数据库；最后演进成 Agent 后端，支持 conversation、message、tool、agent run 和 SSE 流式事件。这个项目帮助我把 Go 服务端经验迁移到 Python/FastAPI，也为后续学习 AI Agent 框架打基础。

### 12.2 2 分钟版本

这个项目的设计思路是渐进式演进，而不是一开始套复杂模板。第一阶段，我用 Task CRUD 学 FastAPI 的基础，包括 APIRouter、Pydantic request/response model、HTTPException 和 TestClient。第二阶段，我把项目重构成 API、service、repository、model 分层，引入 SQLite 和配置管理，让 API 层只处理 HTTP，service 层处理业务，repository 层处理数据访问。第三阶段，我加入 Conversation 和 Message，把普通后端模型扩展成 Agent 上下文模型；再设计 Tool abstraction 和 MockLLMProvider，让 AgentService 编排模型调用和工具调用。最后，我用 AgentRun 和 SSE 事件流解决 Agent 后端常见的长任务状态查询和流式输出问题。

这个项目最大的价值是建立了 Go 到 Python/FastAPI 的迁移模型：Go 里常见的 handler/service/dao 分层，在 FastAPI 里可以映射为 routes/services/repositories；Go struct binding 可以映射到 Pydantic；context 和依赖传递可以通过 Depends 和显式参数管理；Python async/await 则更适合 I/O 密集型的 LLM 调用和流式响应。

### 12.3 深挖问题

**为什么选择 FastAPI？** FastAPI 对类型注解、Pydantic 校验和 OpenAPI 文档支持非常好，适合快速构建 API 服务。对 AI Agent 后端来说，请求/响应 schema、流式接口、依赖注入和 async I/O 都很重要，FastAPI 在这些方面比较轻量且工程化。

**FastAPI 和 Gin/Hertz 最大差异是什么？** Gin/Hertz 更偏显式路由和 handler 组织，参数绑定和校验通常需要手动组合；FastAPI 更依赖 Python 类型注解和 Pydantic，通过函数签名直接表达 path/query/body/dependency。Go 的优势是静态类型和并发模型稳定，FastAPI 的优势是 API schema 生成、开发效率和 async I/O 生态。

**为什么需要 service/repository 分层？** 如果 API 层直接访问数据库，后续加入 Agent 编排、工具调用、状态机时会变得难维护。service 层承载业务流程，repository 层封装数据访问，API 层只处理协议转换。这样测试也更清晰，可以分别测业务逻辑、数据访问和 HTTP 行为。

**为什么 AgentRun 需要状态机？** Agent 请求不一定是一次同步调用，它可能涉及 LLM 生成、工具调用、外部 API、甚至多步推理。AgentRun 用 pending/running/succeeded/failed 描述运行生命周期，前端可以查询状态，也可以订阅事件流。这个模型比简单 `/chat` 更接近真实 Agent 后端。

**为什么用 SSE？** 对 token 流和状态事件这种服务端到客户端的单向推送，SSE 比 WebSocket 更简单，兼容 HTTP 语义，也更容易测试和调试。WebSocket 适合双向实时通信，但会引入连接管理复杂度。这个项目的目标是掌握 Agent 后端基础，所以先用 SSE。

**为什么不用 LangChain / LangGraph？** 先理解 Agent 后端的底层边界：conversation、message、tool、provider、run、event stream。LangChain/LangGraph 是更高层框架，直接上会掩盖这些基础概念。等底层模型清楚后，再接 LangGraph 会更容易理解它解决了什么问题。

## 13. HTML 输出规格

用户期望最终采用 D → A/B 流程：先在对话里确认设计，再输出本地单文件 HTML，如有需要再部署为在线访问地址。

本地单文件路径：

```text
fast-api-demo/fastapi-agent-backend-roadmap.html
```

要求：单文件、可离线打开、不依赖外部 CDN、内联 CSS、可直接浏览器打开、后续可部署成在线地址。

页面风格：深色技术路线图、开发者阅读体验、卡片式布局、重点信息高亮、时间线推进、Go 与 FastAPI 对照表、AgentRun / SSE 流程图、面试话术模块。

页面包含 11 个区块：

1. Hero：从 Go 服务端到 FastAPI Agent Backend。
2. 当前起点：个人背景、项目状态、学习约束。
3. 三层能力目标：FastAPI 基础、Python 工程化、AI Agent 后端。
4. 4 周路线图。
5. 项目演进路径。
6. 最终架构图。
7. API 总览。
8. 核心数据模型。
9. Go ↔ FastAPI 概念对照。
10. 测试与验收标准。
11. 面试讲述模板。

## 14. 暂不纳入范围

第一版不做登录注册、JWT 鉴权、权限系统、多租户、真实 LLM SDK、LangChain / LangGraph、向量数据库、RAG、Redis 队列、WebSocket 和前端页面。

这些能力可以作为后续 AI Agent 深入路线继续扩展。当前重点是建立 FastAPI 工程化能力、Agent API 设计能力、SSE 流式响应能力和 service/provider/tool 分层意识。

## 15. 后续实施顺序

用户审阅本设计规格并确认后，下一步进入实施计划。实施计划应优先生成本地单文件 HTML 设计稿，再开始 FastAPI 项目代码实施。

建议顺序：

1. 生成 `fastapi-agent-backend-roadmap.html`。
2. 本地打开并检查视觉与内容。
3. 如用户需要，部署为在线可访问页面。
4. 从第 1 周目标开始实施 FastAPI 项目代码。
5. 每个阶段完成后运行测试并复盘面试讲法。

## 16. 规格自检结果

- 未保留 TBD、TODO 或未完成占位。
- 架构、接口、测试、HTML 输出规格保持一致。
- 范围聚焦于 FastAPI 工程化和 Agent Backend 基础，未纳入过重生态组件。
- 对「本地 HTML」与「在线 HTML」的关系已明确：先本地单文件，再按需部署在线。
