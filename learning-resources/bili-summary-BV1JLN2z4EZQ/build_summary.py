#!/usr/bin/env python3
"""Build a polished, fully-offline single-file HTML summary for the RAG video.

- All screenshots embedded as base64 data URIs (no external files).
- All diagrams are inline SVG/CSS (no CDN, no Mermaid) so it renders offline / on intranet.
- Content is faithful to the full transcript; nothing omitted.
"""
import base64
from pathlib import Path

WORK = Path(__file__).resolve().parent
SHOTS = WORK / "shots"


def data_uri(name: str) -> str:
    p = SHOTS / name
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{b64}"


IMG = {n.name: data_uri(n.name) for n in sorted(SHOTS.glob("*.jpg"))}


def fig(name, cap, ts=""):
    ts_html = f'<span class="ts">{ts}</span>' if ts else ""
    return (f'<figure><img loading="lazy" src="{IMG[name]}" alt="{cap}">'
            f'<figcaption>{ts_html}{cap}</figcaption></figure>')


# ---------------------------------------------------------------- HTML pieces
HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RAG 工作机制详解 · 视频精读</title>
<style>
:root{
  --bg:#0d1117; --bg2:#111823; --card:#161d2b; --card2:#1c2536;
  --line:#26314a; --fg:#e8edf6; --muted:#98a5bd; --dim:#6f7d97;
  --accent:#5b9bff; --accent2:#38d39f; --amber:#ffb454; --rose:#ff6b8b;
  --violet:#b78bff; --code:#0b1220;
  --p0:#ff6b8b; --p1:#ffb454; --p2:#38d39f;
  --shadow:0 8px 30px rgba(0,0,0,.35);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:radial-gradient(1200px 600px at 80% -10%,#17233b 0,transparent 60%),var(--bg);
  color:var(--fg);line-height:1.75;
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Segoe UI",sans-serif;
  font-size:16px;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
code{font-family:"SF Mono",ui-monospace,Menlo,Consolas,monospace;background:var(--code);
  color:#cfe1ff;padding:.1em .45em;border-radius:6px;font-size:.88em;border:1px solid var(--line)}
.en{font-family:"SF Mono",ui-monospace,Menlo,Consolas,monospace;color:#cfe1ff;font-size:.94em}

/* layout */
.layout{max-width:1180px;margin:0 auto;padding:0 22px;display:grid;
  grid-template-columns:230px minmax(0,1fr);gap:34px}
main{min-width:0;padding-bottom:120px}
nav.toc{position:sticky;top:0;align-self:start;height:100vh;overflow-y:auto;
  padding:26px 0 40px;border-right:1px solid var(--line)}
nav.toc .brand{font-weight:700;font-size:.95rem;color:var(--fg);margin:0 0 4px;letter-spacing:.3px}
nav.toc .brand small{display:block;color:var(--dim);font-weight:500;font-size:.72rem;margin-top:3px}
nav.toc ol{list-style:none;margin:18px 0 0;padding:0;counter-reset:s}
nav.toc a{display:block;color:var(--muted);padding:6px 12px 6px 14px;border-left:2px solid transparent;
  font-size:.86rem;border-radius:0 8px 8px 0;transition:.15s}
nav.toc a:hover{color:var(--fg);background:var(--card);text-decoration:none}
nav.toc a.active{color:var(--fg);border-left-color:var(--accent);background:var(--card)}
nav.toc a.sub{padding-left:28px;font-size:.8rem;color:var(--dim)}

/* hero */
header.hero{padding:46px 0 26px;border-bottom:1px solid var(--line);margin-bottom:8px}
.tag{display:inline-flex;align-items:center;gap:7px;background:linear-gradient(90deg,#1b2b4d,#173a33);
  color:#bcd4ff;border:1px solid var(--line);padding:5px 13px;border-radius:999px;font-size:.76rem;
  letter-spacing:.5px;margin-bottom:16px}
.tag b{color:var(--accent2)}
header.hero h1{font-size:2.05rem;line-height:1.28;margin:0 0 14px;
  background:linear-gradient(92deg,#fff 10%,#a9c6ff 60%,#7ef0c2 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent}
.metabar{display:flex;flex-wrap:wrap;gap:8px 18px;color:var(--muted);font-size:.86rem;align-items:center}
.metabar .dot{width:5px;height:5px;border-radius:50%;background:var(--dim);display:inline-block}
.pill{display:inline-flex;gap:6px;align-items:center;background:var(--card);border:1px solid var(--line);
  padding:3px 11px;border-radius:999px;font-size:.78rem;color:var(--muted)}

/* kpi row */
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:26px 0 8px}
.kpi{background:linear-gradient(180deg,var(--card2),var(--card));border:1px solid var(--line);
  border-radius:14px;padding:15px 16px}
.kpi .k{font-size:1.5rem;font-weight:800;color:#fff;letter-spacing:.3px}
.kpi .l{color:var(--muted);font-size:.78rem;margin-top:2px}
.kpi .k.accent{color:var(--accent2)}

/* sections */
section{scroll-margin-top:18px;padding:30px 0 6px}
h2{font-size:1.5rem;margin:8px 0 6px;display:flex;align-items:center;gap:12px}
h2 .no{font-family:"SF Mono",monospace;font-size:.95rem;color:var(--bg);background:var(--accent);
  min-width:30px;height:30px;display:inline-flex;align-items:center;justify-content:center;
  border-radius:9px;font-weight:700}
h2.answer .no{background:var(--amber)}
h2.review .no{background:var(--violet)}
h3{font-size:1.14rem;margin:30px 0 8px;color:#fff;display:flex;align-items:center;gap:9px}
h3 .ic{font-size:1.05rem}
.lead{color:var(--muted);margin:2px 0 14px;border-left:3px solid var(--line);padding-left:14px}
p{margin:12px 0}
.muted{color:var(--muted)}

.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px 22px;margin:18px 0;
  box-shadow:var(--shadow)}
.card.soft{background:var(--bg2)}

figure{margin:20px 0}
figure img{width:100%;border-radius:12px;border:1px solid var(--line);display:block;background:#000}
figcaption{color:var(--muted);font-size:.83rem;text-align:center;margin-top:9px}
.ts{font-family:"SF Mono",monospace;color:var(--accent);background:var(--code);border:1px solid var(--line);
  padding:1px 7px;border-radius:6px;margin-right:8px;font-size:.78rem}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media(max-width:860px){.grid2{grid-template-columns:1fr}}

ul,ol{padding-left:22px}
li{margin:6px 0}
li::marker{color:var(--accent)}
.check li{list-style:none;position:relative;padding-left:26px}
.check li::before{content:"▸";position:absolute;left:2px;color:var(--accent2);font-weight:700}

/* callouts */
.note{border-radius:12px;padding:14px 16px 14px 18px;margin:16px 0;border:1px solid var(--line);
  background:var(--card2);position:relative}
.note .h{font-weight:700;font-size:.9rem;margin-bottom:4px;display:flex;gap:8px;align-items:center}
.note.info{border-left:4px solid var(--accent)}
.note.tip{border-left:4px solid var(--accent2)} .note.tip .h{color:var(--accent2)}
.note.warn{border-left:4px solid var(--amber)} .note.warn .h{color:var(--amber)}
.note.go{border-left:4px solid var(--violet);background:linear-gradient(180deg,#1b1630,#161d2b)}
.note.go .h{color:var(--violet)}

/* term chips */
.terms{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}
.term{background:var(--code);border:1px solid var(--line);border-radius:8px;padding:4px 10px;font-size:.8rem;color:#cfe1ff}
.term b{color:#fff}

/* problem cards */
.prob{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:16px 0}
@media(max-width:760px){.prob{grid-template-columns:1fr}}
.prob .c{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;border-top:3px solid var(--rose)}
.prob .c .n{font-size:.75rem;color:var(--rose);font-weight:700;letter-spacing:1px}
.prob .c .t{font-weight:700;margin:4px 0 6px;color:#fff}
.prob .c p{margin:0;font-size:.9rem;color:var(--muted)}

/* pipeline (css flow) */
.flow{display:flex;flex-wrap:wrap;align-items:stretch;gap:10px;margin:18px 0}
.flow .step{flex:1 1 120px;min-width:110px;background:linear-gradient(180deg,var(--card2),var(--card));
  border:1px solid var(--line);border-radius:12px;padding:13px 12px;text-align:center;position:relative}
.flow .step .ic{font-size:1.4rem}
.flow .step .t{font-weight:700;margin-top:5px;font-size:.95rem}
.flow .step .d{color:var(--muted);font-size:.76rem;margin-top:3px}
.flow .arrow{align-self:center;color:var(--dim);font-size:1.2rem;flex:0 0 auto}
.flow .step.prep{border-top:3px solid var(--accent)}
.flow .step.ans{border-top:3px solid var(--amber)}

/* two-phase banner */
.phase{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:16px 0}
@media(max-width:760px){.phase{grid-template-columns:1fr}}
.phase .box{border:1px solid var(--line);border-radius:14px;padding:16px 18px;background:var(--card)}
.phase .box.p1{border-top:3px solid var(--accent)}
.phase .box.p2{border-top:3px solid var(--amber)}
.phase .box h4{margin:0 0 4px;font-size:1rem}
.phase .box .when{font-size:.76rem;color:var(--dim)}
.phase .box .chips{margin-top:10px;display:flex;flex-wrap:wrap;gap:6px}
.chip{font-size:.78rem;padding:3px 10px;border-radius:999px;border:1px solid var(--line);background:var(--code);color:#cfe1ff}

/* compare table */
.cmp{width:100%;border-collapse:collapse;margin:14px 0;font-size:.92rem;overflow:hidden;border-radius:12px}
.cmp th,.cmp td{border:1px solid var(--line);padding:11px 13px;text-align:left;vertical-align:top}
.cmp thead th{background:var(--card2);color:#fff}
.cmp tbody th{background:var(--bg2);color:var(--muted);font-weight:600;white-space:nowrap}
.cmp .recall{color:var(--accent2)} .cmp .rerank{color:var(--amber)}
.good{color:var(--accent2)} .bad{color:var(--rose)}

/* transcript */
details.tx{margin:24px 0;border:1px solid var(--line);border-radius:12px;background:var(--bg2);overflow:hidden}
details.tx>summary{cursor:pointer;padding:14px 18px;font-weight:600;color:var(--fg);list-style:none;
  display:flex;justify-content:space-between;align-items:center}
details.tx>summary::-webkit-details-marker{display:none}
details.tx>summary .m{color:var(--dim);font-size:.8rem;font-weight:400}
details.tx .body{padding:6px 18px 18px;max-height:460px;overflow-y:auto;border-top:1px solid var(--line)}
.tx .line{display:flex;gap:12px;padding:5px 0;border-bottom:1px dashed #1d2740;font-size:.9rem}
.tx .line .t{font-family:"SF Mono",monospace;color:var(--accent);font-size:.76rem;flex:0 0 52px;padding-top:2px}
.tx .line .x{color:var(--fg)}

footer{margin-top:60px;padding:24px 0;border-top:1px solid var(--line);color:var(--dim);font-size:.82rem}

/* progress bar */
#bar{position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,var(--accent),var(--accent2));
  width:0;z-index:99;transition:width .1s}
.backtop{position:fixed;right:22px;bottom:22px;width:44px;height:44px;border-radius:50%;
  background:var(--card);border:1px solid var(--line);color:var(--fg);cursor:pointer;display:none;
  align-items:center;justify-content:center;font-size:1.1rem;box-shadow:var(--shadow);z-index:50}
@media(max-width:920px){
  .layout{grid-template-columns:1fr;gap:0}
  nav.toc{display:none}
}
</style>
</head>
<body>
<div id="bar"></div>
"""


def build():
    parts = [HEAD]

    # ---- TOC
    parts.append("""
<div class="layout">
<nav class="toc">
  <div class="brand">RAG 工作机制详解<small>视频精读 · 逐帧图解</small></div>
  <ol>
    <li><a href="#intro" class="active">导读 · RAG 是什么</a></li>
    <li><a href="#scene">1 · 使用场景与痛点</a></li>
    <li><a href="#basic">2 · RAG 基本流程</a></li>
    <li><a href="#chunk">3 · 分片 Chunking</a></li>
    <li><a href="#index">4 · 索引 Indexing</a></li>
    <li><a href="#index" class="sub">向量 / Embedding / 向量库</a></li>
    <li><a href="#recall">5 · 召回 Recall</a></li>
    <li><a href="#recall" class="sub">向量相似度三算法</a></li>
    <li><a href="#rerank">6 · 重排 Rerank</a></li>
    <li><a href="#gen">7 · 生成 Generation</a></li>
    <li><a href="#review">8 · 全链路回顾</a></li>
    <li><a href="#glossary">术语速查表</a></li>
    <li><a href="#transcript">完整字幕原文</a></li>
  </ol>
</nav>
<main>
""")

    # ---- Hero
    parts.append(f"""
<header class="hero" id="intro">
  <div class="tag">📺 B站视频精读 · <b>马克的技术工作坊</b></div>
  <h1>RAG 工作机制详解<br>一个高质量知识库背后的技术全流程</h1>
  <div class="metabar">
    <span class="pill">👤 马克的技术工作坊</span>
    <span class="pill">⏱ 17:02</span>
    <span class="pill">🎬 <a href="https://www.bilibili.com/video/BV1JLN2z4EZQ" target="_blank">BV1JLN2z4EZQ</a></span>
    <span class="pill">🧩 检索增强生成</span>
  </div>
  <div class="kpis">
    <div class="kpi"><div class="k accent">RAG</div><div class="l">Retrieval-Augmented Generation</div></div>
    <div class="kpi"><div class="k">2 阶段</div><div class="l">提问前准备 + 提问后回答</div></div>
    <div class="kpi"><div class="k">5 环节</div><div class="l">分片·索引·召回·重排·生成</div></div>
    <div class="kpi"><div class="k">10→3</div><div class="l">召回 10 片 → 重排精选 3 片</div></div>
  </div>
</header>

<section id="lead-sec" style="padding-top:18px">
  <div class="card soft">
    <p style="margin-top:0"><b>一句话理解：</b>RAG 全称 <span class="en">Retrieval-Augmented Generation</span>，翻译过来就是<b>「检索增强生成」</b>。说白了就干了两件事——<b>先从资料库里检索相关内容，再基于这些内容生成答案</b>。因为它「先检索、再生成」，所以叫检索增强生成。</p>
    <p style="margin-bottom:0">它是目前<b>最常用的 AI 问答方案之一</b>：很多企业内部的知识助手、智能客服，用的都是这项技术。本文按视频原有结构，把整条链路逐环节拆解，并解释其中所有专业名词（向量、Embedding 模型、向量数据库、向量相似度等），配上视频关键画面与原理图，力求<b>不漏任何一个细节</b>。</p>
  </div>
  <div class="note go">
    <div class="h">🐹 后端工程师视角（贯穿全文的类比）</div>
    如果你有后端背景：<b>索引阶段</b>像是一次「离线预计算 + 建倒排/向量索引」的 ETL 作业；<b>召回</b>像用低成本索引做粗筛（类似 ES 的初步检索）；<b>重排</b>像对候选集跑一个更重的打分模型做精排（召回/排序两段式，和推荐系统的 recall→rank 架构如出一辙）；<b>生成</b>则是把精排后的上下文拼进 Prompt 交给 LLM。整条链路本质是一个 <b>召回-精排-生成</b> 的流水线。
  </div>
</section>
""")

    # ---- Section 1: scene
    parts.append(f"""
<section id="scene">
  <h2><span class="no">1</span> 使用场景与「手册太长」的痛点</h2>
  <div class="lead">目标：做一个能回答公司产品各种问题的智能客服 —— 为什么不能把整本手册直接丢给大模型？</div>

  <p>假设你要做一个<b>智能客服</b>，它能回答关于公司产品的各种问题。首先它内部一定要有个大模型（比如 <span class="en">GPT-4o</span>、<span class="en">DeepSeek</span> 这类）。但光有模型不够——<b>模型并不知道你们公司的产品信息</b>。</p>

  <p>一个很自然的想法：<i>发问题时把产品手册一起发给模型不就行了？</i> 这确实是一种方案。但如果手册有<b>上百页乃至上千页</b>，就会带来三个严重问题：</p>

  {fig("02_problems.jpg","视频原图：产品手册太长带来的三个问题","03:47")}

  <div class="prob">
    <div class="c"><div class="n">问题 1</div><div class="t">模型读不全内容</div>
      <p>每个模型只能存储一定量的信息，这个量叫<b>上下文窗口大小（Context Window）</b>。手册字数一旦超过窗口，模型就会「读了后面、忘了前面」，回答准确率无法保障。</p></div>
    <div class="c"><div class="n">问题 2</div><div class="t">推理成本高</div>
      <p>输入越多，成本越高。每次回答都带上一本厚厚的手册，Token 成本可想而知，根本降不下来。</p></div>
    <div class="c"><div class="n">问题 3</div><div class="t">推理速度慢</div>
      <p>输入越多，模型需要消化的内容越多，输出就越慢。一本上百页的手册扔进去，大概率严重拖慢推理速度。</p></div>
  </div>

  <div class="note tip">
    <div class="h">💡 RAG 的核心思路</div>
    既然「整本文档丢给模型」行不通，那就<b>只把文档中相关的内容发给模型</b>。比如上百页手册里，可能只有 <b>3 个片段</b> 真正和用户问题相关——把这 3 个片段单独挑出来，连同用户问题一起发给大模型。这样模型只感知 3 个相关片段，而不是整个文档，上面三个问题就迎刃而解了。这，就是 RAG 登场的地方。
  </div>

  {fig("03_ideal.jpg","设想：只把相关片段（片段1/3/5）+ 问题发给大模型，模型回答「12 个月」","02:19")}
</section>
""")

    # ---- Section 2: basic flow
    parts.append(f"""
<section id="basic">
  <h2><span class="no">2</span> RAG 的基本流程：两个阶段、五个环节</h2>
  <div class="lead">上面是过度简化的链路，隐藏了「如何分片、如何选相关片段」等细节。完整的 RAG 分为两大部分。</div>

  {fig("01_outline.jpg","视频大纲：总体介绍 → 逐步拆解（分片/索引/召回/重排/生成）→ 全链路回顾","01:00")}

  <div class="phase">
    <div class="box p1">
      <h4>🗄 准备部分（数据准备）</h4>
      <div class="when">发生在 —— 用户提问<b>之前</b></div>
      <p class="muted" style="font-size:.9rem;margin:8px 0 0">提前把相关文档准备好并完成预处理，构建出知识库。</p>
      <div class="chips"><span class="chip">① 分片 Chunking</span><span class="chip">② 索引 Indexing</span></div>
    </div>
    <div class="box p2">
      <h4>💬 回答部分</h4>
      <div class="when">发生在 —— 用户提问<b>之后</b></div>
      <p class="muted" style="font-size:.9rem;margin:8px 0 0">用户一提问，就触发回答问题的各个环节。</p>
      <div class="chips"><span class="chip">③ 召回 Recall</span><span class="chip">④ 重排 Rerank</span><span class="chip">⑤ 生成 Generation</span></div>
    </div>
  </div>

  <p class="muted">下面把这五个环节逐一拆解，看看它们分别是如何工作的：</p>
  <div class="flow">
    <div class="step prep"><div class="ic">✂️</div><div class="t">分片</div><div class="d">切成多个片段</div></div>
    <div class="arrow">→</div>
    <div class="step prep"><div class="ic">🗂</div><div class="t">索引</div><div class="d">片段→向量入库</div></div>
    <div class="arrow">┊</div>
    <div class="step ans"><div class="ic">🎣</div><div class="t">召回</div><div class="d">粗筛 10 片</div></div>
    <div class="arrow">→</div>
    <div class="step ans"><div class="ic">🎯</div><div class="t">重排</div><div class="d">精选 3 片</div></div>
    <div class="arrow">→</div>
    <div class="step ans"><div class="ic">🤖</div><div class="t">生成</div><div class="d">大模型出答案</div></div>
  </div>
</section>
""")

    # ---- Section 3: chunk
    parts.append(f"""
<section id="chunk">
  <h2><span class="no">3</span> 分片 Chunking</h2>
  <div class="lead">顾名思义，就是把文档切分成多个片段。</div>

  <p>分片的方式有很多种，可以按不同粒度切分，但不管怎么做，<b>最终都要把一整篇文档切分为多份</b>。切好后，本环节就结束，进入下一环节。</p>

  {fig("04_chunking.jpg","四种常见分片方式：按字数分 / 按段落分 / 按章节分 / 按页码分","05:12")}

  <ul class="check">
    <li><b>按字数分</b>：比如每 1000 个字一个片段。</li>
    <li><b>按段落分</b>：比如一个段落一个片段。</li>
    <li><b>按章节分</b>：比如「第 3 章 · 售后服务」为一个片段。</li>
    <li><b>按页码分</b>：比如每一页为一个片段。</li>
    <li>除此之外还有很多切分方式——「这里面的学问都不少」。</li>
  </ul>
  <div class="note info"><div class="h">📌 要点</div>分片粒度直接影响后续检索质量：切太碎会丢上下文，切太大又回到「片段太长」的老问题。视频未展开调参细节，但强调了「如何分片」本身就是一门学问。</div>
</section>
""")

    # ---- Section 4: index (with vector / embedding / vectordb)
    parts.append(f"""
<section id="index">
  <h2><span class="no">4</span> 索引 Indexing</h2>
  <div class="lead">通过 Embedding 把每个片段文本转换为向量，并将「片段文本 + 对应向量」都存入向量数据库。</div>

  {fig("05_index.jpg","索引 = ① 通过 Embedding 将片段文本转为向量 ② 把片段文本与向量存入向量数据库","08:38")}

  <p>索引只有两步，但信息量巨大，涉及三个核心概念：<b>向量</b>、<b>Embedding</b>、<b>向量数据库</b>。视频先把这三个概念讲清楚，再回来看索引流程。</p>

  <h3><span class="ic">📐</span> 概念一：向量 Vector</h3>
  <p>向量是数学里的概念，代表<b>一个有大小、有方向的量</b>，通常用一个数组表示。数组里数字的个数就是向量的<b>维度</b>：</p>
  <div class="terms">
    <span class="term"><b>一维向量</b> <span class="en">[1.0]</span></span>
    <span class="term"><b>二维向量</b> <span class="en">[2, 2]</span></span>
    <span class="term"><b>三维向量</b> <span class="en">[1.0, 2.3, 5.76 …]</span></span>
  </div>
  <div class="grid2">
    <div>
      <p>低维向量可以直接画在坐标轴里：一维向量 <span class="en">1</span>（大小 1、方向朝右）、<span class="en">-3</span>（大小 3、方向朝左）；二维、三维同理放进对应维度的坐标轴。</p>
      <p>维度再大就无法可视化了（我们生活在三维世界），但<b>无法可视化不代表不存在</b>。</p>
      <div class="note info"><div class="h">📌 关键结论</div>RAG 里用到的向量维度通常很大（<b>几百甚至几千维</b>）。一般来说<b>维度越大，每个向量包含的信息越丰富，用它做各种工作的可靠性也越强</b>。</div>
    </div>
    <div>{fig("06_vector3d.jpg","三维向量在坐标轴中的示意——维度越大，信息越丰富","06:45")}</div>
  </div>

  <h3><span class="ic">🔤</span> 概念二：Embedding（把文本变成向量）</h3>
  <p>Embedding 就是<b>把文本转换为向量的过程</b>。它的关键目的是：<b>含义相近的文本，经过 Embedding 后，对应的向量也相近</b>。视频用二维向量举例：</p>
  <div class="grid2">
    <div>
      <table class="cmp">
        <thead><tr><th>文本</th><th>向量</th><th>关系</th></tr></thead>
        <tbody>
          <tr><td>马克喜欢吃水果</td><td class="en">[1, 2]</td><td class="good">语义相近 → 向量接近</td></tr>
          <tr><td>马克爱吃水果</td><td class="en">[1, 1]</td><td class="good">语义相近 → 向量接近</td></tr>
          <tr><td>天气真好</td><td class="en">[-3, -1]</td><td class="bad">完全不相关 → 距离远</td></tr>
        </tbody>
      </table>
      <p class="muted" style="font-size:.9rem">前两句向量非常接近，「天气真好」则离得很远——这正是 Embedding 的目的。</p>
    </div>
    <div>{fig("07_embedding_sim.jpg","语义相近的三句话向量聚在一起，「天气真好」被甩到第三象限","07:00")}</div>
  </div>

  <p><b>为什么这么设计？</b> 因为这样一来，当用户问「马克喜欢吃什么」时，我们可以先把问题做 Embedding 转成向量，再根据<b>向量相似度</b>把相关文本找出来，最后把相关文本 + 用户问题一起发给大模型，模型就能回答「马克喜欢吃水果」了。</p>

  <div class="note warn">
    <div class="h">⚠️ Embedding 由「专门的模型」完成</div>
    这个操作是模型来做的，但<b>不是</b> GPT-4o、DeepSeek 这类对话模型，而是<b>专门的 Embedding 模型</b>。想知道哪些 Embedding 模型好用，可以看 <b><span class="en">MTEB</span> 排行榜</b>（Hugging Face 上的 <span class="en">huggingface.co/spaces/mteb</span>），它会对各种 Embedding 模型做评测并排名，方便挑选。
  </div>

  <h3><span class="ic">🗃</span> 概念三：向量数据库 Vector Database</h3>
  <p>向量数据库就是<b>用来存储和查询向量的数据库</b>。它为存储向量做了很多优化，并提供了<b>计算向量相似度</b>等相关函数，方便我们使用向量。</p>
  <div class="grid2">
    <div>
      <p>Embedding 后的向量就存进向量数据库，方便后续查询。<b>注意：要存的不只是向量，还有原始文本</b>——所以原始文本也要一起发给向量数据库。</p>
      <p>因为只有这样，我们才能在「通过向量相似度查出相似向量」之后，把对应的<b>原始文本</b>也抽取出来交给大模型。我们最终需要的还是原始文本，<b>向量只是一个中间结果</b>。</p>
      <div class="note info"><div class="h">📌 表结构</div>一般的向量数据库表格里，<b>至少有「原始文本」和「向量」两列</b>。</div>
    </div>
    <div>{fig("08_vectordb.jpg","向量数据库表格：文本列 + 向量列（如「马克喜欢吃水果」→ [1.0, 2.5, 3.7, 5.8, 2.8]）","08:20")}</div>
  </div>

  <h3><span class="ic">🔁</span> 回看索引：对每个片段重复「Embedding + 入库」</h3>
  <p>理解了三个概念后再看索引就很清楚了：其实就是把前面「一句话」的处理换成<b>每个片段的内容</b>——先处理片段一（Embedding→得到向量→连同原始文本存入向量数据库），再处理片段二，依此类推，<b>直到所有片段都处理完毕</b>，整个索引流程结束。</p>
  <div class="note tip"><div class="h">✅ 阶段小结</div>不管是<b>分片</b>还是<b>索引</b>，都发生在<b>用户提问之前</b>，属于要提前准备好的步骤。到这里，知识库就算构建完毕，「就等用户来用了」。</div>
</section>
""")

    # ---- Section 5: recall
    parts.append(f"""
<section id="recall">
  <h2 class="answer"><span class="no">5</span> 召回 Recall（提问后第一步）</h2>
  <div class="lead">召回 = 搜索与用户问题相关片段的过程。</div>

  <p>这个环节从<b>用户问题</b>开始：用户的问题先发给 Embedding 模型 → 转换为向量 → 把向量发给向量数据库 → 让它查询<b>与用户问题最相关的 10 个片段</b>。</p>

  {fig("09_recall.jpg","召回流程：用户问题 → Embedding → 向量 → 向量数据库返回 10 个最相似结果","09:59")}

  <div class="note info"><div class="h">📌 「10」不是固定的</div>召回结果就是 10 个相关片段，但这个数字可以是 15、20 等等，具体多少不重要，<b>只要数量不太多就行</b>。不管多少，向量数据库都要返回与用户问题最相似的一批片段。</div>

  <h3><span class="ic">🧮</span> 向量数据库怎么知道哪些片段最相关？—— 计算向量相似度</h3>
  <p>做法是：把<b>用户问题向量</b>和<b>每个片段向量</b>分别代入一个<b>相似度计算公式</b>，得出向量相似度；公式的第一个参数<b>永远是用户问题向量</b>，第二个参数是各个片段向量。逐个片段算完后<b>排序，取相似度最大的前 10 个</b>。</p>

  {fig("10_similarity_table.jpg","模拟计算：对每个片段算出与用户问题的向量相似度（0.5113 / 0.4718 / 0.7506 …）再排序取 Top-K","11:22")}

  <h3><span class="ic">📊</span> 三种主流的向量相似度算法</h3>
  <div class="grid2">
    <div>
      <ul class="check">
        <li><b>余弦相似度（Cosine）</b>：计算两个向量夹角的 <span class="en">cos</span> 值，再根据 cos 值判断夹角大小。<b>夹角越小，相似度越高</b>。</li>
        <li><b>欧氏距离（Euclidean）</b>：计算两个向量之间的直线距离。<b>距离越小，相似度越高</b>。</li>
        <li><b>点积（Dot Product）</b>：一种用代数方式衡量相似度的方法，<b>既考虑方向关系，也考虑长度</b>。</li>
      </ul>
    </div>
    <div>{fig("11_dotproduct.jpg","点积：从 A 向 B 引垂线，用投影长度与 B 长度的乘积衡量相似度","12:21")}</div>
  </div>
  <div class="note info"><div class="h">📐 点积的几何理解</div>
    要算图中 A 和 B 的点积：先从 A 向 B 引一条垂线，点积 ≈ <b>投影距离 × B 的长度</b> 的乘积。乘积越大相似度越高。
    <ul style="margin:8px 0 0">
      <li>两向量<b>方向一致</b>：向量越长，点积越大；</li>
      <li>方向<b>相反</b>：点积为<b>负</b>；</li>
      <li>方向<b>垂直</b>：点积为 <b>0</b>。</li>
    </ul>
    所以点积能判断两个向量「是否在同一个方向上努力，以及努力的程度有多大」。
  </div>
  <p class="muted">召回阶段查出了与用户问题最匹配的 <b>10 个片段</b>——记住这个结论，因为这 10 个片段会发送到<b>重排</b>阶段继续处理。</p>
</section>
""")

    # ---- Section 6: rerank
    parts.append(f"""
<section id="rerank">
  <h2 class="answer"><span class="no">6</span> 重排 Rerank（重新排序）</h2>
  <div class="lead">从召回的 10 份里，再挑出 3 份与用户问题最相似的，作为重排结果。</div>

  <p>重排做的事和召回类似：召回是从<b>所有片段</b>里挑 10 份最相似的；重排则是从召回的<b>这 10 份</b>里再挑 3 份最相似的。</p>

  <div class="note warn"><div class="h">🤔 为什么不直接在召回阶段挑 3 个，非要搞两遍？</div>
    直接挑 3 个当然可以，但<b>效果没有「召回 + 重排」好</b>。因为两个阶段使用的<b>文本相似度计算逻辑不一样</b>——一个便宜但粗糙，一个精准但昂贵，组合起来才能兼顾速度与准确率。</div>

  {fig("12_recall_vs_rerank.jpg","召回 vs 重排：方法 / 特点（成本·耗时·准确率）/ 适合场景 全面对比","14:00")}

  <table class="cmp">
    <thead><tr><th>对比维度</th><th class="recall">召回 Recall</th><th class="rerank">重排 Rerank</th></tr></thead>
    <tbody>
      <tr><th>方法</th><td>向量相似度<br>（余弦 / 欧氏距离 / 点积）</td><td><span class="en">Cross-Encoder</span> 模型</td></tr>
      <tr><th>成本</th><td class="good">👍 低</td><td class="bad">👎 高</td></tr>
      <tr><th>耗时</th><td class="good">👍 短</td><td class="bad">👎 长</td></tr>
      <tr><th>准确率</th><td class="bad">👎 低</td><td class="good">👍 高</td></tr>
      <tr><th>适合场景</th><td>初步筛选（短时间内把上千条片段的相似度都算出来，挑 Top 10）</td><td>精挑细选（对少量候选做高精度打分）</td></tr>
    </tbody>
  </table>

  <div class="note tip"><div class="h">🧑‍💼 视频类比：公司招聘 = 简历筛选 + 面试</div>
    公司面试分两个环节：<b>简历筛选 + 面试</b>。
    <b>召回 ≈ 简历筛选</b>：候选人太多，只能用粗略方法从成千上万份简历里挑出 10 个看起来最优秀的，准确率会打折扣，但没办法。
    <b>重排 ≈ 面试</b>：对这 10 个人仔细面试，尽可能保证判断正确，从中挑出最优秀的 <b>3 个人入职</b>。</div>
</section>
""")

    # ---- Section 7: generation
    parts.append(f"""
<section id="gen">
  <h2 class="answer"><span class="no">7</span> 生成 Generation</h2>
  <div class="lead">生成什么？当然是生成答案。</div>
  <p>现在我们手上有了：<b>用户问题</b> + <b>与问题最相关的 3 个片段</b>。把这两部分<b>一起发给大模型</b>，让它根据片段内容来回答用户问题。到此，整个 RAG 流程就结束了。</p>
  <div class="flow">
    <div class="step ans"><div class="ic">❓</div><div class="t">用户问题</div><div class="d">马克喜欢吃什么？</div></div>
    <div class="arrow">+</div>
    <div class="step ans"><div class="ic">📄</div><div class="t">3 个相关片段</div><div class="d">重排精选的参考资料</div></div>
    <div class="arrow">→</div>
    <div class="step ans"><div class="ic">🤖</div><div class="t">大模型</div><div class="d">如 GPT-4o</div></div>
    <div class="arrow">→</div>
    <div class="step ans"><div class="ic">✅</div><div class="t">最终答案</div><div class="d">基于片段内容作答</div></div>
  </div>
  <div class="note go"><div class="h">🐹 工程视角补充</div>这一步在工程上就是<b>拼 Prompt</b>：把 3 个片段作为「参考资料 / context」和用户问题一起塞进提示词模板，交给 LLM 生成。片段少（只有 3 个）→ 上下文短 → 成本低、速度快、且模型注意力集中在真正相关的内容上，这正好解决了开头「手册太长」的三个问题。</div>
</section>
""")

    # ---- Section 8: review
    parts.append(f"""
<section id="review">
  <h2 class="review"><span class="no">8</span> 全链路回顾：串起来再走一遍</h2>
  <div class="lead">整个流程分两部分——准备部分（提问前）与回答部分（提问后），所以整体流程图也有两张。</div>

  <h3><span class="ic">🗄</span> 提问前：准备部分（构建知识库）</h3>
  <p class="muted">分片 → Embedding → 入库，三步走完，知识库就绪。</p>
  <div class="flow">
    <div class="step prep"><div class="ic">📕</div><div class="t">产品使用手册</div><div class="d">原始文档</div></div>
    <div class="arrow">→</div>
    <div class="step prep"><div class="ic">✂️</div><div class="t">分片</div><div class="d">→ 片段列表</div></div>
    <div class="arrow">→</div>
    <div class="step prep"><div class="ic">🔤</div><div class="t">Embedding 模型</div><div class="d">每片段→向量</div></div>
    <div class="arrow">→</div>
    <div class="step prep"><div class="ic">🗃</div><div class="t">向量数据库</div><div class="d">向量 + 文本入库</div></div>
  </div>
  {fig("13_flow_prepare.jpg","提问前准备流程：手册 → 片段列表 → Embedding 模型 → 向量 → 向量数据库","16:05")}

  <h3><span class="ic">💬</span> 提问后：回答部分（召回→重排→生成）</h3>
  <p class="muted">用户问题向量化 → 向量库召回 10 片 → Cross-Encoder 重排选 3 片 → 3 片 + 问题交给大模型出答案。</p>
  <div class="flow">
    <div class="step ans"><div class="ic">❓</div><div class="t">用户问题</div><div class="d">这视频是哪个账号做的？</div></div>
    <div class="arrow">→</div>
    <div class="step ans"><div class="ic">🔤</div><div class="t">Embedding</div><div class="d">→ 向量</div></div>
    <div class="arrow">→</div>
    <div class="step ans"><div class="ic">🗃</div><div class="t">向量数据库</div><div class="d">召回 10 片</div></div>
    <div class="arrow">→</div>
    <div class="step ans"><div class="ic">🎯</div><div class="t">Cross-Encoder</div><div class="d">重排选 3 片</div></div>
    <div class="arrow">→</div>
    <div class="step ans"><div class="ic">🤖</div><div class="t">大模型</div><div class="d">出最终答案</div></div>
  </div>
  {fig("14_flow_answer.jpg","提问后回答流程：问题→Embedding→向量→向量库→召回10片→重排3片→大模型→答案「马克的技术工作坊」","16:49")}

  <div class="note tip"><div class="h">🎬 全片总结</div>
    RAG = <b>准备</b>（分片 + 索引）+ <b>回答</b>（召回 + 重排 + 生成）。它通过「只把最相关的少量片段喂给大模型」，一举解决了「整本手册直接丢给模型」带来的<b>读不全、成本高、速度慢</b>三大问题——这就是一个高质量智能客服 / 知识库背后的技术全流程。
  </div>
</section>
""")

    # ---- Glossary
    parts.append("""
<section id="glossary">
  <h2><span class="no">📖</span> 术语速查表</h2>
  <table class="cmp">
    <thead><tr><th>术语</th><th>英文 / 别名</th><th>一句话解释</th></tr></thead>
    <tbody>
      <tr><td>RAG</td><td class="en">Retrieval-Augmented Generation</td><td>检索增强生成：先检索相关内容，再基于它生成答案。</td></tr>
      <tr><td>上下文窗口</td><td class="en">Context Window</td><td>模型一次能「记住 / 读取」的信息量上限，超出就会顾此失彼。</td></tr>
      <tr><td>分片</td><td class="en">Chunking</td><td>把长文档切成多个片段（按字数/段落/章节/页码等）。</td></tr>
      <tr><td>索引</td><td class="en">Indexing</td><td>把每个片段 Embedding 成向量，连同原文一起存入向量数据库。</td></tr>
      <tr><td>向量</td><td class="en">Vector</td><td>有大小有方向的量，用数组表示；数组长度 = 维度，RAG 中常达几百上千维。</td></tr>
      <tr><td>Embedding</td><td class="en">Embedding 模型</td><td>把文本转成向量的过程/模型；语义相近 → 向量相近。非对话模型，是专门模型。</td></tr>
      <tr><td>MTEB</td><td class="en">MTEB Leaderboard</td><td>Embedding 模型评测排行榜，用于挑选好用的 Embedding 模型。</td></tr>
      <tr><td>向量数据库</td><td class="en">Vector Database</td><td>存储、查询向量并计算相似度的数据库；至少含「原文 + 向量」两列。</td></tr>
      <tr><td>向量相似度</td><td class="en">Vector Similarity</td><td>衡量两个向量有多接近，用于找相关片段。</td></tr>
      <tr><td>余弦相似度</td><td class="en">Cosine Similarity</td><td>看夹角 cos 值，夹角越小越相似。</td></tr>
      <tr><td>欧氏距离</td><td class="en">Euclidean Distance</td><td>看直线距离，距离越小越相似。</td></tr>
      <tr><td>点积</td><td class="en">Dot Product</td><td>兼顾方向与长度；同向越长越大，反向为负，垂直为 0。</td></tr>
      <tr><td>召回</td><td class="en">Recall</td><td>用向量相似度从全部片段中粗筛出 Top-K（如 10）个相关片段。</td></tr>
      <tr><td>重排</td><td class="en">Rerank</td><td>用 Cross-Encoder 从召回结果中精选出更相关的少量片段（如 3 个）。</td></tr>
      <tr><td>Cross-Encoder</td><td class="en">Cross-Encoder</td><td>重排阶段用的模型：成本高、耗时长，但准确率高，适合精挑细选。</td></tr>
      <tr><td>生成</td><td class="en">Generation</td><td>把精选片段 + 用户问题一起交给大模型，生成最终答案。</td></tr>
    </tbody>
  </table>
</section>
""")

    return parts


def transcript_section(srt_path: Path):
    """Parse SRT into (timestamp, text) lines and render a collapsible block."""
    import re
    raw = srt_path.read_text(encoding="utf-8")
    blocks = re.split(r"\n\s*\n", raw.strip())
    rows = []
    for b in blocks:
        lines = [l for l in b.splitlines() if l.strip()]
        if len(lines) < 3:
            continue
        m = re.match(r"(\d\d):(\d\d):(\d\d)", lines[1])
        if not m:
            continue
        hh, mm, ss = map(int, m.groups())
        total = hh * 3600 + mm * 60 + ss
        disp = f"{total//60:02d}:{total%60:02d}"
        text = "".join(lines[2:]).strip()
        if text:
            rows.append((disp, text))
    body = "\n".join(
        f'<div class="line"><span class="t">{t}</span><span class="x">{x}</span></div>'
        for t, x in rows
    )
    return f"""
<section id="transcript">
  <details class="tx">
    <summary>📝 展开完整字幕原文（Whisper 转写 · 共 {len(rows)} 段） <span class="m">点击展开 / 收起</span></summary>
    <div class="body">{body}</div>
  </details>
</section>
"""


FOOT = """
<footer>
  <p>本文为「{title}」的视频精读整理，内容忠实于视频讲解与画面，供离线阅读。</p>
  <p>UP主：马克的技术工作坊 · 原视频：<a href="https://www.bilibili.com/video/BV1JLN2z4EZQ" target="_blank">bilibili.com/video/BV1JLN2z4EZQ</a></p>
  <p>字幕由 whisper.cpp（large-v3-turbo）本地转写，关键画面为视频原始截图。</p>
</footer>
</main>
</div>
<div class="backtop" id="backtop" title="回到顶部">↑</div>
<script>
// progress bar + active TOC + back-to-top
var bar=document.getElementById('bar'),backtop=document.getElementById('backtop');
var links=[].slice.call(document.querySelectorAll('nav.toc a'));
var secs=links.map(function(a){var id=a.getAttribute('href').slice(1);return document.getElementById(id);});
function onScroll(){
  var h=document.documentElement,st=h.scrollTop||document.body.scrollTop;
  var sh=(h.scrollHeight-h.clientHeight)||1;
  bar.style.width=(st/sh*100)+'%';
  backtop.style.display=st>500?'flex':'none';
  var idx=0;
  for(var i=0;i<secs.length;i++){if(secs[i]&&secs[i].getBoundingClientRect().top<=120)idx=i;}
  links.forEach(function(a){a.classList.remove('active');});
  if(links[idx])links[idx].classList.add('active');
}
document.addEventListener('scroll',onScroll,{passive:true});onScroll();
backtop.onclick=function(){window.scrollTo({top:0,behavior:'smooth'});};
</script>
</body></html>
"""


if __name__ == "__main__":
    parts = build()
    parts.append(transcript_section(WORK / "transcript.srt"))
    title = "RAG 工作机制详解——一个高质量知识库背后的技术全流程"
    parts.append(FOOT.replace("{title}", title))
    html = "".join(parts)
    out = WORK / "RAG工作机制详解_视频精读.html"
    out.write_text(html, encoding="utf-8")
    print(f"✅ wrote {out} ({len(html)//1024} KB)")
