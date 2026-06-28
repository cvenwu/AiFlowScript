# FastAPI Agent Backend Roadmap HTML Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a polished, offline-openable single-file HTML roadmap for the approved「Go 服务端工程师的 FastAPI Agent Backend 进阶路线」design.

**Architecture:** This plan implements the first independently testable deliverable from the approved spec: `fastapi-agent-backend-roadmap.html`. The page is a static single HTML file with embedded CSS and semantic sections; a lightweight Python validation script checks content coverage, offline constraints, and required section IDs.

**Tech Stack:** HTML5, CSS3, Python standard library, local browser preview on macOS.

## Global Constraints

- Primary working directory: `/Users/bytedance/Documents/workspace/personal_workspace/github_workspace/AiFlowScript/fast-api-demo`.
- Approved design spec: `docs/superpowers/specs/2026-06-28-fastapi-agent-backend-roadmap-design.md`.
- HTML output path: `fastapi-agent-backend-roadmap.html`.
- The HTML must be a single file, offline-openable, and must not depend on external CDN, remote fonts, remote scripts, or remote images.
- The HTML must include 11 sections: Hero、当前起点、三层能力目标、4 周路线图、项目演进路径、最终架构图、API 总览、核心数据模型、Go ↔ FastAPI 概念对照、测试与验收标准、面试讲述模板。
- The visual style must use a dark technical roadmap aesthetic, card layout, timeline progression, architecture/process diagrams, comparison tables, and interview-ready copy.
- Do not implement FastAPI application code in this plan; the backend project implementation gets its own later plan.
- Keep changes focused on the HTML roadmap and its validation only.

---

## File Structure

- Create: `fastapi-agent-backend-roadmap.html`
  - Responsibility: single-file visual roadmap containing all approved learning route, architecture, API, testing, and interview content.
- Create: `scripts/validate_roadmap_html.py`
  - Responsibility: verify the HTML is offline-safe and contains all required section IDs and key phrases.
- No changes to FastAPI runtime files in this plan.

---

### Task 1: Add HTML Contract Validation

**Files:**
- Create: `scripts/validate_roadmap_html.py`
- Test target: `fastapi-agent-backend-roadmap.html`

**Interfaces:**
- Consumes: file path argument passed on CLI as `python scripts/validate_roadmap_html.py fastapi-agent-backend-roadmap.html`.
- Produces: exit code `0` and line `Roadmap HTML validation passed` when the HTML satisfies the contract; non-zero exit with clear error message otherwise.

- [ ] **Step 1: Create the validation script**

Create `scripts/validate_roadmap_html.py` with this complete content:

```python
from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_SECTION_IDS = [
    "hero",
    "current-start",
    "capabilities",
    "weekly-roadmap",
    "project-evolution",
    "architecture",
    "api-overview",
    "data-models",
    "go-fastapi-map",
    "testing-acceptance",
    "interview-story",
]

REQUIRED_KEY_PHRASES = [
    "Go 服务端工程师",
    "FastAPI Agent Backend",
    "每天约 2 小时",
    "Task CRUD",
    "Conversation",
    "Message",
    "Tool",
    "AgentRun",
    "SSE",
    "Pydantic",
    "APIRouter",
    "pytest",
    "TestClient",
    "Mock LLM Provider",
    "30 秒版本",
    "2 分钟版本",
]

FORBIDDEN_PATTERNS = [
    r"https?://",
    r"<script\b",
    r"@import\b",
    r"cdn\.",
    r"fonts\.googleapis",
    r"fonts\.gstatic",
]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_roadmap_html.py <html-file>", file=sys.stderr)
        return 2

    html_path = Path(sys.argv[1])
    if not html_path.exists():
        print(f"Missing HTML file: {html_path}", file=sys.stderr)
        return 1

    html = html_path.read_text(encoding="utf-8")

    missing_sections = [
        section_id
        for section_id in REQUIRED_SECTION_IDS
        if f'id="{section_id}"' not in html and f"id='{section_id}'" not in html
    ]
    if missing_sections:
        print(f"Missing required section ids: {', '.join(missing_sections)}", file=sys.stderr)
        return 1

    missing_phrases = [phrase for phrase in REQUIRED_KEY_PHRASES if phrase not in html]
    if missing_phrases:
        print(f"Missing required phrases: {', '.join(missing_phrases)}", file=sys.stderr)
        return 1

    forbidden_hits = [pattern for pattern in FORBIDDEN_PATTERNS if re.search(pattern, html, flags=re.I)]
    if forbidden_hits:
        print(f"Forbidden offline-unsafe patterns found: {', '.join(forbidden_hits)}", file=sys.stderr)
        return 1

    if "<style>" not in html or "</style>" not in html:
        print("Missing embedded <style> block", file=sys.stderr)
        return 1

    if len(html) < 20_000:
        print("HTML looks too small to contain the approved roadmap content", file=sys.stderr)
        return 1

    print("Roadmap HTML validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run validation before HTML exists and verify it fails correctly**

Run:

```bash
python scripts/validate_roadmap_html.py fastapi-agent-backend-roadmap.html
```

Expected: command exits non-zero and prints:

```text
Missing HTML file: fastapi-agent-backend-roadmap.html
```

- [ ] **Step 3: Commit validation script**

Run:

```bash
git add scripts/validate_roadmap_html.py
git commit -m "test: add roadmap HTML validation"
```

Expected: commit succeeds and includes only `scripts/validate_roadmap_html.py`.

---

### Task 2: Create Single-File HTML Shell and Core Layout

**Files:**
- Create: `fastapi-agent-backend-roadmap.html`
- Modify: `fastapi-agent-backend-roadmap.html`
- Test: `scripts/validate_roadmap_html.py`

**Interfaces:**
- Consumes: validation contract from `scripts/validate_roadmap_html.py`.
- Produces: a UTF-8 HTML file with embedded CSS and required section IDs.

- [ ] **Step 1: Create the HTML file with embedded CSS and all required sections**

Create `fastapi-agent-backend-roadmap.html` with this initial structure. Keep all section IDs exactly as shown because the validator depends on them:

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Go 服务端工程师的 FastAPI Agent Backend 进阶路线</title>
  <style>
    :root {
      --bg: #070b14;
      --panel: #101827;
      --panel-2: #0d1321;
      --text: #e8eefc;
      --muted: #9aa8c7;
      --line: rgba(148, 163, 184, 0.22);
      --cyan: #38d9ff;
      --green: #7cffb2;
      --violet: #a78bfa;
      --amber: #ffd166;
      --red: #ff6b6b;
      --radius: 24px;
      --shadow: 0 24px 80px rgba(0, 0, 0, 0.34);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at 10% 0%, rgba(56, 217, 255, 0.16), transparent 28%),
        radial-gradient(circle at 85% 10%, rgba(167, 139, 250, 0.18), transparent 30%),
        linear-gradient(180deg, #070b14 0%, #0a1020 48%, #060912 100%);
      line-height: 1.65;
    }
    a { color: inherit; }
    .page { width: min(1180px, calc(100% - 40px)); margin: 0 auto; padding: 48px 0 80px; }
    .hero { min-height: 72vh; display: grid; align-items: center; position: relative; }
    .eyebrow { color: var(--green); text-transform: uppercase; letter-spacing: 0.18em; font-size: 13px; font-weight: 800; }
    h1 { margin: 16px 0 20px; font-size: clamp(42px, 7vw, 88px); line-height: 0.96; letter-spacing: -0.06em; }
    h2 { margin: 0 0 18px; font-size: clamp(28px, 4vw, 46px); letter-spacing: -0.04em; }
    h3 { margin: 0 0 12px; font-size: 22px; }
    p { margin: 0 0 14px; color: var(--muted); }
    section { margin: 42px 0; scroll-margin-top: 24px; }
    .lead { max-width: 820px; font-size: 21px; color: #cbd7f6; }
    .grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 18px; }
    .card {
      background: linear-gradient(180deg, rgba(16, 24, 39, 0.92), rgba(13, 19, 33, 0.88));
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 24px;
    }
    .span-4 { grid-column: span 4; }
    .span-6 { grid-column: span 6; }
    .span-8 { grid-column: span 8; }
    .span-12 { grid-column: span 12; }
    .pill { display: inline-flex; padding: 7px 11px; border: 1px solid var(--line); border-radius: 999px; color: #dbe7ff; background: rgba(255,255,255,0.05); font-size: 13px; margin: 4px 6px 4px 0; }
    .metric { font-size: 36px; font-weight: 900; color: var(--cyan); letter-spacing: -0.04em; }
    .timeline { display: grid; gap: 16px; }
    .week { position: relative; padding-left: 26px; border-left: 2px solid rgba(56, 217, 255, 0.35); }
    .week::before { content: ""; position: absolute; left: -7px; top: 8px; width: 12px; height: 12px; border-radius: 50%; background: var(--cyan); box-shadow: 0 0 24px var(--cyan); }
    .flow { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
    .node { padding: 12px 14px; border: 1px solid var(--line); border-radius: 16px; background: rgba(56, 217, 255, 0.07); color: #eaf6ff; font-weight: 750; }
    .arrow { color: var(--amber); font-weight: 900; }
    table { width: 100%; border-collapse: collapse; overflow: hidden; border-radius: 18px; border: 1px solid var(--line); }
    th, td { padding: 14px 16px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
    th { color: var(--green); background: rgba(124, 255, 178, 0.07); }
    code, pre { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; }
    pre { margin: 0; padding: 18px; overflow: auto; border-radius: 18px; background: #050812; border: 1px solid var(--line); color: #cfe7ff; }
    .diagram { display: grid; gap: 12px; }
    .layer { display: grid; grid-template-columns: 180px 1fr; gap: 12px; align-items: center; }
    .layer-label { color: var(--amber); font-weight: 900; }
    .layer-box { padding: 14px 16px; border-radius: 16px; border: 1px solid var(--line); background: rgba(167, 139, 250, 0.08); }
    .quote { border-left: 4px solid var(--green); padding-left: 18px; color: #d9e6ff; }
    .footer { margin-top: 70px; color: var(--muted); text-align: center; }
    @media (max-width: 820px) {
      .page { width: min(100% - 24px, 1180px); padding-top: 24px; }
      .span-4, .span-6, .span-8 { grid-column: span 12; }
      .layer { grid-template-columns: 1fr; }
      h1 { font-size: 42px; }
    }
  </style>
</head>
<body>
  <main class="page">
    <section id="hero" class="hero"></section>
    <section id="current-start"></section>
    <section id="capabilities"></section>
    <section id="weekly-roadmap"></section>
    <section id="project-evolution"></section>
    <section id="architecture"></section>
    <section id="api-overview"></section>
    <section id="data-models"></section>
    <section id="go-fastapi-map"></section>
    <section id="testing-acceptance"></section>
    <section id="interview-story"></section>
    <footer class="footer">FastAPI Agent Backend Roadmap · Offline HTML</footer>
  </main>
</body>
</html>
```

- [ ] **Step 2: Run validation and verify expected content failure**

Run:

```bash
python scripts/validate_roadmap_html.py fastapi-agent-backend-roadmap.html
```

Expected: command exits non-zero and prints missing required phrases, because the shell has section IDs but not final content yet.

- [ ] **Step 3: Commit HTML shell**

Run:

```bash
git add fastapi-agent-backend-roadmap.html
git commit -m "feat: add roadmap HTML shell"
```

Expected: commit succeeds and includes only `fastapi-agent-backend-roadmap.html`.

---

### Task 3: Fill Roadmap Content Sections

**Files:**
- Modify: `fastapi-agent-backend-roadmap.html`
- Source reference: `docs/superpowers/specs/2026-06-28-fastapi-agent-backend-roadmap-design.md`
- Test: `scripts/validate_roadmap_html.py`

**Interfaces:**
- Consumes: required section IDs from Task 2.
- Produces: completed readable content covering all 11 approved HTML sections.

- [ ] **Step 1: Replace empty section bodies with approved content**

Edit only the section bodies inside `fastapi-agent-backend-roadmap.html`. Use these exact section structures and keep the existing CSS unchanged.

For `#hero`, use:

```html
<div>
  <div class="eyebrow">FastAPI · Python Engineering · AI Agent Backend</div>
  <h1>从 Go 服务端到 FastAPI Agent Backend</h1>
  <p class="lead">用 4 周时间，从 FastAPI CRUD 演进到简化版 AI Agent 后端。每天约 2 小时，建立 Python Web 工程化、SSE 流式响应、Tool 抽象和面试可讲述项目经验。</p>
  <div>
    <span class="pill">Go 服务端工程师</span>
    <span class="pill">FastAPI Agent Backend</span>
    <span class="pill">每天约 2 小时</span>
    <span class="pill">面试 / 转岗可讲述</span>
  </div>
</div>
```

For `#current-start`, use a heading `当前起点` and three cards describing: current project is `fast-api-demo`, current Python level is simple scripts, final goal is interview-ready Agent Backend.

For `#capabilities`, create three `.span-4.card` cards titled `FastAPI 基础能力`, `Python 服务端工程能力`, and `AI Agent 后端能力`. Include these phrases across the cards: `APIRouter`, `Pydantic`, `pytest`, `TestClient`, `async/await`, `Conversation`, `Message`, `Tool`, `AgentRun`, `SSE`, `Mock LLM Provider`.

For `#weekly-roadmap`, create four `.week.card` blocks:

```html
<div class="week card"><h3>Week 1 · FastAPI 基础 CRUD</h3><p>Health API、Task CRUD、Pydantic、HTTPException、TestClient。</p></div>
<div class="week card"><h3>Week 2 · 工程化后端结构</h3><p>APIRouter 拆分、service/repository 分层、SQLite、配置、日志、异常。</p></div>
<div class="week card"><h3>Week 3 · Agent Backend Core</h3><p>Conversation、Message、Tool、Mock LLM Provider、AgentRun 状态机。</p></div>
<div class="week card"><h3>Week 4 · Streaming + Interview Story</h3><p>StreamingResponse、SSE token streaming、集成测试、30 秒版本和 2 分钟版本面试表达。</p></div>
```

For `#project-evolution`, create a `.flow.card` with these nodes in order: `Hello Script`, `Health API`, `Task CRUD`, `DB-backed Service`, `Conversation / Message`, `Tool + Mock LLM`, `AgentRun`, `SSE Events`.

For `#architecture`, create a layered diagram with these rows: `Client`, `api/routes`, `schemas`, `services`, `repositories -> models -> db`, `llm provider`, `tool service -> builtin tools`, `core`.

For `#api-overview`, include a table with API groups and endpoints for Health, Tasks, Conversations, Tools, Agent. Include every endpoint from the approved spec.

For `#data-models`, include five cards: Task, Conversation, Message, Tool, AgentRun. Include fields exactly as described in the spec, including `role: user | assistant | tool` and `status: pending | running | succeeded | failed`.

For `#go-fastapi-map`, include a table mapping Gin/Hertz Router to APIRouter, struct binding to Pydantic, handler to route function, service layer to services, dao to repositories, gorm.DB to SQLAlchemy Session, goroutine to asyncio task, streaming response to StreamingResponse / SSE.

For `#testing-acceptance`, include four cards for Week 1-4 acceptance. Mention `pytest`, `TestClient`, `404`, `422`, database isolation, AgentRun state transition, and SSE events.

For `#interview-story`, include three cards: `30 秒版本`, `2 分钟版本`, and `深挖问题`. The 30-second and 2-minute copy should match the approved design spec closely. The deep-dive list must include why FastAPI, why service/repository, why AgentRun, why SSE, why not LangChain / LangGraph first.

- [ ] **Step 2: Run validation and verify it passes**

Run:

```bash
python scripts/validate_roadmap_html.py fastapi-agent-backend-roadmap.html
```

Expected:

```text
Roadmap HTML validation passed
```

- [ ] **Step 3: Commit roadmap content**

Run:

```bash
git add fastapi-agent-backend-roadmap.html
git commit -m "feat: fill FastAPI Agent roadmap content"
```

Expected: commit succeeds and includes the completed HTML content.

---

### Task 4: Polish Visual Hierarchy and Local Preview

**Files:**
- Modify: `fastapi-agent-backend-roadmap.html`
- Test: `scripts/validate_roadmap_html.py`

**Interfaces:**
- Consumes: completed content from Task 3.
- Produces: polished offline HTML ready for local review.

- [ ] **Step 1: Improve visual scanability without adding external dependencies**

Modify the existing `<style>` block only. Add these CSS rules below the existing `.quote` rule:

```css
.section-head { margin-bottom: 20px; }
.section-kicker { color: var(--cyan); font-size: 13px; font-weight: 900; letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 8px; }
.muted-list { margin: 10px 0 0; padding-left: 20px; color: var(--muted); }
.muted-list li { margin: 7px 0; }
.api-method { display: inline-block; min-width: 64px; color: var(--green); font-weight: 900; }
.status { display: inline-flex; align-items: center; gap: 8px; margin: 4px 8px 4px 0; padding: 8px 10px; border-radius: 999px; border: 1px solid var(--line); background: rgba(255,255,255,0.045); }
.status::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: var(--green); box-shadow: 0 0 16px var(--green); }
.callout { background: linear-gradient(135deg, rgba(56,217,255,0.12), rgba(167,139,250,0.11)); border: 1px solid rgba(56,217,255,0.28); }
.print-note { color: var(--muted); font-size: 13px; }
@media print {
  body { background: #ffffff; color: #111827; }
  .card, pre, table { box-shadow: none; border-color: #d1d5db; }
  p, .muted-list, .footer { color: #374151; }
}
```

Then use `.section-head`, `.section-kicker`, `.callout`, and `.muted-list` in the HTML sections where helpful. Do not change section IDs.

- [ ] **Step 2: Validate offline safety again**

Run:

```bash
python scripts/validate_roadmap_html.py fastapi-agent-backend-roadmap.html
```

Expected:

```text
Roadmap HTML validation passed
```

- [ ] **Step 3: Open the local HTML preview**

Run on macOS:

```bash
open fastapi-agent-backend-roadmap.html
```

Expected: the browser opens the local file. Review these visible checks manually:

```text
1. Hero title is readable without scrolling on a laptop-sized window.
2. 4-week roadmap appears as a timeline.
3. Architecture section clearly shows route -> service -> repository/db plus llm/tools.
4. API overview table includes all endpoint groups.
5. Interview section includes 30 秒版本 and 2 分钟版本.
```

- [ ] **Step 4: Commit visual polish**

Run:

```bash
git add fastapi-agent-backend-roadmap.html
git commit -m "style: polish roadmap HTML presentation"
```

Expected: commit succeeds and includes only visual/content polish for the HTML file.

---

### Task 5: Final Verification and Handoff

**Files:**
- Modify: none unless verification finds a concrete defect.
- Test: `scripts/validate_roadmap_html.py`

**Interfaces:**
- Consumes: completed HTML and validation script from previous tasks.
- Produces: final handoff summary with local path and next execution choices.

- [ ] **Step 1: Run final validator**

Run:

```bash
python scripts/validate_roadmap_html.py fastapi-agent-backend-roadmap.html
```

Expected:

```text
Roadmap HTML validation passed
```

- [ ] **Step 2: Check Git status**

Run:

```bash
git status --short
```

Expected: no uncommitted changes from this plan. Existing unrelated untracked files outside `fast-api-demo` may still appear and should not be committed by this plan.

- [ ] **Step 3: Report completion to user**

Use this response structure:

```text
已完成本地单文件 HTML 路线图：
- 文件：fastapi-agent-backend-roadmap.html
- 验证：python scripts/validate_roadmap_html.py fastapi-agent-backend-roadmap.html 通过
- 打开方式：open fastapi-agent-backend-roadmap.html

下一步可以选择：
1. 继续做在线预览 / GitHub Pages 部署计划
2. 开始 FastAPI 项目第 1 周代码实施计划
```

---

## Self-Review

**Spec coverage:** This plan implements the approved HTML deliverable only. It covers the 11 HTML sections, offline single-file requirement, dark technical roadmap style, architecture/API/model/testing/interview content, and local preview. It intentionally excludes FastAPI app code because the approved spec says HTML should be generated before backend code implementation.

**Placeholder scan:** The plan contains no unresolved placeholders and no deferred implementation markers. Each task has exact paths, commands, expected outputs, and concrete code or HTML/CSS structure.

**Type and interface consistency:** The validator path, HTML path, section IDs, and required phrases are consistent across all tasks. Later tasks consume `fastapi-agent-backend-roadmap.html` and `scripts/validate_roadmap_html.py` exactly as created in earlier tasks.
