#!/usr/bin/env python3
"""Build a polished, single-file, offline HTML summary for BV1zSDMBUE5o.
Self-contained: base64 screenshots + inlined mermaid.min.js. No external deps at runtime.
"""
import base64
import html as html_mod
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
MERMAID_JS_PATH = Path("/Users/bytedance/.agents/skills/bilibili-video-summary/assets/mermaid.min.js")

# ---------------------------------------------------------------- helpers
def esc(s) -> str:
    return html_mod.escape(str(s))

def img_data_uri(rel: str) -> str:
    p = WORK / rel
    data = base64.b64encode(p.read_bytes()).decode("ascii")
    ext = p.suffix.lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    return f"data:{mime};base64,{data}"

def figure(rel: str, caption: str = "") -> str:
    if not (WORK / rel).exists():
        return f'<figure class="shot"><div class="missing">图片缺失：{esc(rel)}</div></figure>'
    cap = f'<figcaption>{esc(caption)}</figcaption>' if caption else ""
    return f'<figure class="shot"><img loading="lazy" src="{img_data_uri(rel)}" alt="{esc(caption)}">{cap}</figure>'

def mermaid(code: str) -> str:
    return f'<div class="mermaid-box"><pre class="mermaid">{code}</pre></div>'

# ---------------------------------------------------------------- meta
META = {
    "title": "近年 AI 应用技术串讲与优质文档分享",
    "subtitle": "Agent、Skill、OpenClaw、Harness……一条脉络讲清 2017→今",
    "up": "堂吉诃德拉曼查的英豪",
    "duration": "33:45",
    "url": "https://www.bilibili.com/video/BV1zSDMBUE5o/",
    "bvid": "BV1zSDMBUE5o",
}

OVERVIEW = (
    "这是一期「AI 应用技术串讲」：UP 主用一条清晰的时间线，把近些年工程同学绕不开的关键技术节点"
    "——从大模型基石 Transformer，一路讲到 Prompt 工程、微调、RAG、Function Call、MCP、Agent、"
    "Multi-Agent、上下文工程、Agent Skill、OpenClaw（小龙虾）、以及最近重新火起来的 Harness 驾驭工程"
    "——串成了一个完整的认知框架，并顺手分享了每个节点背后他认为最优质的文档与论文。"
    "全片主要面向工程同学，也适合所有对 AI 感兴趣的朋友。"
)

# 作者的两点方法论（题外话）
PHILOSOPHY = [
    ("掌握背景比追新名词更重要",
     "AI 应用领域的名词迭代太快，「学海无涯、回头是岸」，是学不完的。与其追新词，不如把脉络想清楚："
     "把自己放到某个具体时间节点，去想——在此之前从业者做事会遇到什么问题？为什么某个方案会成为"
     "标准协议 / 行业共识 / 最佳实践？它解决了什么、又遗留了什么？后来出现的新东西补齐了什么、自身又有哪些局限？"),
    ("工程与算法息息相关",
     "工程领域的发展和模型、算法能力的提升是紧密关联的。工程同学也应多了解算法的基本原理与前沿动态——"
     "它会影响你在耗时、效果等工程细节上的技术决策，也能帮你更深地理解基础工程概念。"),
]

# ---------------------------------------------------------------- 思维脑图（mindmap）
MINDMAP = """mindmap
  root((近年 AI 应用<br/>技术脉络))
    一 基石
      LLM 与 Transformer
      Decoder-only 成为主流
    二 让模型答得更好
      Prompt Engineering 提示词工程
      Fine-tuning 微调 与 LoRA
      RAG 检索增强生成
    三 赋予模型行动力
      Function Call 函数调用
      MCP 模型上下文协议
    四 走向自主智能体
      Agent 与 ReAct Loop
      Multi-Agent 多智能体
      Context Engineering 上下文工程
    五 复用与规模化
      Agent Skill 技能协议
      OpenClaw 小龙虾
      Harness 驾驭工程
"""

# ---------------------------------------------------------------- 演进主线（framework flowchart）
FRAMEWORK = """flowchart TD
  classDef base fill:#eef2ff,stroke:#6366f1,color:#3730a3;
  classDef better fill:#ecfdf5,stroke:#10b981,color:#065f46;
  classDef act fill:#fff7ed,stroke:#f59e0b,color:#92400e;
  classDef auto fill:#eff6ff,stroke:#3b82f6,color:#1e3a8a;
  classDef scale fill:#fdf2f8,stroke:#ec4899,color:#9d174e;

  LLM["① LLM · Transformer 2017<br/>大模型时代基石"]:::base
  PE["② Prompt 提示词工程<br/>调输出质量，但受限于上下文窗口"]:::better
  FT["③ Fine-tuning 微调<br/>LoRA 降本；但慢、贵、易被 SOTA 反超"]:::better
  RAG["④ RAG 检索增强<br/>轻量注入私有知识 · 抑制幻觉"]:::better
  FC["⑤ Function Call 函数调用<br/>给模型一双手"]:::act
  MCP["⑥ MCP 模型上下文协议<br/>工具跨应用复用"]:::act
  AGT["⑦ Agent · ReAct Loop<br/>思考-行动-观察 自主闭环"]:::auto
  MA["⑧ Multi-Agent 多智能体<br/>按上下文边界拆分"]:::auto
  CE["⑨ Context Engineering<br/>写/选/压/隔 管理上下文"]:::auto
  SK["⑩ Agent Skill 技能<br/>文件夹即 Agent · 渐进式加载"]:::scale
  OC["⑪ OpenClaw 小龙虾<br/>本地私人 AI 助手 · 产品破圈"]:::scale
  HN["⑫ Harness 驾驭工程<br/>人类掌舵 · 智能体执行"]:::scale

  LLM --> PE --> FT --> RAG
  RAG -->|"仍只是 Chatbot 不会动手"| FC
  FC -->|"工具重复开发"| MCP
  MCP --> AGT
  AGT -->|"单体上下文/工具过载"| MA
  AGT -->|"循环中数据爆炸"| CE
  MA --> SK
  CE --> SK
  SK --> OC
  SK --> HN
"""

# ---------------------------------------------------------------- 12 个章节
SECTIONS = [
    {
        "num": "01", "zh": "LLM 与 Transformer", "en": "Attention Is All You Need · 2017",
        "shot": "frames/scene_005.jpg", "shot_cap": "视频中的「LLM 演进树」与 Transformer 三种变体",
        "tagline": "一切的起点：盘古开天的那篇论文。",
        "points": [
            "2017 年 Google 发表《Attention Is All You Need》，首次提出 Transformer 架构，是大模型时代的开山之作；直到今天绝大多数模型仍基于该架构。",
            "Transformer 整体分两大部分：左边编码器 Encoder、右边解码器 Decoder。",
            "编码器像「只管阅读」的选手，负责把用户输入转成机器能理解的数学表示；解码器像「专门写作」的选手，根据理解生成最终输出。",
            "2018 年 OpenAI 在 GPT-1 中发现：干掉编码器、只保留解码器（Decoder-only），模型在创作生成类任务上表现更强。",
            "此后市面上绝大多数模型沿用 GPT 思路，采用 Decoder-only 架构——这也是 Transformer 的三种变体（Encoder-only / Encoder-Decoder / Decoder-only）中最主流的一支。",
        ],
        "diagram": """flowchart LR
  T["Transformer 2017"] --> ENC["Encoder 编码器<br/>只管阅读 → 数学表示"]
  T --> DEC["Decoder 解码器<br/>专门写作 → 生成输出"]
  DEC --> G["GPT-1 2018<br/>只留解码器"]
  G --> D["Decoder-only<br/>当今最主流变体"]
""",
        "refs": [("Attention Is All You Need（Transformer 原论文）", "https://arxiv.org/abs/1706.03762")],
    },
    {
        "num": "02", "zh": "Prompt Engineering 提示词工程", "en": "Prompt Engineering",
        "shot": "frames/scene_017.jpg", "shot_cap": "文档中 Prompt / Fine-tuning / RAG 的分节与推荐链接",
        "tagline": "同一个模型、同一个对话框，为什么有人拿到的结果质量更好？",
        "points": [
            "有了大模型后涌现出大量 Chatbot（聊天机器人），这是人们与大模型交互的最初形态。",
            "同样的模型、同样的对话框，输出质量差异来自「提示词工程的艺术」。",
            "提示词工程并不简单，真正调过 PE 的人都知道很痛苦，涉及不少技术手段与技巧。",
            "经典技巧如 Few-shot（小样本提示）：在提示词中注入少量标准答案示例，可显著提升输出质量，并能有效约束模型按期望的格式输出。",
            "局限：提示词工程只能优化输出质量，且受限于大模型有限的上下文（输入）窗口——无法把整个领域的知识、或训练阶段没见过的私有知识都塞给模型。",
        ],
        "diagram": """flowchart LR
  U["用户提问"] --> P["精心设计的提示词<br/>+ Few-shot 示例"]
  P --> M["大模型"]
  M --> O["更高质量 · 格式可控的输出"]
  L["局限：受上下文窗口限制<br/>无法灌入海量/私有知识"] -.-> P
""",
        "refs": [("提示词工程笔记（UP 主非常推荐的博客）", "https://www.aeasystone.com/archives/2024/01/prompt-engineering-notes.html")],
    },
    {
        "num": "03", "zh": "Fine-tuning 微调", "en": "LoRA · Low-Rank Adaptation",
        "shot": None, "shot_cap": "",
        "tagline": "想让模型真正「学会」私有知识？训练它。但代价不小。",
        "points": [
            "2021 年的 LoRA 论文是重点：最大贡献之一是把微调这件「高成本、高耗时」的事的算力成本压了下来。",
            "微调因此走向千家万户，每个小团队都能调一下，不再是「富人的游戏」。",
            "但工程落地中微调并非任何时刻都理想：① 需要训练模型、需要 GPU / 卡、成本高；② 需投入人力准备与清洗数据集、跑训练，耗时周期长、迭代慢。",
            "更扎心的一点：这两年基座大模型迭代太快——你还拿着上一版基座调了几个月，人家反手出个新的 SOTA，在你想微调的细分领域、以及其它领域都把你干掉了。",
            "于是问题变成：如果只是想让模型拥有一些私有知识，有没有更轻的平替方案？（引出 RAG）",
        ],
        "diagram": """flowchart TD
  FT["Fine-tuning 微调<br/>LoRA 降低算力成本"]
  FT --> A["✅ 真正改变模型参数<br/>让模型掌握私有知识"]
  FT --> B["❌ 需 GPU、成本高"]
  FT --> C["❌ 备数据/清洗/训练，周期长迭代慢"]
  FT --> D["❌ 基座迭代太快<br/>调完可能已被新 SOTA 反超"]
""",
        "refs": [("LoRA: Low-Rank Adaptation of Large Language Models", "https://arxiv.org/abs/2106.09685")],
    },
    {
        "num": "04", "zh": "RAG 检索增强生成", "en": "Retrieval-Augmented Generation",
        "shot": "frames/scene_020.jpg", "shot_cap": "文档中的 RAG 时序图：生产链路 + 消费链路",
        "tagline": "不动模型参数，也能让它带着「真实可信的资料」回答。",
        "points": [
            "RAG（Retrieval-Augmented Generation，检索增强生成）与微调是两回事：它最初是为解决大模型的「幻觉」问题。",
            "生产链路（建库）：把自己的文档先切片 → 做向量化（embedding）→ 存入向量数据库，也就是知识库。",
            "消费链路：用户输入提示词 → 请求打到服务端 → 服务端对用户请求做 embedding（转成向量）→ 用该向量去向量数据库召回相关的文本片段。",
            "召回后：把用户输入与召回的相关片段拼接（增强上下文）→ 再发给模型 → 模型基于以上信息生成回复。正好对应「检索 - 增强 - 生成」三步。",
            "收益：回答能带上真实可信的参考信息，甚至标注来源，大幅减少幻觉；相比微调更轻量、成本低廉得多、落地快得多。",
            "局限：RAG 没有改变模型任何参数，也没让模型更聪明，作用有限；且真正用好 RAG 很难——切片怎么切、多模态数据怎么入库、用什么 embedding 模型、检索方式怎么选、请求与库内相似度低时怎么处理，处处是门道。",
        ],
        "diagram": """flowchart LR
  subgraph PROD["生产链路（建库）"]
    DOC["私有文档"] --> CH["切片"] --> EM["向量化 embedding"] --> VDB[("向量数据库/知识库")]
  end
  subgraph CONS["消费链路（问答）"]
    Q["用户提问"] --> QE["请求 embedding"] --> RC["向量检索：召回相关片段"]
    Q --> AUG["拼接增强上下文"]
    RC --> AUG --> LLM["大模型生成回复<br/>可标注来源 · 抑制幻觉"]
  end
  VDB -. 召回 .-> RC
""",
        "refs": [("Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", "https://arxiv.org/abs/2005.11401")],
    },
    {
        "num": "05", "zh": "Function Call 函数调用", "en": "OpenAI Function Calling",
        "shot": "frames/scene_022.jpg", "shot_cap": "文档中的 Function Call 时序图",
        "tagline": "另起一条线：让只会聊天的模型，长出「一双手」。",
        "points": [
            "前面所有动作（PE / 微调 / RAG）都是让模型「答得更好」，但归根结底它还是个 Chatbot，只能聊天，没法帮你做更多操作。",
            "为了让模型有「动手能力」、能操作工具，出现了 Function Call。可参考 OpenAI 的官方协议文档。",
            "原理：① 用户提问；② 在提示词里约束模型返回规定格式的调用指令（通常是 JSON，含要调用的函数名与参数）。",
            "③ 模型按规范写好调用指令后，服务端反序列化这个 JSON、解析指令，去实现真正的函数调用；④ 拿到结果后，再发起第二轮 LLM Call，让模型根据返回结果继续后续回答。",
            "本质：通过工程手段巧妙实现「模型调用工具」——模型只负责「说」（决定调什么），服务端负责「做」（真正执行）。",
        ],
        "diagram": """sequenceDiagram
  autonumber
  participant U as 用户
  participant A as AI应用/服务端
  participant M as 大模型
  participant T as 外部工具/函数
  U->>A: 发起提问
  A->>M: 提问 + 约束返回规定格式(JSON)
  M-->>A: 返回调用指令 JSON（函数名 + 参数）
  A->>T: 反序列化并真正调用函数
  T-->>A: 返回执行结果
  A->>M: 第二轮 LLM Call（带上结果）
  M-->>A: 基于结果生成最终回答
  A-->>U: 返回回复
""",
        "refs": [("OpenAI Function Calling 官方文档", "https://platform.openai.com/docs/guides/function-calling")],
    },
    {
        "num": "06", "zh": "MCP 模型上下文协议", "en": "Model Context Protocol · Anthropic 2024.11",
        "shot": "frames/scene_024.jpg", "shot_cap": "文档中的 MCP 时序图（MCP Host / Client / Server）",
        "tagline": "Function Call 遍地开花后，工具能不能像插件一样被大家共享？",
        "points": [
            "有了 Function Call，大家纷纷给自己的 AI 应用接入外部能力；但很多外部能力其实是可复用的重复性工作。",
            "举例：你们老板让做「异常请求 AI 自动归因」，隔壁团队要做「异常指标自动告警监控」，两个团队都需要同一个能力——查日志（让模型输出查日志的 Function Call，返回结果再塞回模型）。",
            "为减少功能的重复开发、实现通用 Function Call 能力的共享，出现了 MCP（Model Context Protocol，模型上下文协议）。",
            "MCP 是 Anthropic（Claude 的母公司）于 2024 年 11 月提出的协议规范，此后火了大概一年多；很多公司都在建自己的 MCP Hub，在公司内部实现工具复用。",
            "所谓协议，无非是「大家都遵循同一规范」：遵循该协议开发出的可供 Function Call 的工具，可被任何适配了该协议的 AI 应用使用——对工具开发者和 AI 应用开发者都非常友好，也促进了社区生态繁荣。",
        ],
        "diagram": """flowchart TD
  subgraph BEFORE["没有 MCP：各自造轮子"]
    T1["团队A 自研查日志工具"]
    T2["团队B 又写一遍查日志"]
  end
  subgraph AFTER["有了 MCP：一次开发，处处复用"]
    S["MCP Server<br/>（查日志等能力）"]
    S --> H1["适配 MCP 的 AI 应用 1"]
    S --> H2["适配 MCP 的 AI 应用 2"]
    S --> H3["公司内部 MCP Hub"]
  end
  BEFORE -. 抽象为统一协议 .-> AFTER
""",
        "refs": [("Model Context Protocol 官网", "https://modelcontextprotocol.io/")],
    },
    {
        "num": "07", "zh": "Agent 智能体", "en": "ReAct · Think–Act–Observe Loop",
        "shot": "frames/scene_026.jpg", "shot_cap": "文档中引用的 ReAct 论文（Agent 的起点）",
        "tagline": "从「会聊天 + 会动手」到「像同事一样自主完成任务」。",
        "points": [
            "定义很多，简单说：在前面基础上，我们让 AI 能更好地聊天、也能操作外部工具/访问外部数据；但仅到此，AI 还不能像同事一样代替我们工作。",
            "类比实习生：给他明确目标和材料，他会自己拿目标 → 做计划 → 结合手上的工具与资源去完成；遇到环境跑不通、接口报错、不会配置等问题，他会去看报错、再进行下一步处理——这是一个循环。",
            "人类做事就是：思考任务目标 → 根据目标行动 → 观察行动结果，在不断与环境交互中逐步达成计划。Agent 要模拟的正是这个「思考-行动-观察」循环，即著名的 Agent Loop。",
            "强烈推荐 ReAct Agent 论文，非常重要：后面会遇到各种各样的 Agent、设计模式、Multi-Agent 架构，但本质上一个 Agent 就是 ReAct Agent，它是一切的起点。可以说「提示词 + LLM + Tools」就构成一个最简单的 Agent。",
            "示例（AI 排障）：Thinking 列计划 → 调用注册的 Function Call / MCP tools（看告警、看日志）拿数据 → 数据喂回主脑模型做 Observation → 再思考下一步是否换个工具深入。若认为已定位问题就结束循环（结束节点由大模型控制输出）；若不够就回到循环起点继续。",
            "设计模式：从 ReAct Agent 出发大致分两条线——侧重「规划（planning）」的 Agent 与侧重「反思（reflection）」的 Agent；UP 推荐了相关博客做延伸阅读。",
        ],
        "diagram": """flowchart LR
  G["任务目标"] --> TH["Thinking 思考<br/>列计划"]
  TH --> AC["Action 行动<br/>调用 Function Call 或 MCP 工具"]
  AC --> OB["Observation 观察<br/>结果喂回主脑模型"]
  OB --> DE{"已定位/达成目标?"}
  DE -- "否，继续" --> TH
  DE -- "是" --> EN["结束循环<br/>（由大模型判定输出）"]
""",
        "refs": [
            ("ReAct: Synergizing Reasoning and Acting in Language Models", "https://arxiv.org/abs/2210.03629"),
            ("AI Agent 设计模式综述（Medium）", "https://medium.com/@binome/ai-agent-workflow-design-patterns-an-overview-cf9e1f609696"),
        ],
    },
    {
        "num": "08", "zh": "Multi-Agent 多智能体", "en": "When (and when not) to use Multi-Agent",
        "shot": "frames/scene_044.jpg", "shot_cap": "Anthropic：关于何时使用多智能体的文章",
        "tagline": "一个 Agent 解决不了所有问题吗？——但多智能体也常被滥用。",
        "points": [
            "起因（至少前几年）：模型能力有限。① 上下文窗口有限；② 给的东西太多太杂会陷入混乱，出现注意力分散/稀释；③ 给同一个 Agent 注册两三个工具还行，注册五十上百个工具基本会「挑不准」。",
            "所以过去常用 Multi-Agent 架构实现复杂系统。经典（但被点名的）反面例子：自动写需求系统里，子 Agent1 读代码、子 Agent2 写代码、子 Agent3 review 代码——UP 强调这是经典 bad case，不要学。",
            "Anthropic 文章背景：他们发现多 Agent 架构如今有点泛滥，自己团队也曾投入数月构建复杂多 Agent，最终却退回单 Agent，再进一步优化提示词、优化工具描述，反而效果更好。",
            "多 Agent 优于单 Agent 的三种情况：① 业务存在上下文爆炸/污染导致模型智力下降，需要多个子 Agent 相互隔离上下文；② 任务可并行运行，用多 Agent 提速；③ 拆分不同子 Agent 能改善工具决策效果、或让任务更聚焦。不属于这三种就要慎重。",
            "常见工程错误：喜欢「按职能/工作类型」拆子 Agent（一个写码、一个测试、一个 review）——这种模式下大量 Token 都消耗在互相解释上下文、解释彼此的工作上。",
            "正确姿势：按「上下文隔离的边界」划分——谁掌握信息谁就把这块负责到底；只有当任务所需的背景信息/上下文知识完全不同时，才考虑拆成不同子 Agent。一句话：团队协作里「拉通对齐」的精力，有时远比实际干活更费劲。",
        ],
        "diagram": """flowchart TD
  Q{"何时用 Multi-Agent?"}
  Q --> C1["① 上下文爆炸/污染<br/>→ 子 Agent 相互隔离上下文"]
  Q --> C2["② 任务可并行<br/>→ 多 Agent 提速"]
  Q --> C3["③ 拆分改善工具决策/更聚焦"]
  W["❌ 按职能拆：读码/写码/评审<br/>Token 都耗在互相解释上下文"]
  R["✅ 按上下文隔离边界拆<br/>谁掌握信息谁负责到底"]
  W -. 纠正为 .-> R
""",
        "refs": [("Building multi-agent systems: when and how to use them（Anthropic）", "https://www.anthropic.com/engineering/building-multi-agent-research-system")],
    },
    {
        "num": "09", "zh": "Context Engineering 上下文工程", "en": "Write / Select / Compress / Isolate",
        "shot": "frames/scene_048.jpg", "shot_cap": "LangChain：Context Engineering（UP 认为比 Anthropic 那篇更好）",
        "tagline": "Agent 循环里数据越滚越多——到底该把什么放进下一轮上下文窗口？",
        "points": [
            "UP 认为 LangChain 这篇比 Anthropic 那篇写得更好。",
            "什么是上下文工程：在 Agent 循环运行中会产生越来越多与下一轮推理相关的数据——系统提示词、用户提示词、历史对话、工具描述、每轮工具调用返回的结果、状态信息、RAG 召回的数据等等。",
            "上下文工程就是：如何把这些海量信息筛选、提炼，精确选取合适的信息放入下一轮模型调用的上下文窗口，以获得最好的返回结果。",
            "为什么不能把全量信息一股脑丢进去？① 上下文窗口有限（老生常谈）——比如日志一返回就几万个 Token，来几个直接把窗口干崩，得做压缩裁剪。",
            "② 更重要的是效果：Transformer 基于自注意力机制，要求每个 Token 都要和输入里其它所有 Token 建立关系；你每多给一个 Token，都是在消耗模型本已有限的注意力资源。上下文越长注意力被稀释得越严重，模型越难找到最关键的信息（冗余上下文影响注意力、有毒上下文影响决策等）。",
            "怎么做：LangChain 把上下文工程的管理分成四部分——写上下文（Write）、选择上下文（Select）、压缩上下文（Compress）、隔离上下文（Isolate）。",
        ],
        "diagram": """flowchart LR
  SRC["循环中不断产生的数据<br/>系统/用户提示词 · 历史 · 工具描述<br/>工具结果 · 状态 · RAG 数据"] --> CE["上下文工程"]
  CE --> W["Write 写"]
  CE --> S["Select 选择"]
  CE --> C["Compress 压缩"]
  CE --> I["Isolate 隔离"]
  W & S & C & I --> WIN["精选后放入<br/>下一轮上下文窗口"]
  WIN --> BEST["更优的模型决策与输出"]
""",
        "refs": [
            ("Context Engineering（LangChain）", "https://blog.langchain.com/context-engineering-for-agents/"),
            ("Effective context engineering for AI agents（Anthropic）", "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"),
        ],
    },
    {
        "num": "10", "zh": "Agent Skill 技能", "en": "Claude Agent Skills · Progressive Disclosure",
        "shot": "frames/scene_058.jpg", "shot_cap": "UP 的进阶文档《从技术迭代的视角理解 Agent Skill》大纲",
        "tagline": "回到初心：一个文件夹，就是一个可分享、可复用的 Agent。",
        "points": [
            "先想「站在此刻还有哪些问题没解决」：最经典的是上下文爆炸——几乎每个做 Agent 的团队都遇到过。",
            "亮点设计一：基于文件系统的渐进式加载。提示词不再在用户请求时一次性全量塞给模型，而是以文件系统形式分门别类存放，只有需要某部分提示词时才把它拉进上下文；这个查找过程也是一种 agentic search——让 AI 直接看到文件结构，自己一层层翻找需要哪部分提示词。",
            "亮点设计二：Agent 的整体可复用/可分享。MCP 实现了「工具」的复用，但 Skill 想实现整个 Agent 的复用——把一整个 Agent 需要的东西打包成一个文件夹，甚至不懂 AI 的人都能通过微信发文件直接分享；对方在 Cursor / Claude Code 里合适位置解压，立刻就能用上、体验这个 Agent。",
            "对比过去的痛：工程团队要在不同框架里接入新 Agent 逻辑，可能得把代码洗一遍、再配 MCP 工具、抄一遍提示词；非专业用户则用扣子等低代码平台手动搭建、复制提示词、重配所有工具——Agent 分享一直没那么容易。",
            "Skill 是什么：Anthropic（Claude 母公司）去年提出的新概念。每个 Skill 本质就是一个文件夹，最重要的文件是 SKILL.md，里面放名称、描述，以及类似系统提示词的内容——规定这个 Skill 能做什么、怎么执行脚本、什么时候读引用文件、什么时候用静态资源（对应文件夹里的各类内容）。",
            "运作流程（渐进式披露）：把下载的多个 Skill 文件夹放到能被 Claude Code / Cursor 等本地 coding agent 扫描的位置 → 启动时它把所有可用 Skill 的「名称+描述」塞进主导模型的系统提示词 → 你发请求时，主导模型判断请求是否匹配某个技能 → 若相关性强就「激活」：把该 SKILL.md 的全部内容加载进上下文（此前只加载了名称+描述）→ 运行中按 SKILL.md 指示去读 reference 里的文件、或启动 sandbox 执行 script 脚本、拿返回数据继续完成任务。",
            "更深入的 Skill 与 SubAgent、与 MCP 的区别、以及工程中的 Skill 实现，UP 留到了下一期视频。",
        ],
        "diagram": """flowchart TD
  DL["下载多个 Skill 文件夹<br/>放到可被扫描的位置"] --> BOOT["coding agent 启动<br/>仅加载各 Skill 名称+描述<br/>塞进系统提示词"]
  BOOT --> REQ["用户发起请求"]
  REQ --> MATCH{"请求匹配某技能?"}
  MATCH -- "相关性强" --> ACT["激活：加载整份 SKILL.md 进上下文"]
  ACT --> REF["按需读取 references/ 文件"]
  ACT --> SCR["按需在 Sandbox 执行 scripts/ 脚本"]
  REF & SCR --> DONE["拿返回数据继续完成任务"]
  MATCH -- "不相关" --> SKIP["不加载，节省上下文"]
""",
        "refs": [
            ("Equipping agents for the real world with Agent Skills（Anthropic）", "https://www.anthropic.com/news/agent-skills"),
            ("Agent Skills 官方文档", "https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview"),
            ("agentskills.io", "https://agentskills.io/home"),
            ("Claude Skills 深度剖析（全生命周期原理）", "https://feehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive"),
        ],
    },
    {
        "num": "11", "zh": "OpenClaw 小龙虾", "en": "Local Personal AI Assistant",
        "shot": "frames/scene_061.jpg", "shot_cap": "文档中的 OpenClaw 小节与参考链接（含 NanoBot）",
        "tagline": "技术上没什么突破，但产品与交互上足够「破圈」。",
        "points": [
            "OpenClaw（小龙虾）本质是一个运行在你电脑本地的个人 AI 助手，有点类似 Siri。",
            "UP 认为它在技术上没什么特别值得展开、也没什么突破性创新；它的创新主要在产品、理念、交互层面。",
            "比如可以通过飞书等对人类特别友好的入口和你的 Agent 交互，去操作你自己的电脑、帮你完成很多私人任务——这对很多原本不了解 Agent 领域、其它行业的朋友是很新奇的体验，也造就了这次小龙虾的出圈。",
            "回到技术，值得看看它的上下文管理、记忆管理这块代码；但必须提醒：它的代码实在太长了，感觉都是 AI 写的。",
            "替代学习路径：推荐黄超老师的 NanoBot 项目——用约 1% 的代码实现了 90% 以上的功能，核心代码只有几千行，是一个 mini 版 OpenClaw，适合用来了解基本技术原理。",
        ],
        "diagram": """flowchart LR
  ENTRY["人类友好入口<br/>如飞书"] --> OC["OpenClaw<br/>本地个人 AI 助手"]
  OC --> PC["操作你自己的电脑<br/>完成私人任务"]
  OC -. 创新点 .-> INNO["产品 / 理念 / 交互<br/>（非技术突破）→ 破圈"]
  OC -. 想读原理? .-> NANO["NanoBot：1% 代码 90% 功能<br/>mini 版 OpenClaw"]
""",
        "refs": [("NanoBot（mini 版 OpenClaw）", "https://github.com/HKUDS/nanobot")],
    },
    {
        "num": "12", "zh": "Harness 驾驭工程", "en": "Harness Engineering · OpenAI",
        "shot": "frames/scene_063.jpg", "shot_cap": "视频中的「12. Harness Engineering」小节",
        "tagline": "AI 越聪明，人类越要学会「掌舵」而非「拆需求」。",
        "points": [
            "应运而生：即便有了前面这么多东西，你仍很难做到「丢个需求给 Agent，让它跑 8 小时代码、第二天来验收」。不驾驭的话，AI 就像一匹脱缰野马——一觉醒来它可能已经跑到一千公里以外，非常可怕。",
            "OpenAI 文章里的例子：他们通过「人类掌舵、智能体执行」，用几周时间交付了一个 100 万行代码的项目，且基本都是 AI 编写；并提到未来很可能要重新定义工程师的角色、重新定义人与 AI 的协作交互方式。",
            "什么是 Harness：随着 AI 越来越聪明，人类不再是把需求拆得极细、指着具体代码位置告诉它 1-2-3 怎么改，而是在宏观上做四件事。",
            "① 约束智能体：告诉它能做什么、边界在哪、必须依赖什么规则、在什么范围内改动。",
            "② 提供尽可能完整的上下文：项目迭代背景、完整需求文档、代码架构概述等都塞给它——很多时候 AI 做错并不一定是笨，而是像不知道上下文的人一样容易写 bug、踩坑。",
            "③ 验证 Agent 是否正确完成任务：比如让它写完每个接口都自己写符合预期的单测；或让 AI 自己把代码推到流水线部署起来，看会不会编译/报错。",
            "④ 科学的循环系统：出错时能第一时间给予反馈、保障 Agent 自我修复、重新回到正确轨道。",
            "落地细节：要提高代码可读性。AI 改不好代码的一个典型场景是「屎山代码」——不把当初写这行代码的人拉来问清逻辑与历史背景，可能这辈子都想不明白；人做不到的事别指望 AI 做到。所以应创建一个 AI-friendly 的环境，让它更好地开展工作。",
            "归根结底：工程师要学会改变与 AI 的协作模式，从而最大化发挥 Agent 潜力、提升效率。",
        ],
        "diagram": """flowchart TD
  H["Harness 驾驭工程<br/>人类掌舵 · 智能体执行"]
  H --> C1["① 约束<br/>能做什么·边界·规则·改动范围"]
  H --> C2["② 完整上下文<br/>迭代背景·需求文档·架构概述"]
  H --> C3["③ 验证<br/>写单测·推流水线·看是否报错"]
  H --> C4["④ 科学循环<br/>及时反馈·自我修复·回到正轨"]
  BASE["基础：AI-friendly 环境<br/>提高代码可读性 · 告别屎山"] --> H
""",
        "refs": [
            ("Harness Engineering（OpenAI）", "https://openai.com/zh-Hans-CN/index/harness-engineering/"),
        ],
    },
]

# ---------------------------------------------------------------- 结语 / 展望
OUTLOOK = {
    "title": "结语：技术冲击下，工程师的机会在哪里",
    "points": [
        "技术发展对行业的冲击确实比较严重，但事物要辩证看待：整体或许有缩减趋势，但也存在增量空间。",
        "增量一：AI 提效的应用与落地本身需要投入人力去建设，这个过程会持续一段时间。",
        "增量二：效率提升后代码变廉价，一些原来「不被看见」的需求会涌现出来——它们并非不存在。",
        "增量三：计算机行业只是一个开始，AI 在各行各业的落地会稍慢一步（不是每个行业都热衷自我革命）；懂技术、又握着最先进工具的人，在这波浪潮里能做的事更多、机会也更多。",
        "至于整个「赛博基建」完成之后的事，就交给以后考虑——每个时代都会有新的热点与机遇，且变化太快，几年前也没人料到是这般光景。",
    ],
}

# 完整参考文档清单（按视频顺序）
REFERENCES = [
    ("LLM · Transformer", [("Attention Is All You Need", "https://arxiv.org/abs/1706.03762")]),
    ("Prompt Engineering", [("提示词工程笔记（博客）", "https://www.aeasystone.com/archives/2024/01/prompt-engineering-notes.html")]),
    ("Fine-tuning", [("LoRA: Low-Rank Adaptation of Large Language Models", "https://arxiv.org/abs/2106.09685")]),
    ("RAG", [("Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", "https://arxiv.org/abs/2005.11401")]),
    ("Function Call", [("OpenAI Function Calling 文档", "https://platform.openai.com/docs/guides/function-calling")]),
    ("MCP", [("Model Context Protocol 官网", "https://modelcontextprotocol.io/")]),
    ("Agent", [
        ("ReAct 论文（arXiv:2210.03629）", "https://arxiv.org/abs/2210.03629"),
        ("AI Agent 设计模式综述（Medium）", "https://medium.com/@binome/ai-agent-workflow-design-patterns-an-overview-cf9e1f609696"),
    ]),
    ("Multi-Agent", [("Building multi-agent systems: when and how to use them（Anthropic）", "https://www.anthropic.com/engineering/building-multi-agent-research-system")]),
    ("Context Engineering", [
        ("Context Engineering（LangChain）", "https://blog.langchain.com/context-engineering-for-agents/"),
        ("Effective context engineering for AI agents（Anthropic）", "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"),
    ]),
    ("Agent Skill", [
        ("Equipping agents for the real world with Agent Skills（Anthropic）", "https://www.anthropic.com/news/agent-skills"),
        ("Agent Skills 官方文档", "https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview"),
        ("agentskills.io", "https://agentskills.io/home"),
        ("Claude Skills 深度剖析", "https://feehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive"),
    ]),
    ("OpenClaw", [("NanoBot（mini 版 OpenClaw）", "https://github.com/HKUDS/nanobot")]),
    ("Harness Engineering", [("Harness Engineering（OpenAI）", "https://openai.com/zh-Hans-CN/index/harness-engineering/")]),
    ("Claude Code 源码（延伸）", [
        ("claw-code", "https://github.com/instructkr/claw-code"),
        ("claude-code-fork", "https://github.com/hesreallyhim/claude-code-fork"),
    ]),
]

KEY_SHOTS = [
    ("frames/scene_005.jpg", "LLM 演进树与 Transformer 变体"),
    ("frames/scene_020.jpg", "RAG 生产/消费双链路时序图"),
    ("frames/scene_022.jpg", "Function Call 时序图"),
    ("frames/scene_024.jpg", "MCP 时序图"),
    ("frames/scene_046.jpg", "文档中完整的参考资料清单"),
    ("frames/scene_073.jpg", "OpenAI 关于 Harness 驾驭工程的文章"),
]

# ---------------------------------------------------------------- 渲染
def render_refs(refs):
    lis = "".join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t, u in refs)
    return f'<ul class="reflist">{lis}</ul>'

def render_section(s, idx):
    parts = [f'<article class="sec" id="sec-{s["num"]}">']
    parts.append(
        f'<div class="sec-head"><span class="badge">{s["num"]}</span>'
        f'<div class="sec-titles"><h2>{esc(s["zh"])}</h2>'
        f'<div class="en">{esc(s["en"])}</div></div></div>'
    )
    if s.get("tagline"):
        parts.append(f'<p class="tagline">{esc(s["tagline"])}</p>')
    parts.append("<ul class='points'>" + "".join(f"<li>{esc(p)}</li>" for p in s["points"]) + "</ul>")
    # 图与截图并排（截图可选）
    parts.append('<div class="media">')
    if s.get("diagram"):
        parts.append(mermaid(s["diagram"]))
    if s.get("shot"):
        parts.append(figure(s["shot"], s.get("shot_cap", "")))
    parts.append('</div>')
    if s.get("refs"):
        parts.append('<details class="sec-ref"><summary>本节参考文档</summary>' + render_refs(s["refs"]) + '</details>')
    parts.append('</article>')
    return "\n".join(parts)

def render_toc():
    items = "".join(
        f'<a href="#sec-{s["num"]}"><span>{s["num"]}</span>{esc(s["zh"])}</a>' for s in SECTIONS
    )
    return f'<nav class="toc">{items}</nav>'

def render_philosophy():
    cards = "".join(
        f'<div class="phi-card"><h4>{esc(t)}</h4><p>{esc(d)}</p></div>' for t, d in PHILOSOPHY
    )
    return f'<div class="phi">{cards}</div>'

def render_full_refs():
    blocks = []
    for group, refs in REFERENCES:
        blocks.append(f'<div class="refgroup"><h4>{esc(group)}</h4>{render_refs(refs)}</div>')
    return '<div class="refgrid">' + "".join(blocks) + '</div>'

def render_key_shots():
    figs = "".join(figure(rel, cap) for rel, cap in KEY_SHOTS)
    return f'<div class="gallery">{figs}</div>'

def render_outlook():
    lis = "".join(f"<li>{esc(p)}</li>" for p in OUTLOOK["points"])
    return f'<h2>{esc(OUTLOOK["title"])}</h2><ul class="points">{lis}</ul>'

def build():
    mermaid_js = MERMAID_JS_PATH.read_text(encoding="utf-8")
    sections_html = "\n".join(render_section(s, i) for i, s in enumerate(SECTIONS))
    html = TEMPLATE.format(
        title=esc(META["title"]),
        subtitle=esc(META["subtitle"]),
        up=esc(META["up"]),
        duration=esc(META["duration"]),
        url=esc(META["url"]),
        bvid=esc(META["bvid"]),
        overview=esc(OVERVIEW),
        philosophy=render_philosophy(),
        mindmap=mermaid(MINDMAP),
        framework=mermaid(FRAMEWORK),
        toc=render_toc(),
        sections=sections_html,
        outlook=render_outlook(),
        fullrefs=render_full_refs(),
        keyshots=render_key_shots(),
        mermaid_js=mermaid_js,
    )
    out = WORK / "AI应用技术串讲-Agent-Skill-OpenClaw-Harness.html"
    out.write_text(html, encoding="utf-8")
    print(f"✅ wrote {out} ({len(html)//1024} KB)")

TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}｜视频总结</title>
<style>
  :root{{
    --bg:#0b1020; --bg2:#0f1730; --panel:#141d38; --panel2:#18234a;
    --fg:#e8ecf8; --muted:#9aa6c8; --line:#26315c;
    --accent:#7c9cff; --accent2:#37e0c4; --amber:#ffb454; --rose:#ff7a9c;
    --shadow:0 10px 30px rgba(0,0,0,.35);
  }}
  *{{box-sizing:border-box}}
  html{{scroll-behavior:smooth}}
  body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Segoe UI",sans-serif;
       color:var(--fg);background:linear-gradient(180deg,#0a0f1f,#0b1020 40%,#0a0e1c);line-height:1.75;
       -webkit-font-smoothing:antialiased}}
  a{{color:var(--accent)}}
  .wrap{{max-width:960px;margin:0 auto;padding:0 20px 100px}}

  /* hero */
  .hero{{position:relative;padding:64px 20px 40px;text-align:center;overflow:hidden}}
  .hero::before{{content:"";position:absolute;inset:0;background:
     radial-gradient(60% 120% at 20% 0%,rgba(124,156,255,.22),transparent 60%),
     radial-gradient(50% 120% at 90% 10%,rgba(55,224,196,.16),transparent 60%);
     pointer-events:none}}
  .hero .kicker{{color:var(--accent2);font-weight:700;letter-spacing:.16em;font-size:.78rem;text-transform:uppercase}}
  .hero h1{{font-size:2.05rem;margin:.5rem auto .4rem;max-width:820px;line-height:1.3;
     background:linear-gradient(90deg,#fff,#c7d4ff);-webkit-background-clip:text;background-clip:text;color:transparent}}
  .hero .sub{{color:var(--muted);max-width:720px;margin:0 auto 18px;font-size:1.02rem}}
  .hero .metabar{{display:inline-flex;flex-wrap:wrap;gap:8px;justify-content:center}}
  .chip{{background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:5px 13px;font-size:.84rem;color:var(--muted)}}
  .chip a{{text-decoration:none}}
  .chip b{{color:var(--fg);font-weight:600}}

  section.block{{background:linear-gradient(180deg,var(--panel),var(--bg2));border:1px solid var(--line);
     border-radius:16px;padding:24px 26px;margin:22px 0;box-shadow:var(--shadow)}}
  h2{{font-size:1.35rem;margin:0 0 6px}}
  .lead-note{{color:var(--muted);font-size:.9rem;margin:-2px 0 16px}}
  .overview{{font-size:1.03rem;color:#dbe2fb}}

  /* philosophy */
  .phi{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}}
  .phi-card{{background:var(--panel2);border:1px solid var(--line);border-left:3px solid var(--accent2);
     border-radius:12px;padding:14px 16px}}
  .phi-card h4{{margin:0 0 6px;color:var(--accent2);font-size:1rem}}
  .phi-card p{{margin:0;color:#cbd5f5;font-size:.92rem}}

  /* toc */
  .toc{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:6px}}
  .toc a{{display:flex;align-items:center;gap:8px;background:var(--panel2);border:1px solid var(--line);
     border-radius:10px;padding:9px 12px;color:var(--fg);text-decoration:none;font-size:.9rem;transition:.15s}}
  .toc a:hover{{border-color:var(--accent);transform:translateY(-1px)}}
  .toc a span{{color:var(--accent);font-weight:700;font-variant-numeric:tabular-nums}}

  /* sections */
  .sec{{background:linear-gradient(180deg,var(--panel),var(--bg2));border:1px solid var(--line);
     border-radius:16px;padding:22px 24px;margin:18px 0;box-shadow:var(--shadow);scroll-margin-top:16px}}
  .sec-head{{display:flex;align-items:center;gap:14px;border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:6px}}
  .badge{{flex:0 0 auto;width:46px;height:46px;border-radius:12px;display:grid;place-items:center;
     font-weight:800;font-size:1.05rem;color:#0b1020;background:linear-gradient(135deg,var(--accent),var(--accent2))}}
  .sec-titles h2{{margin:0;font-size:1.28rem}}
  .sec-titles .en{{color:var(--muted);font-size:.82rem;letter-spacing:.04em}}
  .tagline{{color:var(--amber);font-weight:600;margin:12px 0 4px}}
  ul.points{{padding-left:20px;margin:10px 0}}
  ul.points li{{margin:7px 0;color:#dbe2fb}}
  ul.points li::marker{{color:var(--accent)}}

  .media{{display:flex;flex-direction:column;gap:14px;margin-top:8px}}
  .mermaid-box{{background:#f7f9ff;border:1px solid var(--line);border-radius:12px;padding:10px;overflow:auto}}
  .mermaid{{text-align:center}}
  figure.shot{{margin:0}}
  figure.shot img{{width:100%;border-radius:12px;border:1px solid var(--line);display:block}}
  figure.shot figcaption{{color:var(--muted);font-size:.82rem;text-align:center;margin-top:7px}}
  .missing{{padding:30px;text-align:center;color:var(--rose);border:1px dashed var(--line);border-radius:12px}}

  details.sec-ref{{margin-top:14px;background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:6px 14px}}
  details.sec-ref summary{{cursor:pointer;color:var(--accent2);font-size:.9rem;font-weight:600}}
  ul.reflist{{padding-left:20px;margin:8px 0}}
  ul.reflist li{{margin:5px 0;font-size:.9rem;word-break:break-all}}

  /* full refs */
  .refgrid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:8px}}
  .refgroup{{background:var(--panel2);border:1px solid var(--line);border-radius:12px;padding:12px 16px}}
  .refgroup h4{{margin:0 0 6px;color:var(--accent);font-size:.95rem}}

  /* gallery */
  .gallery{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px;margin-top:8px}}

  footer{{text-align:center;color:var(--muted);font-size:.85rem;margin-top:30px}}
  @media(max-width:720px){{
    .phi,.toc,.refgrid{{grid-template-columns:1fr}}
    .hero h1{{font-size:1.55rem}}
  }}
</style>
</head>
<body>
  <header class="hero">
    <div class="kicker">Bilibili · AI 应用技术串讲</div>
    <h1>{title}</h1>
    <p class="sub">{subtitle}</p>
    <div class="metabar">
      <span class="chip">UP 主：<b>{up}</b></span>
      <span class="chip">时长：<b>{duration}</b></span>
      <span class="chip"><b>{bvid}</b></span>
      <span class="chip"><a href="{url}" target="_blank" rel="noopener">▶ 原视频链接</a></span>
    </div>
  </header>

  <div class="wrap">
    <section class="block">
      <h2>一句话总览</h2>
      <p class="overview">{overview}</p>
      <h2 style="margin-top:22px">作者的两点方法论（贯穿全片）</h2>
      {philosophy}
    </section>

    <section class="block">
      <h2>🧠 思维脑图：全片知识架构</h2>
      <div class="lead-note">按「基石 → 让模型答得更好 → 赋予行动力 → 走向自主 → 复用与规模化」五个层次组织。</div>
      {mindmap}
    </section>

    <section class="block">
      <h2>🧭 演进主线：问题如何一步步被解决</h2>
      <div class="lead-note">每一步都在补齐上一步的遗留问题，同时带来新的局限——这正是作者建议的学习视角。</div>
      {framework}
    </section>

    <section class="block">
      <h2>📑 章节导航</h2>
      {toc}
    </section>

    {sections}

    <section class="block">
      {outlook}
    </section>

    <section class="block">
      <h2>📚 完整参考文档清单</h2>
      <div class="lead-note">视频中作者逐节分享的优质文档与论文（按出现顺序整理）。</div>
      {fullrefs}
    </section>

    <section class="block">
      <h2>🖼 关键截图</h2>
      {keyshots}
    </section>

    <footer>
      本页由视频字幕（whisper 转写）与关键帧截图整理而成 · 单文件离线可打开<br>
      内容版权归原 UP 主所有，仅作学习总结之用。
    </footer>
  </div>

<script>{mermaid_js}</script>
<script>
  mermaid.initialize({{ startOnLoad:true, theme:"neutral", securityLevel:"loose",
    themeVariables:{{ fontFamily:'-apple-system,"PingFang SC","Microsoft YaHei",sans-serif' }},
    flowchart:{{ htmlLabels:true, curve:"basis" }},
    mindmap:{{ padding:12 }} }});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
