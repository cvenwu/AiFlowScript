#!/usr/bin/env python3
"""Build the P2 bilibili video note as one offline HTML file."""
import base64
import html
import json
import mimetypes
import re
from pathlib import Path

WORK = Path(__file__).resolve().parent
CONTENT = WORK / "content_p2.json"
OUT = WORK / "LlamaIndex路由器查询引擎_P2_视频精读.html"


def esc(value):
    return html.escape(str(value or ""), quote=True)


def slug(value):
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", str(value)).strip("-") or "section"


def data_uri(rel):
    path = WORK / rel
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def figure(item):
    rel = item["file"]
    path = WORK / rel
    caption = item.get("caption", "")
    ts = item.get("time", "")
    if not path.exists():
        return f'<figure class="shot missing"><div>截图缺失：{esc(rel)}</div><figcaption>{esc(ts)} · {esc(caption)}</figcaption></figure>'
    return (
        '<figure class="shot">'
        f'<img src="{data_uri(rel)}" alt="{esc(caption)}" loading="lazy" data-caption="{esc(ts)} · {esc(caption)}">'
        f'<figcaption><span>{esc(ts)}</span>{esc(caption)}</figcaption>'
        '</figure>'
    )


def code_block(block):
    return (
        '<div class="code-wrap">'
        f'<div class="code-title">{esc(block.get("caption", "代码 / 配置"))}</div>'
        f'<pre><code>{esc(block.get("code", ""))}</code></pre>'
        '</div>'
    )


def list_items(items):
    return "".join(f"<li>{esc(x)}</li>" for x in items)


def build():
    c = json.loads(CONTENT.read_text(encoding="utf-8"))
    meta = c["meta"]
    sections = c.get("sections", [])
    transcript = ""
    txt = WORK / "transcript" / "page2.txt"
    if txt.exists():
        transcript = txt.read_text(encoding="utf-8")

    toc = [
        ("overview", "视频概览"),
        ("framework", "整体框架"),
        ("logic", "作者讲解逻辑"),
    ] + [(s.get("id") or slug(s.get("title")), s.get("title", "章节")) for s in sections] + [
        ("screenshots", "关键截图"),
        ("summary", "结尾总结"),
        ("transcript", "转写原文"),
    ]

    framework_html = "".join(
        f'<div class="framework-card"><h3>{esc(x.get("title"))}</h3><ul>{list_items(x.get("children", []))}</ul></div>'
        for x in c.get("framework", [])
    )
    flow_html = "".join(f'<span class="flow-node">{esc(x)}</span>' for x in c.get("flow", []))
    sections_html = []
    for i, sec in enumerate(sections, 1):
        sid = sec.get("id") or slug(sec.get("title"))
        shots = "".join(figure(x) for x in sec.get("screenshots", []))
        codes = "".join(code_block(x) for x in sec.get("code_blocks", []))
        sections_html.append(f'''
        <section id="{esc(sid)}" class="card chapter">
          <div class="chapter-kicker">第 {i:02d} 章 · {esc(sec.get("time"))}</div>
          <h2>{esc(sec.get("title"))}</h2>
          <p class="summary-line">{esc(sec.get("summary"))}</p>
          {f'<div class="highlight"><strong>核心结论：</strong>{esc(sec.get("highlight"))}</div>' if sec.get("highlight") else ''}
          <h3>讲解要点</h3>
          <ul class="point-list">{list_items(sec.get("points", []))}</ul>
          {codes}
          {shots}
        </section>''')

    key_shots = "".join(figure(x) for x in c.get("key_screenshots", []))
    final = c.get("final_summary", {})
    html_doc = f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(c["title"])}</title>
  <style>
    :root {{ --bg:#f5f7f4; --paper:#fffdf8; --paper2:#eef5ef; --ink:#1f2933; --muted:#667085; --line:#d9e2dc; --brand:#256f5b; --brand2:#d97706; --hi:#fff5cc; --code:#102018; --shadow:0 18px 50px rgba(31,41,51,.10); }}
    [data-theme="dark"] {{ --bg:#111815; --paper:#17211d; --paper2:#203029; --ink:#e7eee9; --muted:#a6b5ad; --line:#31443a; --brand:#7dd3b0; --brand2:#fbbf24; --hi:#3a3216; --code:#e7eee9; --shadow:0 18px 50px rgba(0,0,0,.38); }}
    * {{ box-sizing:border-box; }} html {{ scroll-behavior:smooth; }} body {{ margin:0; background:radial-gradient(circle at top left, var(--paper2), transparent 28rem), var(--bg); color:var(--ink); font:16px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",Arial,sans-serif; }}
    #progress {{ position:fixed; top:0; left:0; height:4px; width:0; z-index:20; background:linear-gradient(90deg,var(--brand),var(--brand2)); }}
    .layout {{ display:grid; grid-template-columns:300px minmax(0,1fr); gap:28px; max-width:1440px; margin:0 auto; padding:24px; }}
    aside {{ position:sticky; top:20px; height:calc(100vh - 40px); overflow:auto; padding:18px; border:1px solid var(--line); border-radius:24px; background:rgba(255,253,248,.82); background:color-mix(in srgb, var(--paper) 88%, transparent); box-shadow:var(--shadow); backdrop-filter:blur(14px); }}
    .brand {{ font-weight:850; line-height:1.25; margin-bottom:14px; }} .brand small {{ display:block; color:var(--muted); font-weight:500; margin-top:6px; }}
    .toc a {{ display:block; padding:8px 10px; border-radius:12px; color:var(--muted); text-decoration:none; font-size:14px; }} .toc a:hover,.toc a.active {{ background:var(--paper2); color:var(--brand); }}
    main {{ min-width:0; }} .hero,.card {{ border:1px solid var(--line); border-radius:28px; background:var(--paper); box-shadow:var(--shadow); }} .hero {{ padding:38px; margin-bottom:24px; position:relative; overflow:hidden; }} .hero:before {{ content:""; position:absolute; inset:auto -8rem -9rem auto; width:22rem; height:22rem; border-radius:50%; background:color-mix(in srgb, var(--brand) 18%, transparent); }}
    h1 {{ margin:0 0 14px; font-size:clamp(30px,5vw,58px); line-height:1.08; letter-spacing:-.05em; }} h2 {{ margin:0 0 16px; font-size:clamp(24px,3vw,36px); letter-spacing:-.03em; }} h3 {{ margin:22px 0 10px; }}
    .meta-grid,.takeaways,.framework-grid {{ display:grid; gap:14px; }} .meta-grid {{ grid-template-columns:repeat(4,minmax(0,1fr)); margin-top:22px; }} .meta-item,.takeaways li,.framework-card,.highlight {{ background:var(--paper2); border:1px solid var(--line); border-radius:18px; padding:14px 16px; }} .meta-item b {{ display:block; font-size:13px; color:var(--muted); }} .meta-item span {{ font-weight:760; }}
    .toolbar {{ position:fixed; right:22px; bottom:22px; z-index:15; display:flex; flex-direction:column; gap:10px; }} button {{ border:1px solid var(--line); background:var(--paper); color:var(--ink); border-radius:999px; padding:10px 14px; cursor:pointer; box-shadow:var(--shadow); }}
    section.card {{ padding:28px; margin:24px 0; }} .kicker,.chapter-kicker {{ color:var(--brand); font-weight:800; letter-spacing:.03em; }} .summary-line {{ font-size:18px; color:var(--muted); }} .point-list li {{ margin:7px 0; }} .highlight {{ border-left:5px solid var(--brand2); background:var(--hi); margin:16px 0; }}
    .takeaways {{ padding:0; list-style:none; grid-template-columns:repeat(2,minmax(0,1fr)); }} .framework-grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} .flow {{ display:flex; flex-wrap:wrap; gap:10px; align-items:center; }} .flow-node {{ padding:10px 14px; border-radius:999px; background:var(--paper2); border:1px solid var(--line); }} .flow-node:not(:last-child)::after {{ content:" →"; color:var(--brand2); font-weight:900; }}
    .code-wrap {{ margin:18px 0; border-radius:18px; overflow:hidden; border:1px solid var(--line); background:#0d1b14; }} .code-title {{ padding:9px 14px; background:#173526; color:#c9f5dc; font-size:13px; }} pre {{ margin:0; padding:18px; overflow:auto; color:#e5ffe9; line-height:1.55; }} code {{ font-family:"SFMono-Regular",Consolas,Menlo,monospace; font-size:13px; }}
    figure.shot {{ margin:18px 0; }} .shot img {{ width:100%; border-radius:18px; box-shadow:0 12px 30px rgba(0,0,0,.18); cursor:zoom-in; border:1px solid var(--line); }} figcaption {{ color:var(--muted); font-size:14px; margin-top:8px; }} figcaption span {{ color:var(--brand); font-weight:800; margin-right:8px; }} .gallery {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:18px; }}
    details {{ border:1px solid var(--line); background:var(--paper2); border-radius:18px; padding:16px; }} details pre {{ white-space:pre-wrap; color:var(--ink); background:transparent; padding:8px 0 0; }}
    .modal {{ position:fixed; inset:0; display:none; align-items:center; justify-content:center; padding:24px; z-index:30; background:rgba(0,0,0,.78); }} .modal.open {{ display:flex; }} .modal img {{ max-width:96vw; max-height:86vh; border-radius:16px; }} .modal p {{ position:absolute; left:24px; bottom:12px; right:24px; color:white; text-align:center; }}
    @media (max-width:900px) {{ .layout {{ display:block; padding:14px; }} aside {{ position:relative; height:auto; margin-bottom:16px; }} .toc.collapsed nav {{ display:none; }} .meta-grid,.takeaways,.framework-grid,.gallery {{ grid-template-columns:1fr; }} .hero,section.card {{ padding:22px; border-radius:22px; }} }}
  </style>
</head>
<body>
  <div id="progress"></div>
  <div class="toolbar"><button id="theme">🌗 主题</button><button id="top">↑ 顶部</button></div>
  <div class="layout">
    <aside class="toc" id="toc"><div class="brand">视频精读目录<small>BV1uWQYBqE1c · P2 · 路由器查询引擎</small></div><button id="tocToggle">目录展开/收起</button><nav>{''.join(f'<a href="#{esc(h)}">{esc(t)}</a>' for h,t in toc)}</nav></aside>
    <main>
      <header class="hero" id="overview"><div class="kicker">视频概览区</div><h1>{esc(c['title'])}</h1><p class="summary-line">{esc(c.get('overview'))}</p><div class="meta-grid">
        <div class="meta-item"><b>UP 主</b><span>{esc(meta.get('up'))}</span></div><div class="meta-item"><b>总时长</b><span>{esc(meta.get('duration'))}</span></div><div class="meta-item"><b>当前分 P</b><span>P{esc(meta.get('page'))} · {esc(meta.get('part_title'))}</span></div><div class="meta-item"><b>内容类型</b><span>{esc(meta.get('content_type'))}</span></div>
      </div><h3>10 秒核心要点</h3><ul class="takeaways">{list_items(c.get('key_takeaways', []))}</ul></header>
      <section class="card" id="framework"><div class="kicker">整体框架与讲解思路</div><h2>章节框架</h2><div class="framework-grid">{framework_html}</div><h3>路由链路</h3><div class="flow">{flow_html}</div></section>
      <section class="card" id="logic"><div class="kicker">作者讲解逻辑</div><h2>作者如何组织这节课</h2><ul class="point-list">{list_items(c.get('author_logic', []))}</ul></section>
      {''.join(sections_html)}
      <section class="card" id="screenshots"><div class="kicker">关键截图配套</div><h2>代表性关键帧</h2><div class="gallery">{key_shots}</div></section>
      <section class="card" id="summary"><div class="kicker">结尾总结与价值提炼</div><h2>核心内容复盘</h2><ul>{list_items(final.get('checklist', []))}</ul><h3>落地价值</h3><ul>{list_items(final.get('value', []))}</ul></section>
      <section class="card" id="transcript"><div class="kicker">转写原文</div><h2>Whisper 转写文本</h2><details><summary>展开查看完整转写</summary><pre>{esc(transcript)}</pre></details></section>
    </main>
  </div>
  <div class="modal" id="modal"><img alt="放大截图"><p></p></div>
  <script>
    const root=document.documentElement, saved=localStorage.getItem('theme'); if(saved) root.dataset.theme=saved;
    document.getElementById('theme').onclick=()=>{{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';localStorage.setItem('theme',root.dataset.theme);}};
    document.getElementById('top').onclick=()=>scrollTo({{top:0,behavior:'smooth'}});
    document.getElementById('tocToggle').onclick=()=>document.getElementById('toc').classList.toggle('collapsed');
    const bar=document.getElementById('progress'), links=[...document.querySelectorAll('.toc a')], secs=links.map(a=>document.querySelector(a.getAttribute('href'))).filter(Boolean);
    addEventListener('scroll',()=>{{const h=document.documentElement;bar.style.width=(h.scrollTop/(h.scrollHeight-h.clientHeight)*100)+'%';let cur=secs[0];secs.forEach(s=>{{if(s.getBoundingClientRect().top<140)cur=s;}});links.forEach(a=>a.classList.toggle('active',cur&&a.hash==='#'+cur.id));}},{{passive:true}});
    const modal=document.getElementById('modal');document.querySelectorAll('.shot img').forEach(img=>img.onclick=()=>{{modal.classList.add('open');modal.querySelector('img').src=img.src;modal.querySelector('p').textContent=img.dataset.caption||img.alt;}});modal.onclick=()=>modal.classList.remove('open');
  </script>
</body>
</html>'''
    OUT.write_text(html_doc, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    build()
