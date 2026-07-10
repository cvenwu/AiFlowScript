#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 32 集 summary.md 整合为单文件 HTML 学习手册。"""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(BASE), "langchain-langgraph-吴恩达系列学习手册.html")

# 四门课分组（集数范围 + 课程名）
COURSES = [
    ("第一门课 · LangChain 大语言模型应用开发", list(range(1, 9))),          # 1-8
    ("第二门课 · LangChain 的函数、工具与代理", list(range(9, 17))),         # 9-16
    ("第三门课 · 用 LangGraph 构建长期代理记忆", list(range(17, 24))),       # 17-23
    ("第四门课 · 吴恩达 LangGraph 中的 AI 代理", list(range(24, 33))),       # 24-32
]

def read_summary(i):
    p = os.path.join(BASE, f"p{i:02d}", "summary.md")
    with open(p, encoding="utf-8") as f:
        return f.read()

def get_title(md):
    m = re.match(r"#\s*(.+)", md.strip())
    return m.group(1).strip() if m else f"第{i}集"

def get_theme(md):
    # 提取“核心主题:”一句话
    m = re.search(r"核心主题[:：]\s*(.+)", md)
    return m.group(1).strip() if m else ""

def get_timerange(md):
    m = re.search(r"时间范围[:：]\s*(.+)", md)
    return m.group(1).strip() if m else ""

chapters = []
for i in range(1, 33):
    md = read_summary(i)
    title = get_title(md)
    chapters.append({
        "n": i,
        "title": title,
        "theme": get_theme(md),
        "time": get_timerange(md),
        "md": md,
    })

DATA_JSON = json.dumps(chapters, ensure_ascii=False)

# 目录分组结构（供侧栏与总览用）
nav_groups = []
for cname, nums in COURSES:
    items = [{"n": c["n"], "title": c["title"]} for c in chapters if c["n"] in nums]
    nav_groups.append({"course": cname, "items": items})
NAV_JSON = json.dumps(nav_groups, ensure_ascii=False)

# ============ HTML 模板 ============
HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>吴恩达 LangChain + LangGraph 系列学习手册（32 集完整版）</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11.9.0/styles/atom-one-light.min.css" id="hljs-light">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11.9.0/styles/atom-one-dark.min.css" id="hljs-dark" disabled>
<style>
:root{
  --bg:#faf8f4; --panel:#ffffff; --text:#2b2b2b; --muted:#666; --accent:#2b6cb0; --accent2:#c05621;
  --code-bg:#282c34; --code-fg:#e6e6e6; --border:#e6e2da; --hi-yellow:#fff5cc; --hi-red:#ffe6e0;
  --hi-green:#e6f5e0; --shadow:0 2px 8px rgba(0,0,0,.06);
}
:root[data-theme=dark]{
  --bg:#1a1a1a; --panel:#242424; --text:#e8e8e8; --muted:#aaa; --accent:#7ab8ff; --accent2:#ff9955;
  --code-bg:#0f0f0f; --code-fg:#e8e8e8; --border:#333; --hi-yellow:#4a3f1a; --hi-red:#4a2a24; --hi-green:#2a4a2a;
  --shadow:0 2px 8px rgba(0,0,0,.4);
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Helvetica Neue",Helvetica,Arial,sans-serif;line-height:1.75;font-size:15.5px;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.layout{display:flex;min-height:100vh}
/* 侧栏 */
.sidebar{position:sticky;top:0;height:100vh;width:290px;flex-shrink:0;overflow-y:auto;background:var(--panel);border-right:1px solid var(--border);padding:18px 14px;font-size:13.5px}
.sidebar h2{margin:0 0 12px;font-size:15px;color:var(--accent);border-bottom:1px solid var(--border);padding-bottom:8px}
.sidebar .group{margin-bottom:14px}
.sidebar .group>.gtitle{font-weight:600;color:var(--accent2);padding:6px 4px;cursor:pointer;user-select:none;border-radius:4px}
.sidebar .group>.gtitle:hover{background:var(--border)}
.sidebar .group>.gtitle::before{content:"▼ ";font-size:10px}
.sidebar .group.collapsed>.gtitle::before{content:"▶ "}
.sidebar .group.collapsed ul{display:none}
.sidebar ul{list-style:none;padding-left:8px;margin:4px 0}
.sidebar li{padding:2px 0}
.sidebar li a{display:block;padding:4px 8px;border-radius:4px;color:var(--text)}
.sidebar li a:hover{background:var(--border);text-decoration:none}
.sidebar li a.active{background:var(--accent);color:#fff}
.sidebar .meta{color:var(--muted);font-size:12px;padding:6px 4px;line-height:1.5}
/* 主体 */
.main{flex:1;padding:34px 44px;max-width:1080px;margin:0 auto;min-width:0}
.hero{background:linear-gradient(135deg,#2b6cb0 0%,#c05621 100%);color:#fff;padding:36px 34px;border-radius:14px;box-shadow:var(--shadow);margin-bottom:28px}
.hero h1{margin:0 0 12px;font-size:28px;line-height:1.35}
.hero .sub{opacity:.92;font-size:14.5px;line-height:1.7}
.hero .tags{margin-top:14px}
.hero .tag{display:inline-block;background:rgba(255,255,255,.2);padding:3px 10px;border-radius:12px;font-size:12.5px;margin:2px 6px 2px 0}
.card{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:22px 26px;margin-bottom:22px;box-shadow:var(--shadow)}
.card h2{margin-top:0;color:var(--accent);border-bottom:2px solid var(--border);padding-bottom:8px}
.card h3{color:var(--accent2);margin-top:22px}
.card h4{margin-top:16px}
.card ul,.card ol{padding-left:22px}
.card p{margin:10px 0}
.hi-key{background:var(--hi-yellow);padding:1px 4px;border-radius:3px}
.hi-warn{background:var(--hi-red);padding:1px 4px;border-radius:3px;font-weight:600}
.hi-ok{background:var(--hi-green);padding:1px 4px;border-radius:3px}
/* 章节 */
.chapter{background:var(--panel);border:1px solid var(--border);border-radius:10px;margin-bottom:22px;box-shadow:var(--shadow);overflow:hidden}
.chapter>header{padding:16px 24px;background:linear-gradient(90deg,rgba(43,108,176,.08),transparent);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:14px;cursor:pointer;user-select:none}
.chapter>header .badge{background:var(--accent);color:#fff;padding:3px 10px;border-radius:8px;font-size:13px;font-weight:600;flex-shrink:0}
.chapter>header h2{margin:0;font-size:19px;color:var(--text);flex:1;min-width:0}
.chapter>header .toggle{color:var(--muted);font-size:14px;font-family:monospace}
.chapter.collapsed>.content{display:none}
.chapter.collapsed>header .toggle::after{content:"▶"}
.chapter>header .toggle::after{content:"▼"}
.chapter>.content{padding:20px 28px}
.chapter .meta-line{color:var(--muted);font-size:13.5px;background:var(--bg);padding:8px 12px;border-radius:6px;margin-bottom:14px;border-left:3px solid var(--accent)}
/* markdown内的元素 */
.md h1{display:none}
.md h2{color:var(--accent);border-bottom:1px solid var(--border);padding-bottom:6px;margin-top:26px;font-size:20px}
.md h2::before{content:"🔹 ";}
.md h2:first-of-type::before{content:""}
.md h3{color:var(--accent2);margin-top:20px;font-size:17px}
.md strong{color:var(--accent2)}
.md ul,.md ol{padding-left:24px}
.md li{margin:4px 0}
.md blockquote{border-left:4px solid var(--accent);background:var(--bg);padding:8px 14px;color:var(--muted);margin:12px 0;border-radius:0 6px 6px 0}
.md p code,.md li code,.md td code{background:var(--hi-yellow);padding:1px 6px;border-radius:3px;font-family:"SF Mono",Menlo,Consolas,monospace;font-size:.92em;color:#c05621}
:root[data-theme=dark] .md p code,:root[data-theme=dark] .md li code,:root[data-theme=dark] .md td code{color:#ffb47a}
.md pre{background:var(--code-bg);color:var(--code-fg);padding:0;border-radius:8px;overflow-x:auto;margin:14px 0;box-shadow:var(--shadow);position:relative}
.md pre code{display:block;padding:14px 18px;font-family:"SF Mono",Menlo,Consolas,monospace;font-size:13.5px;line-height:1.65;background:transparent}
.md pre code.hljs{background:transparent}
.md table{border-collapse:collapse;margin:14px 0;box-shadow:var(--shadow);border-radius:6px;overflow:hidden}
.md th,.md td{border:1px solid var(--border);padding:8px 12px}
.md th{background:var(--bg);font-weight:600}
.mermaid-wrap{background:#fff;border:1px solid var(--border);border-radius:8px;padding:14px;margin:14px 0;box-shadow:var(--shadow);overflow-x:auto}
:root[data-theme=dark] .mermaid-wrap{background:#2c2c2c}
.mermaid{display:flex;justify-content:center}
/* 底部按钮 */
.fab{position:fixed;right:22px;bottom:22px;display:flex;flex-direction:column;gap:10px;z-index:100}
.fab button{width:44px;height:44px;border-radius:22px;border:none;background:var(--accent);color:#fff;font-size:18px;cursor:pointer;box-shadow:var(--shadow);transition:transform .15s}
.fab button:hover{transform:scale(1.08)}
.fab button#totop{background:var(--accent2)}
/* 移动端 */
.mobile-toggle{display:none;position:fixed;top:12px;left:12px;z-index:200;background:var(--accent);color:#fff;border:none;padding:8px 14px;border-radius:6px;font-size:14px;box-shadow:var(--shadow);cursor:pointer}
@media (max-width:900px){
  .sidebar{position:fixed;left:0;top:0;transform:translateX(-100%);transition:transform .25s;z-index:150;width:280px}
  .sidebar.open{transform:translateX(0)}
  .main{padding:60px 20px 34px}
  .mobile-toggle{display:block}
  .hero{padding:24px 20px}
  .hero h1{font-size:22px}
  .card{padding:16px 18px}
  .chapter>.content{padding:14px 18px}
}
</style>
</head>
<body>
<button class="mobile-toggle" onclick="document.querySelector('.sidebar').classList.toggle('open')">☰ 目录</button>
<div class="layout">
  <aside class="sidebar" id="sidebar">
    <h2>📖 目录导航</h2>
    <div class="meta">
      共 <strong>32</strong> 集 · 4 门课程<br>
      吴恩达 × LangChain 官方
    </div>
    <div id="nav"></div>
    <div style="margin-top:16px;padding-top:12px;border-top:1px solid var(--border)">
      <a href="#top">↑ 课程总览</a><br>
      <a href="#principles">🌱 第一性原理总纲</a><br>
      <a href="#chapters">📚 分章节正文</a><br>
      <a href="#summary">🎯 结尾汇总</a>
    </div>
  </aside>
  <main class="main">
    <a id="top"></a>
    <!-- Hero -->
    <section class="hero">
      <h1>吴恩达 × LangChain + LangGraph 系列学习手册</h1>
      <div class="sub">
        基于 B 站 BV1XFMA6EEVx 视频合集全 32 集英文原声字幕逐字提炼；覆盖<strong>四门 DeepLearning.AI 官方短课</strong>，从 LLM 应用开发基础 → 工具与代理 → 长期代理记忆 → LangGraph 中的 AI 代理，构建"从 0 到 1 熟练掌握大模型应用开发"的完整学习路径。
      </div>
      <div class="tags">
        <span class="tag">LangChain</span>
        <span class="tag">LangGraph</span>
        <span class="tag">LangMem</span>
        <span class="tag">Agents</span>
        <span class="tag">Function Calling</span>
        <span class="tag">RAG</span>
        <span class="tag">LCEL</span>
        <span class="tag">Tavily</span>
        <span class="tag">Python</span>
      </div>
    </section>

    <!-- 总览 -->
    <section class="card">
      <h2>🎯 核心价值速览</h2>
      <ul>
        <li><strong>能掌握什么：</strong>用 LangChain 组合 Model / Prompt / Parser / Memory / Chain / Agent 构建 LLM 应用；用 OpenAI Function Calling + LCEL 稳定生产结构化数据；用 LangGraph 编排带状态、可持久化、能人机协作、支持长期记忆的多步 Agent。</li>
        <li><strong>能解决什么问题：</strong>私有文档问答（RAG）、自动化助理（邮件/日历/工具调用）、多步推理任务（研究写作/评估/复核）、可上线的 Agent 系统（持久化 + 人工审批 + 时间旅行）。</li>
        <li><strong>适合什么人群：</strong>零基础到中级 Python 学习者；产品经理/工程师想快速上手大模型应用；已有 LangChain 使用经验、希望系统建立"第一性原理"的开发者。</li>
      </ul>

      <h2>🗺️ 整体知识体系架构图</h2>
      <div class="mermaid-wrap">
      <div class="mermaid">
graph TB
    ROOT["吴恩达 LangChain + LangGraph 系列<br/>32 集 · 4 门课"] --> C1
    ROOT --> C2
    ROOT --> C3
    ROOT --> C4
    C1["第一门课<br/>LangChain 应用开发基础<br/>(P1-P8)"] --> C1A["Models / Prompts / Parsers<br/>P2"]
    C1 --> C1B["Memory 四种记忆<br/>P3"]
    C1 --> C1C["Chains 链与路由<br/>P4"]
    C1 --> C1D["Q&A over Documents (RAG)<br/>P5"]
    C1 --> C1E["Evaluation 评估<br/>P6"]
    C1 --> C1F["Agents 推理引擎<br/>P7"]
    C2["第二门课<br/>Functions Tools Agents<br/>(P9-P16)"] --> C2A["OpenAI Function Calling<br/>P10"]
    C2 --> C2B["LCEL 表达式语言<br/>P11"]
    C2 --> C2C["Pydantic 生成函数<br/>P12"]
    C2 --> C2D["Tagging / Extraction<br/>P13"]
    C2 --> C2E["Tools & Routing<br/>P14"]
    C2 --> C2F["Conversational Agent<br/>P15"]
    C3["第三门课<br/>LangGraph 长期代理记忆<br/>(P17-P23)"] --> C3A["记忆三分类<br/>语义/情景/程序 P18"]
    C3 --> C3B["基线邮件助手<br/>P19"]
    C3 --> C3C["语义记忆 LangMem<br/>P20"]
    C3 --> C3D["情景记忆 少样本<br/>P21"]
    C3 --> C3E["程序记忆 自动调整提示词<br/>P22"]
    C4["第四门课<br/>LangGraph 中的 AI 代理<br/>(P24-P32)"] --> C4A["从头手写 ReAct 循环<br/>P25"]
    C4 --> C4B["用 LangGraph 实现 Agent<br/>P26"]
    C4 --> C4C["Agentic 搜索 Tavily<br/>P27"]
    C4 --> C4D["持久化 + 流式输出<br/>P28"]
    C4 --> C4E["Human in the Loop<br/>P29"]
    C4 --> C4F["Essay Writer 综合项目<br/>P30"]
    C4 --> C4G["进阶架构综述<br/>P32"]
    classDef root fill:#2b6cb0,color:#fff,stroke:#2b6cb0
    classDef c1 fill:#c6d9f0,stroke:#2b6cb0
    classDef c2 fill:#f6d4b6,stroke:#c05621
    classDef c3 fill:#d4edda,stroke:#2f7d3a
    classDef c4 fill:#e8dbf0,stroke:#7a3fa8
    class ROOT root
    class C1,C1A,C1B,C1C,C1D,C1E,C1F c1
    class C2,C2A,C2B,C2C,C2D,C2E,C2F c2
    class C3,C3A,C3B,C3C,C3D,C3E c3
    class C4,C4A,C4B,C4C,C4D,C4E,C4F,C4G c4
      </div>
      </div>

      <h2>📐 学习路径规划</h2>
      <table style="width:100%">
      <thead><tr><th>阶段</th><th>集数</th><th>难度</th><th>类别</th></tr></thead>
      <tbody>
      <tr><td>入门必学</td><td>P1-P8（第一门课全部）</td><td>★</td><td>建立 LangChain 六大组件体感</td></tr>
      <tr><td>入门必学</td><td>P10（Function Calling）· P11（LCEL）</td><td>★★</td><td>掌握"结构化输出"的现代方式</td></tr>
      <tr><td>进阶选学</td><td>P12-P15（Pydantic / Tools / Conversational Agent）</td><td>★★</td><td>组合能力，做出类 ChatGPT 应用</td></tr>
      <tr><td>进阶选学</td><td>P17-P23（记忆三分类 + LangMem 实战）</td><td>★★★</td><td>让 Agent 记住你</td></tr>
      <tr><td>精通深化</td><td>P24-P30（手写 Agent → LangGraph → 综合项目）</td><td>★★★★</td><td>真正掌握编排</td></tr>
      <tr><td>精通深化</td><td>P32（进阶架构综述）</td><td>★★★★</td><td>了解多代理/监督者/LATS 等主流方案</td></tr>
      </tbody>
      </table>
      <p style="margin-top:14px;color:var(--muted);font-size:13.5px">💡 <strong>建议节奏：</strong>入门每天 1-2 集边看边跑 notebook；进阶两天 1 集，重点动手改练习；精通配合官方 GitHub 与 LangSmith 一起做。</p>
    </section>

    <!-- 第一性原理总纲 -->
    <section class="card" id="principles">
      <h2>🌱 第一性原理总纲</h2>
      <h3>整套课程的底层本质</h3>
      <p>大语言模型（LLM）本质上是一个<span class="hi-key">"给定一段文本 → 输出下一段文本"</span>的无状态函数。它天生解决不了三件事：</p>
      <ol>
        <li><strong>反复使用需要脚手架</strong>：真实应用要多次调用、拼提示词、解析输出，每次手写太啰嗦。</li>
        <li><strong>调用外部世界要接口</strong>：模型自己不知今天日期、不会算术、不能读你的数据库，必须通过<span class="hi-key">工具（Tools）</span>把执行权交给程序。</li>
        <li><strong>多步任务要控制流</strong>：真实决策不是一次问答，而是"想→做→观察→再想"的循环，需要一个能<span class="hi-key">编排状态</span>的图。</li>
      </ol>
      <p>LangChain / LangGraph 这套课程的所有内容，都是围绕上面三条本质需求提供抽象：</p>

      <h3>五条底层公理</h3>
      <ol>
        <li><strong>公理 1 · 模型无状态</strong>：LLM 每次 API 调用彼此独立，"记忆"是应用层把历史拼进 prompt 制造出来的（对应 P3 / P17）。</li>
        <li><strong>公理 2 · 模型输出即字符串</strong>：即使看起来像 JSON，也必须解析后才能安全使用（对应 P2 输出解析器、P10 函数调用）。</li>
        <li><strong>公理 3 · 拼提示词就是拼字典</strong>：Prompt 是一个带占位符的模板，把变量填进去即可复用，不必为每种输入重写（对应 P2、P4）。</li>
        <li><strong>公理 4 · Agent = LLM + 循环 + 工具</strong>：Agent 本质是"模型推理 + 程序执行 + 结果回填"的 while 循环，任何 Agent 框架（AgentExecutor / LangGraph / ReAct）都只是这个循环的不同实现（对应 P7、P25、P26）。</li>
        <li><strong>公理 5 · 图 = 状态 + 节点 + 边</strong>：LangGraph 把 Agent 的控制流写成一张有向图，状态在节点间传递，条件边决定分支（对应 P26 及之后）。掌握了图，就等于掌握了任意复杂 Agent 的组装能力。</li>
      </ol>

      <h3>通用思考框架（碰到新问题时按此顺序问自己）</h3>
      <ol>
        <li>这个问题的<strong>输入是什么？期望的输出是什么？</strong>（决定 Prompt/Schema）</li>
        <li>模型自己能否闭环？还是需要<strong>外部工具/数据</strong>？（决定要不要 Tools/RAG）</li>
        <li>需要几步？<strong>一次成稿还是多轮迭代</strong>？（决定 Chain 还是 Agent/Graph）</li>
        <li>要不要跨轮记住？<strong>短期还是长期记忆？语义/情景/程序哪种？</strong>（决定 Memory 层设计）</li>
        <li>失败会不会有代价？<strong>要不要人工审批 / 可回溯</strong>？（决定 Human-in-the-Loop 与持久化）</li>
      </ol>
    </section>

    <a id="chapters"></a>
    <h2 style="border-bottom:2px solid var(--accent);padding-bottom:8px;margin:34px 0 20px;color:var(--accent)">📚 分章节正文（P1–P32）</h2>
    <div id="chapters-container"></div>

    <!-- 结尾汇总 -->
    <section class="card" id="summary">
      <h2>🎯 全系列核心知识清单（复习提纲）</h2>
      <h3>一、LangChain 六大核心组件</h3>
      <ul>
        <li><strong>Models</strong>：`ChatOpenAI(temperature=0)` 封装 LLM 调用，`temperature=0` 让输出可复现。</li>
        <li><strong>Prompts</strong>：`ChatPromptTemplate.from_template()` 用 `{变量}` 定义可复用模板。</li>
        <li><strong>Parsers</strong>：`StructuredOutputParser` / `JsonOutputFunctionsParser` 把字符串转成 Python 字典。</li>
        <li><strong>Memory</strong>：Buffer / Window / Token / Summary 四种权衡，本质都是把历史塞回 prompt。</li>
        <li><strong>Chains</strong>：LLMChain → SimpleSequentialChain → SequentialChain → RouterChain 组合难度递增。</li>
        <li><strong>Indexes / Retrievers</strong>：Loader + Splitter + Embeddings + VectorStore + Retriever 构成 RAG 五件套。</li>
      </ul>
      <h3>二、结构化输出与工具的现代做法</h3>
      <ul>
        <li>用 <strong>Pydantic BaseModel</strong> 定义 Schema，`convert_pydantic_to_openai_function` 转成 function schema。</li>
        <li>用 <strong>`model.bind(functions=..., function_call=...)`</strong> 强制/自动调用；用 `@tool` 装饰器一键做出工具。</li>
        <li>用 <strong>LCEL 管道符 `|`</strong> 组合 prompt / model / parser / retriever；`.bind()` 加参数、`.with_fallbacks()` 加回退。</li>
      </ul>
      <h3>三、Agent 与 LangGraph</h3>
      <ul>
        <li>Agent = <strong>LLM 大脑 + Runtime 手脚 + 循环</strong>。ReAct 模式：Thought → Action → Observation → …</li>
        <li>LangGraph = <strong>StateGraph（图）+ Node（节点）+ Edge / Conditional Edge（边）+ State（可累加状态）</strong>。</li>
        <li>关键能力：<strong>Persistence</strong>（SqliteSaver checkpointer）、<strong>Streaming</strong>（stream/astream_events）、<strong>Human in the Loop</strong>（interrupt_before + get_state/update_state/时间旅行）。</li>
      </ul>
      <h3>四、长期代理记忆（LangMem）</h3>
      <ul>
        <li><strong>语义记忆</strong>：事实（谁是谁），存 Store + vector index，用 `manage_memory` / `search_memory` 工具。</li>
        <li><strong>情景记忆</strong>：过往例子（few-shot），按 namespace `("email","<user>","examples")` 隔离。</li>
        <li><strong>程序记忆</strong>：提示词本身（如何做事），用 `create_multi_prompt_optimizer` 根据反馈自动调整。</li>
        <li>更新时机：<strong>热路径</strong>（即时但增延迟）vs <strong>后台</strong>（低延迟但非即时）。</li>
      </ul>

      <h2>🚀 实战落地建议</h2>
      <ol>
        <li><strong>第 1 周</strong>：跑通 P2-P5 的 notebook，能用 LangChain 完成"翻译邮件 → 抽取字段 → RAG 问答"三个 demo。</li>
        <li><strong>第 2 周</strong>：把 P10-P14 内容用 Pydantic + LCEL 重写一次，做出一个"抽取论文标题+作者"的抽取服务。</li>
        <li><strong>第 3 周</strong>：动手做出 P19-P22 的邮件助手，为它加上三种记忆，并接一个真实邮箱（可先 mock）。</li>
        <li><strong>第 4 周</strong>：跟着 P25-P30 从头写一个 Agent，再用 LangGraph 重写，加上持久化 + 人工审批，跑通"作文写手"。</li>
        <li><strong>持续</strong>：每次做完开 <strong>LangSmith</strong> 看 trace，用 <strong>Playground</strong> 调 prompt。</li>
      </ol>

      <h2>🌐 进阶拓展方向</h2>
      <ul>
        <li><strong>LangGraph 官方 how-to</strong>：涵盖 subgraph、branching、streaming events、interrupt 更细粒度用法。</li>
        <li><strong>LangSmith</strong>：调试、监控、数据集回归测试，是生产落地必备。</li>
        <li><strong>LangServe + Templates</strong>：一键把 chain / agent 部署成 REST API。</li>
        <li><strong>Prompt Hub</strong>：LangChain 官方 Prompt 分享社区，用来找灵感。</li>
        <li><strong>多代理架构</strong>：Multi-Agent（共享状态）、Supervisor（总管）、Plan-and-Execute、LATS（树搜索）——参见 P32。</li>
        <li><strong>研究前沿</strong>：AlphaCodium 类流程工程、Reflection Pattern、Toolformer/Function-Calling 训练。</li>
      </ul>
      <blockquote>
        💡 本手册严格基于 B 站合集 <strong>BV1XFMA6EEVx</strong> 全 32 集字幕原文提炼（其中 p27-p32 及 p15/p19-p26 使用 Whisper 转录）。所有代码/API 用法均出自视频讲解，不做超出原视频范围的引申。
      </blockquote>
    </section>
    <div style="text-align:center;color:var(--muted);font-size:13px;padding:18px 0">— 手册结束 · Happy Building —</div>
  </main>
</div>

<div class="fab">
  <button id="theme" title="明暗切换">🌓</button>
  <button id="totop" title="回到顶部">↑</button>
</div>

<!-- 依赖库：CDN -->
<script src="https://cdn.jsdelivr.net/npm/marked@11.1.1/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11.9.0/highlight.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.min.js"></script>

<!-- 数据 & 渲染逻辑 -->
<script>
const CHAPTERS = __DATA_JSON__;
const NAV = __NAV_JSON__;

// ---- 目录侧栏 ----
(function renderNav(){
  const nav = document.getElementById('nav');
  NAV.forEach((g, gi)=>{
    const gEl = document.createElement('div');
    gEl.className = 'group';
    const t = document.createElement('div');
    t.className = 'gtitle';
    t.textContent = g.course;
    t.onclick = ()=> gEl.classList.toggle('collapsed');
    gEl.appendChild(t);
    const ul = document.createElement('ul');
    g.items.forEach(it=>{
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = '#ch'+it.n;
      a.textContent = 'P'+it.n+' · '+it.title.replace(/^第\d+集[:：]?\s*/, '');
      li.appendChild(a); ul.appendChild(li);
    });
    gEl.appendChild(ul);
    nav.appendChild(gEl);
  });
})();

// ---- Marked 渲染 & 拦截 mermaid 代码块 ----
marked.setOptions({
  gfm: true, breaks: false,
  highlight: function(code, lang){
    try {
      if (lang && hljs.getLanguage(lang)) return hljs.highlight(code, {language: lang}).value;
      return hljs.highlightAuto(code).value;
    } catch(e){ return code; }
  }
});
// 自定义 renderer：mermaid 代码块转成 <div class="mermaid-wrap"><div class="mermaid">...</div></div>
const renderer = new marked.Renderer();
const origCode = renderer.code.bind(renderer);
renderer.code = function(code, lang){
  if (lang === 'mermaid') {
    return '<div class="mermaid-wrap"><div class="mermaid">'+code+'</div></div>';
  }
  return origCode(code, lang);
};
marked.use({renderer});

// ---- 章节渲染 ----
(function renderChapters(){
  const box = document.getElementById('chapters-container');
  CHAPTERS.forEach(ch=>{
    const wrap = document.createElement('article');
    wrap.className = 'chapter';
    wrap.id = 'ch'+ch.n;
    const header = document.createElement('header');
    header.innerHTML = '<span class="badge">P'+ch.n+'</span>'+
                       '<h2>'+ch.title.replace(/^第\d+集[:：]?\s*/, '')+'</h2>'+
                       '<span class="toggle"></span>';
    header.onclick = (e)=>{ wrap.classList.toggle('collapsed'); };
    wrap.appendChild(header);
    const content = document.createElement('div');
    content.className = 'content';
    let meta = '';
    if (ch.time) meta += '<span>⏱ 时间范围：<strong>'+ch.time+'</strong></span> &nbsp;·&nbsp; ';
    if (ch.theme) meta += '<span>🎯 '+ch.theme+'</span>';
    if (meta) content.innerHTML += '<div class="meta-line">'+meta+'</div>';
    const mdBox = document.createElement('div');
    mdBox.className = 'md';
    mdBox.innerHTML = marked.parse(ch.md);
    content.appendChild(mdBox);
    wrap.appendChild(content);
    box.appendChild(wrap);
  });
  // 代码块二次高亮（针对 renderer 未走 highlight 的情形）
  document.querySelectorAll('.md pre code').forEach(el=>{ try{ hljs.highlightElement(el); }catch(e){} });
})();

// ---- Mermaid 初始化（根据主题）----
function decodeEntities(s){
  const t = document.createElement('textarea');
  t.innerHTML = s;
  return t.value;
}
let mermaidSeq = 0;
async function initMermaid(){
  const isDark = document.documentElement.dataset.theme === 'dark';
  mermaid.initialize({startOnLoad:false, theme: isDark ? 'dark' : 'default', securityLevel:'loose', fontFamily:'inherit'});
  const els = [...document.querySelectorAll('.mermaid')];
  for (let i = 0; i < els.length; i++){
    const el = els[i];
    // 首次：保存原始图定义（保留 <br>，并解码 &gt; &amp; 等实体）
    if (el.dataset.raw === undefined){
      el.dataset.raw = decodeEntities(el.innerHTML.trim());
    }
    try{
      const { svg } = await mermaid.render('mmd-' + (mermaidSeq++), el.dataset.raw);
      el.innerHTML = svg;
    }catch(e){
      el.innerHTML = '<pre style="color:#c05621;font-size:12px">图表渲染失败，源码如下：\n' +
                     el.dataset.raw.replace(/</g,'&lt;') + '</pre>';
    }
  }
}
initMermaid();

// ---- 主题切换 ----
document.getElementById('theme').onclick = ()=>{
  const cur = document.documentElement.dataset.theme;
  const next = cur === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  document.getElementById('hljs-light').disabled = next === 'dark';
  document.getElementById('hljs-dark').disabled = next !== 'dark';
  initMermaid();
};
// ---- 回顶 ----
document.getElementById('totop').onclick = ()=> window.scrollTo({top:0, behavior:'smooth'});
// ---- 侧栏 active 高亮 ----
window.addEventListener('scroll', ()=>{
  const chs = document.querySelectorAll('.chapter');
  let cur = null;
  chs.forEach(c=>{ if (c.getBoundingClientRect().top < 120) cur = c.id; });
  document.querySelectorAll('.sidebar a').forEach(a=>{
    a.classList.toggle('active', cur && a.getAttribute('href') === '#'+cur);
  });
});
// ---- 首屏折叠：默认展开 ----
</script>
</body>
</html>
"""

# 注入数据
html = HTML.replace("__DATA_JSON__", DATA_JSON).replace("__NAV_JSON__", NAV_JSON)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print(f"OK -> {OUT}")
print(f"chapters: {len(chapters)}  size: {os.path.getsize(OUT)//1024} KB")

