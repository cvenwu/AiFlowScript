#!/usr/bin/env python3
"""Build an offline single-file HTML note for BV1uWQYBqE1c P05.

The generated page embeds CSS, JS and referenced screenshots as base64 data URIs.
It intentionally avoids CDN/runtime external dependencies.
"""
from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path


WORK = Path(__file__).resolve().parent
CONTENT = WORK / "content.p05.json"
OUT = WORK / "index.html"
TRANSCRIPT = WORK / "transcript.p05.en.srt"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def slug(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff_-]+", "-", value.strip())
    return value.strip("-") or "section"


def inline_mark(text: str) -> str:
    safe = esc(text)
    safe = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe)
    safe = re.sub(r"`([^`]+)`", r"<code>\1</code>", safe)
    return safe


def img_data_uri(rel: str) -> str:
    path = WORK / rel
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{data}"


def figure(item: dict) -> str:
    rel = item["file"]
    caption = item.get("caption", "")
    ts = item.get("time", "")
    if not (WORK / rel).exists():
        return f'<figure class="shot missing"><div>图片缺失：{esc(rel)}</div></figure>'
    return (
        '<figure class="shot">'
        f'<button class="shot-btn" type="button" data-full="{img_data_uri(rel)}" aria-label="点击放大截图：{esc(caption)}">'
        f'<img loading="lazy" src="{img_data_uri(rel)}" alt="{esc(caption)}">'
        '</button>'
        f'<figcaption><span class="time">{esc(ts)}</span>{esc(caption)}</figcaption>'
        '</figure>'
    )


def code_block(item: dict) -> str:
    return (
        '<div class="code-card">'
        f'<div class="code-title">{esc(item.get("caption", "代码"))}</div>'
        f'<pre><code>{esc(item.get("code", ""))}</code></pre>'
        '</div>'
    )


def section_html(sec: dict, idx: int) -> str:
    parts = [
        f'<section id="{esc(sec["id"])}" class="section-card">',
        f'<div class="section-kicker">{idx:02d} · {esc(sec.get("time", ""))}</div>',
        f'<h2>{esc(sec["title"])}</h2>',
        f'<p class="summary">{inline_mark(sec.get("summary", ""))}</p>',
        '<ul class="point-list">',
    ]
    for point in sec.get("points", []):
        parts.append(f'<li>{inline_mark(point)}</li>')
    parts.append('</ul>')
    for block in sec.get("code_blocks", []):
        parts.append(code_block(block))
    shots = sec.get("screenshots", [])
    if shots:
        parts.append('<div class="shot-grid">')
        for shot in shots:
            parts.append(figure(shot))
        parts.append('</div>')
    parts.append('</section>')
    return "\n".join(parts)


def framework_html(framework: list[dict]) -> str:
    cards = []
    for i, item in enumerate(framework, 1):
        children = "".join(f"<li>{inline_mark(child)}</li>" for child in item.get("children", []))
        cards.append(
            '<div class="framework-card">'
            f'<span class="badge">{i}</span>'
            f'<h3>{esc(item.get("title", ""))}</h3>'
            f'<ul>{children}</ul>'
            '</div>'
        )
    return "\n".join(cards)


def flow_html(flow: list[str]) -> str:
    return "\n".join(
        f'<div class="flow-node"><span>{i}</span><p>{esc(text)}</p></div>'
        for i, text in enumerate(flow, 1)
    )


def transcript_text() -> str:
    if TRANSCRIPT.exists():
        return TRANSCRIPT.read_text(encoding="utf-8", errors="ignore")
    return "未找到 transcript.p05.en.srt。"


def main() -> None:
    data = json.loads(CONTENT.read_text(encoding="utf-8"))
    meta = data["meta"]
    toc = "\n".join(
        f'<a href="#{esc(sec["id"])}"><span>{i:02d}</span>{esc(sec["title"])}</a>'
        for i, sec in enumerate(data["sections"], 1)
    )
    sections = "\n".join(section_html(sec, i) for i, sec in enumerate(data["sections"], 1))
    key_takeaways = "\n".join(f'<li>{inline_mark(x)}</li>' for x in data["key_takeaways"])
    author_logic = "\n".join(f'<li>{inline_mark(x)}</li>' for x in data["author_logic"])
    final_summary = "\n".join(f'<li>{inline_mark(x)}</li>' for x in data["final_summary"])
    action_items = "\n".join(f'<li>{inline_mark(x)}</li>' for x in data["action_items"])
    transcript = esc(transcript_text())

    doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(data['title'])}</title>
<style>
:root {{
  --bg:#f6f3ec; --bg-soft:#fffaf1; --paper:#fffdf8; --paper-2:#fff7e8;
  --text:#26322f; --muted:#6e7b74; --line:#e4dac9; --brand:#2f7d68;
  --brand-2:#c5633d; --accent:#e7a738; --code-bg:#f4efe6;
  --shadow:0 18px 50px rgba(74,54,32,.12); --radius:22px;
}}
body.dark {{
  --bg:#101615; --bg-soft:#141d1b; --paper:#192220; --paper-2:#202c29;
  --text:#ecf5ef; --muted:#aab9b1; --line:#30403b; --brand:#66d0af;
  --brand-2:#ff9d72; --accent:#ffd166; --code-bg:#0e1413;
  --shadow:0 18px 50px rgba(0,0,0,.35);
}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:radial-gradient(900px 520px at 80% -20%,rgba(47,125,104,.18),transparent 70%),var(--bg);color:var(--text);font:16px/1.75 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Segoe UI",sans-serif}}
a{{color:inherit}}
.layout{{display:grid;grid-template-columns:280px minmax(0,1fr);gap:34px;max-width:1320px;margin:0 auto;padding:0 28px}}
.toc{{position:sticky;top:0;height:100vh;padding:28px 18px 32px 0;overflow:auto;border-right:1px solid var(--line)}}
.toc h2{{font-size:1rem;margin:0 0 6px;color:var(--brand)}}
.toc p{{margin:0 0 18px;color:var(--muted);font-size:.86rem;line-height:1.5}}
.toc a{{display:flex;gap:10px;align-items:flex-start;padding:9px 10px;margin:4px 0;border-radius:12px;text-decoration:none;color:var(--muted);font-size:.9rem;line-height:1.35}}
.toc a span{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--brand);font-size:.78rem;margin-top:1px}}
.toc a:hover,.toc a.active{{background:var(--paper-2);color:var(--text)}}
main{{min-width:0;padding-bottom:90px}}
.hero{{padding:56px 0 34px}}
.eyebrow{{display:inline-flex;gap:8px;align-items:center;background:var(--paper-2);border:1px solid var(--line);border-radius:999px;padding:5px 13px;color:var(--brand);font-size:.82rem;font-weight:700}}
h1{{font-size:clamp(2rem,5vw,4.4rem);line-height:1.05;margin:22px 0 16px;letter-spacing:-.06em}}
.subtitle{{max-width:900px;color:var(--muted);font-size:1.08rem;margin:0}}
.toolbar{{position:fixed;right:22px;top:18px;display:flex;gap:10px;z-index:20}}
.toolbar button,.mobile-menu{{border:1px solid var(--line);background:var(--paper);color:var(--text);box-shadow:var(--shadow);border-radius:999px;padding:9px 13px;cursor:pointer}}
.mobile-menu{{display:none;position:fixed;left:16px;top:16px;z-index:25}}
.meta-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:26px 0}}
.meta-item{{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:15px 16px;box-shadow:var(--shadow)}}
.meta-item b{{display:block;color:var(--brand);font-size:.78rem;margin-bottom:5px}}
.panel,.section-card{{background:linear-gradient(180deg,var(--paper),var(--bg-soft));border:1px solid var(--line);border-radius:var(--radius);padding:28px;margin:22px 0;box-shadow:var(--shadow)}}
.panel h2,.section-card h2{{font-size:1.55rem;line-height:1.3;margin:0 0 12px;letter-spacing:-.03em}}
.summary{{font-size:1.02rem;color:var(--text);background:var(--paper-2);border-left:4px solid var(--brand);padding:14px 16px;border-radius:14px;margin:12px 0 18px}}
.quick-list,.point-list,.clean-list{{padding-left:1.25rem;margin:12px 0}}
li{{margin:8px 0}}
strong{{color:var(--brand-2)}}
code{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--code-bg);border:1px solid var(--line);border-radius:6px;padding:.1em .35em}}
.framework{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}}
.framework-card{{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:18px}}
.framework-card .badge{{display:inline-grid;place-items:center;width:30px;height:30px;border-radius:10px;background:var(--brand);color:#fff;font-weight:800}}
.framework-card h3{{margin:10px 0 8px;font-size:1.05rem}}
.flow{{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-top:16px}}
.flow-node{{position:relative;background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:13px;min-height:108px}}
.flow-node:not(:last-child)::after{{content:"→";position:absolute;right:-12px;top:39px;color:var(--brand);font-weight:900}}
.flow-node span{{display:inline-grid;place-items:center;width:24px;height:24px;border-radius:8px;background:var(--accent);color:#382800;font-weight:800;font-size:.78rem}}
.flow-node p{{margin:9px 0 0;line-height:1.45;font-size:.9rem}}
.section-kicker{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--brand);font-size:.88rem;margin-bottom:8px}}
.shot-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:20px}}
.shot{{margin:0}}
.shot-btn{{display:block;width:100%;border:0;background:transparent;padding:0;cursor:zoom-in}}
.shot img{{display:block;width:100%;border-radius:18px;border:1px solid var(--line);box-shadow:0 12px 30px rgba(44,35,23,.14)}}
figcaption{{color:var(--muted);font-size:.88rem;line-height:1.55;margin-top:8px;text-align:center}}
.time{{display:inline-block;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:#fff;background:var(--brand);border-radius:999px;padding:1px 8px;margin-right:8px;font-size:.78rem}}
.code-card{{margin:18px 0;background:var(--code-bg);border:1px solid var(--line);border-radius:18px;overflow:hidden}}
.code-title{{padding:10px 14px;border-bottom:1px solid var(--line);color:var(--brand);font-weight:700;font-size:.9rem}}
pre{{margin:0;padding:16px;overflow:auto;font-size:.86rem;line-height:1.6}}
.two-col{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
details{{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:16px;margin:20px 0}}
summary{{cursor:pointer;font-weight:800;color:var(--brand)}}
.transcript{{white-space:pre-wrap;max-height:420px;overflow:auto;background:var(--code-bg);border-radius:14px;padding:14px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.82rem;line-height:1.55}}
#topBtn{{position:fixed;right:22px;bottom:22px;z-index:20;border:1px solid var(--line);background:var(--brand);color:#fff;border-radius:999px;padding:11px 14px;box-shadow:var(--shadow);cursor:pointer;display:none}}
.lightbox{{position:fixed;inset:0;background:rgba(0,0,0,.82);display:none;align-items:center;justify-content:center;padding:28px;z-index:50}}
.lightbox.open{{display:flex}}
.lightbox img{{max-width:min(1200px,96vw);max-height:88vh;border-radius:16px;background:#fff}}
.lightbox button{{position:absolute;right:22px;top:18px;border:0;background:#fff;color:#111;border-radius:999px;padding:9px 13px;cursor:pointer}}
@media(max-width:980px){{.layout{{display:block;padding:0 16px}}.toc{{position:fixed;left:0;top:0;bottom:0;width:82vw;max-width:330px;background:var(--bg);z-index:24;transform:translateX(-105%);transition:.2s;padding:70px 18px 22px;border-right:1px solid var(--line)}}body.toc-open .toc{{transform:translateX(0)}}.mobile-menu{{display:block}}.toolbar{{top:16px;right:16px}}.meta-grid,.framework,.two-col,.shot-grid{{grid-template-columns:1fr}}.flow{{grid-template-columns:1fr}}.flow-node:not(:last-child)::after{{content:"↓";right:50%;top:auto;bottom:-17px}}.hero{{padding-top:76px}}}}
</style>
</head>
<body>
<button class="mobile-menu" id="menuBtn">目录</button>
<div class="toolbar"><button id="themeBtn">明暗切换</button></div>
<div class="layout">
  <nav class="toc" id="toc">
    <h2>章节目录</h2>
    <p>{esc(meta['part_title'])} · {esc(meta['duration'])}</p>
    <a href="#overview"><span>00</span>视频概览</a>
    <a href="#framework"><span>F</span>整体框架</a>
    {toc}
    <a href="#wrapup"><span>Z</span>复盘与落地</a>
  </nav>
  <main>
    <header class="hero" id="overview">
      <span class="eyebrow">LlamaIndex · Agentic RAG · P{esc(meta['page'])}</span>
      <h1>{esc(data['title'])}</h1>
      <p class="subtitle">{esc(data['overview'])}</p>
      <div class="meta-grid">
        <div class="meta-item"><b>视频标题</b>{esc(meta['part_title'])}</div>
        <div class="meta-item"><b>UP 主</b>{esc(meta['up'])}</div>
        <div class="meta-item"><b>总时长</b>{esc(meta['duration'])}</div>
        <div class="meta-item"><b>内容类型</b>{esc(meta['content_type'])}</div>
      </div>
    </header>

    <section class="panel">
      <h2>10 秒核心要点速览</h2>
      <ul class="quick-list">{key_takeaways}</ul>
    </section>

    <section class="panel" id="framework">
      <h2>整体框架与讲解思路</h2>
      <div class="framework">{framework_html(data['framework'])}</div>
      <h2 style="margin-top:28px">作者讲解逻辑</h2>
      <ol class="clean-list">{author_logic}</ol>
      <h2 style="margin-top:28px">端到端流程</h2>
      <div class="flow">{flow_html(data['flow'])}</div>
    </section>

    {sections}

    <section class="panel" id="wrapup">
      <h2>结尾总结与价值提炼</h2>
      <div class="two-col">
        <div>
          <h3>核心内容复盘</h3>
          <ul class="clean-list">{final_summary}</ul>
        </div>
        <div>
          <h3>落地行动建议</h3>
          <ul class="clean-list">{action_items}</ul>
        </div>
      </div>
      <details>
        <summary>查看英文转录全文（用于回溯核对）</summary>
        <div class="transcript">{transcript}</div>
      </details>
    </section>
  </main>
</div>
<button id="topBtn">↑ 顶部</button>
<div class="lightbox" id="lightbox"><button id="closeLightbox">关闭</button><img alt="放大截图" id="lightboxImg"></div>
<script>
const body = document.body;
const themeBtn = document.getElementById('themeBtn');
const savedTheme = localStorage.getItem('p05-theme');
if (savedTheme === 'dark') body.classList.add('dark');
themeBtn.addEventListener('click', () => {{
  body.classList.toggle('dark');
  localStorage.setItem('p05-theme', body.classList.contains('dark') ? 'dark' : 'light');
}});
document.getElementById('menuBtn').addEventListener('click', () => body.classList.toggle('toc-open'));
document.querySelectorAll('.toc a').forEach(a => a.addEventListener('click', () => body.classList.remove('toc-open')));
const topBtn = document.getElementById('topBtn');
window.addEventListener('scroll', () => {{ topBtn.style.display = window.scrollY > 600 ? 'block' : 'none'; }});
topBtn.addEventListener('click', () => window.scrollTo({{top:0, behavior:'smooth'}}));
const links = [...document.querySelectorAll('.toc a')];
const targets = links.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
window.addEventListener('scroll', () => {{
  let current = targets[0];
  for (const t of targets) if (t.getBoundingClientRect().top < 140) current = t;
  links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + current.id));
}});
const box = document.getElementById('lightbox');
const boxImg = document.getElementById('lightboxImg');
document.querySelectorAll('.shot-btn').forEach(btn => btn.addEventListener('click', () => {{
  boxImg.src = btn.dataset.full; box.classList.add('open');
}}));
function closeLightbox() {{ box.classList.remove('open'); boxImg.removeAttribute('src'); }}
document.getElementById('closeLightbox').addEventListener('click', closeLightbox);
box.addEventListener('click', e => {{ if (e.target === box) closeLightbox(); }});
document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeLightbox(); }});
</script>
</body>
</html>
"""
    OUT.write_text(doc, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
