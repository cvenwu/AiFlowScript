# bilibili-video-summarizer Skill 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 交付一个可用的 `bilibili-video-summarizer` skill，输入 B 站视频链接后，自动校验 cookie、拉取字幕（无则降级 Whisper 转录）、抽取关键帧，并生成带 Mermaid 图与截图的 Markdown 学习笔记。

**Architecture:** 单个 skill 目录，脚本层（`scripts/bili_summarize.py`）负责所有确定性取数（cookie 校验、字幕拉取、抽帧），以 JSON 形式输出结果；Agent 层通过 `SKILL.md` 编排流程，读取 JSON 后创作 Markdown。子命令 `check` 与 `fetch` 分离，便于分阶段调用与错误处理。

**Tech Stack:** Python 3.9+、`requests`、`yt-dlp`（下载视频/字幕）、`ffmpeg`（关键帧抽取、抽音频）、`openai-whisper`（无字幕降级转录）。

## Global Constraints

- Skill 目录：`bilibili-video-summarizer/`
- Cookie 环境变量名：`BILIBILI_COOKIE`
- B 站登录态校验接口：`https://api.bilibili.com/x/web-interface/nav`
- 抽帧参数：场景阈值 `scene > 0.4`、最多 15 张、少于 3 张时降级为均匀抽帧（8~12 张）
- 关键帧命名：`frame_<秒>.jpg`（秒数补零 4 位），存于 `workdir/frames/`
- Markdown 文件名：`学习笔记.md`，位于 `workdir/` 下
- 输出根目录默认为当前工作目录
- 视频源文件默认在抽帧后删除，`--keep-video` 开关可保留
- 技能代码写入 AiFlowScript 仓库顶层目录 `bilibili-video-summarizer/`

---

## File Structure

- `bilibili-video-summarizer/SKILL.md` —— skill 主入口，含 frontmatter + 编排流程 + Markdown 撰写指引
- `bilibili-video-summarizer/scripts/bili_summarize.py` —— 主脚本，提供 `check` 与 `fetch` 两个子命令
- `bilibili-video-summarizer/scripts/requirements.txt` —— Python 依赖清单
- `bilibili-video-summarizer/references/troubleshooting.md` —— 常见故障排查
- `bilibili-video-summarizer/tests/test_bili_summarize.py` —— 单元测试
- `bilibili-video-summarizer/tests/fixtures/nav_valid.json` —— B 站 nav 接口合法响应示例
- `bilibili-video-summarizer/tests/fixtures/nav_invalid.json` —— B 站 nav 接口未登录响应示例
- `bilibili-video-summarizer/tests/fixtures/subtitle_sample.json` —— B 站字幕 JSON 样本

---

## Task 1：脚手架与依赖清单

**Files:**
- Create: `bilibili-video-summarizer/SKILL.md`
- Create: `bilibili-video-summarizer/scripts/requirements.txt`
- Create: `bilibili-video-summarizer/scripts/bili_summarize.py`（先创建带 `if __name__ == "__main__"` 骨架）
- Create: `bilibili-video-summarizer/tests/__init__.py`
- Create: `bilibili-video-summarizer/tests/test_bili_summarize.py`（占位一个 smoke test）

**Interfaces:**
- Consumes: 无
- Produces: 模块 `bili_summarize` 可通过 `python3 scripts/bili_summarize.py --help` 打印帮助；`check` 与 `fetch` 两个子命令注册（尚未实现具体逻辑，先 `raise NotImplementedError`）。

- [ ] **Step 1：创建目录结构**

```bash
mkdir -p bilibili-video-summarizer/scripts
mkdir -p bilibili-video-summarizer/references
mkdir -p bilibili-video-summarizer/tests/fixtures
```

- [ ] **Step 2：写 requirements.txt**

`bilibili-video-summarizer/scripts/requirements.txt`:

```
requests>=2.31
yt-dlp>=2024.03.10
openai-whisper>=20231117
```

- [ ] **Step 3：写占位 SKILL.md（frontmatter + 空章节）**

`bilibili-video-summarizer/SKILL.md`：

```markdown
---
name: bilibili-video-summarizer
description: "输入 B 站视频链接，自动校验 BILIBILI_COOKIE 有效性、拉取字幕(无则本地 Whisper 转录)、抽取关键帧，生成带 Mermaid 图与截图的中文 Markdown 学习笔记。触发词：B 站视频总结、bilibili 学习笔记、视频知识点提炼。"
version: 0.1.0
---

# bilibili-video-summarizer

（后续任务填充）
```

- [ ] **Step 4：写主脚本骨架**

`bilibili-video-summarizer/scripts/bili_summarize.py`：

```python
#!/usr/bin/env python3
"""bilibili-video-summarizer 主脚本。

提供两个子命令：
    check              校验 BILIBILI_COOKIE 是否合法
    fetch --url --outdir   拉取视频信息、字幕/转录、关键帧并输出 JSON
"""

import argparse
import sys


def cmd_check(_args: argparse.Namespace) -> int:
    raise NotImplementedError


def cmd_fetch(_args: argparse.Namespace) -> int:
    raise NotImplementedError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bili_summarize")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check", help="校验 BILIBILI_COOKIE").set_defaults(func=cmd_check)

    f = sub.add_parser("fetch", help="拉取视频数据")
    f.add_argument("--url", required=True)
    f.add_argument("--outdir", required=True)
    f.add_argument("--keep-video", action="store_true")
    f.set_defaults(func=cmd_fetch)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5：写占位 smoke test**

`bilibili-video-summarizer/tests/test_bili_summarize.py`：

```python
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "bili_summarize.py"


def test_help_runs():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "check" in result.stdout
    assert "fetch" in result.stdout
```

- [ ] **Step 6：运行测试确认通过**

Run: `pytest bilibili-video-summarizer/tests/test_bili_summarize.py -v`
Expected: 1 passed。

- [ ] **Step 7：提交**

```bash
git add SkillCollections/bilibili-video-summarizer
git commit -m "feat(bilibili-video-summarizer): scaffold skill directory and CLI skeleton"
```

---

## Task 2：`check` 子命令实现（cookie 校验）

**Files:**
- Modify: `bilibili-video-summarizer/scripts/bili_summarize.py`（实现 `cmd_check` 与辅助函数 `validate_cookie`）
- Create: `bilibili-video-summarizer/tests/fixtures/nav_valid.json`
- Create: `bilibili-video-summarizer/tests/fixtures/nav_invalid.json`
- Modify: `bilibili-video-summarizer/tests/test_bili_summarize.py`（新增用例）

**Interfaces:**
- Consumes: 环境变量 `BILIBILI_COOKIE`
- Produces:
  - `validate_cookie(cookie: str | None, session: requests.Session | None = None) -> dict`：返回 `{"valid": bool, ...}`，`reason` 取值 `"not_set" | "invalid" | "expired"`（当前实现里合并 `invalid`/`expired` 用 `"invalid"`，`SESSDATA` 缺失时用 `"invalid"`）。
  - `cmd_check(args) -> int`：向 stdout 打印 JSON，valid 时退出码 0，否则 1。

- [ ] **Step 1：写 fixtures**

`tests/fixtures/nav_valid.json`：

```json
{"code": 0, "message": "0", "data": {"isLogin": true, "uname": "test_user", "mid": 12345}}
```

`tests/fixtures/nav_invalid.json`：

```json
{"code": -101, "message": "账号未登录", "data": {"isLogin": false}}
```

- [ ] **Step 2：写失败测试**

在 `tests/test_bili_summarize.py` 末尾追加：

```python
import json
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(SCRIPT.parent))
import bili_summarize as bs  # noqa: E402


def _fixture(name):
    return json.loads((Path(__file__).parent / "fixtures" / name).read_text())


def test_validate_cookie_not_set():
    result = bs.validate_cookie(None)
    assert result == {"valid": False, "reason": "not_set"}


def test_validate_cookie_valid():
    session = MagicMock()
    resp = MagicMock()
    resp.json.return_value = _fixture("nav_valid.json")
    resp.raise_for_status = MagicMock()
    session.get.return_value = resp

    result = bs.validate_cookie("SESSDATA=abc; bili_jct=x", session=session)
    assert result == {"valid": True, "uname": "test_user", "mid": 12345}


def test_validate_cookie_invalid():
    session = MagicMock()
    resp = MagicMock()
    resp.json.return_value = _fixture("nav_invalid.json")
    resp.raise_for_status = MagicMock()
    session.get.return_value = resp

    result = bs.validate_cookie("SESSDATA=stale", session=session)
    assert result == {"valid": False, "reason": "invalid"}


def test_validate_cookie_missing_sessdata():
    result = bs.validate_cookie("some=thing")
    assert result == {"valid": False, "reason": "invalid"}
```

- [ ] **Step 3：运行测试确认失败**

Run: `pytest bilibili-video-summarizer/tests -v`
Expected: 4 个新测试 FAIL（`validate_cookie` 不存在）。

- [ ] **Step 4：实现 `validate_cookie` 与 `cmd_check`**

在 `bili_summarize.py` 中，替换 `cmd_check` 部分并新增函数：

```python
import json
import os
import requests

NAV_URL = "https://api.bilibili.com/x/web-interface/nav"


def validate_cookie(cookie, session=None):
    if not cookie:
        return {"valid": False, "reason": "not_set"}
    if "SESSDATA=" not in cookie:
        return {"valid": False, "reason": "invalid"}

    sess = session or requests.Session()
    headers = {
        "Cookie": cookie,
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.bilibili.com",
    }
    try:
        resp = sess.get(NAV_URL, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return {"valid": False, "reason": "invalid"}

    payload = data.get("data") or {}
    if data.get("code") == 0 and payload.get("isLogin"):
        return {
            "valid": True,
            "uname": payload.get("uname", ""),
            "mid": payload.get("mid", 0),
        }
    return {"valid": False, "reason": "invalid"}


def cmd_check(_args):
    cookie = os.environ.get("BILIBILI_COOKIE")
    result = validate_cookie(cookie)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result.get("valid") else 1
```

- [ ] **Step 5：运行测试确认通过**

Run: `pytest bilibili-video-summarizer/tests -v`
Expected: 全部 passed。

- [ ] **Step 6：提交**

```bash
git add SkillCollections/bilibili-video-summarizer
git commit -m "feat(bilibili-video-summarizer): implement cookie check subcommand"
```

---

## Task 3：视频元信息与 BV 号解析

**Files:**
- Modify: `bilibili-video-summarizer/scripts/bili_summarize.py`（新增 `parse_bvid`、`fetch_video_info`）
- Modify: `bilibili-video-summarizer/tests/test_bili_summarize.py`（新增用例）
- Create: `bilibili-video-summarizer/tests/fixtures/view_valid.json`

**Interfaces:**
- Consumes: 无
- Produces:
  - `parse_bvid(url: str) -> str`：从 `https://www.bilibili.com/video/BVxxxxx[/?p=1]` 中提取 BV 号；提取失败抛 `ValueError`。
  - `fetch_video_info(bvid: str, cookie: str, session=None) -> dict`：调用 `https://api.bilibili.com/x/web-interface/view?bvid=<bvid>`，返回 `{"title", "author", "duration_sec", "cid"}`。`cid` 供后续字幕接口使用。

- [ ] **Step 1：写 fixture**

`tests/fixtures/view_valid.json`：

```json
{
  "code": 0,
  "data": {
    "bvid": "BV1xx411c7mD",
    "title": "示例视频标题",
    "owner": {"name": "示例UP主"},
    "duration": 615,
    "cid": 987654321
  }
}
```

- [ ] **Step 2：写失败测试**

追加到 `tests/test_bili_summarize.py`：

```python
import pytest


def test_parse_bvid_standard_url():
    assert bs.parse_bvid("https://www.bilibili.com/video/BV1xx411c7mD/") == "BV1xx411c7mD"


def test_parse_bvid_with_query():
    assert bs.parse_bvid("https://www.bilibili.com/video/BV1xx411c7mD?p=1&spm_id=abc") == "BV1xx411c7mD"


def test_parse_bvid_short_url_rejected():
    with pytest.raises(ValueError):
        bs.parse_bvid("https://b23.tv/abcd")


def test_fetch_video_info():
    session = MagicMock()
    resp = MagicMock()
    resp.json.return_value = _fixture("view_valid.json")
    resp.raise_for_status = MagicMock()
    session.get.return_value = resp

    info = bs.fetch_video_info("BV1xx411c7mD", "SESSDATA=x", session=session)
    assert info == {
        "title": "示例视频标题",
        "author": "示例UP主",
        "duration_sec": 615,
        "cid": 987654321,
    }
```

- [ ] **Step 3：运行测试确认失败**

Run: `pytest bilibili-video-summarizer/tests -v`
Expected: 新增 4 个 FAIL。

- [ ] **Step 4：实现**

在 `bili_summarize.py` 中新增：

```python
import re

VIEW_URL = "https://api.bilibili.com/x/web-interface/view"
BVID_RE = re.compile(r"(BV[0-9A-Za-z]{10})")


def parse_bvid(url):
    match = BVID_RE.search(url or "")
    if not match:
        raise ValueError(f"无法从 URL 中解析 BV 号: {url}")
    return match.group(1)


def fetch_video_info(bvid, cookie, session=None):
    sess = session or requests.Session()
    headers = {
        "Cookie": cookie,
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.bilibili.com",
    }
    resp = sess.get(VIEW_URL, params={"bvid": bvid}, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"获取视频信息失败: {data.get('message')}")
    d = data["data"]
    return {
        "title": d["title"],
        "author": d["owner"]["name"],
        "duration_sec": d["duration"],
        "cid": d["cid"],
    }
```

- [ ] **Step 5：运行测试确认通过**

Run: `pytest bilibili-video-summarizer/tests -v`
Expected: 全部 passed。

- [ ] **Step 6：提交**

```bash
git add SkillCollections/bilibili-video-summarizer
git commit -m "feat(bilibili-video-summarizer): add BV parse and video info fetch"
```

---

## Task 4：字幕拉取

**Files:**
- Modify: `bilibili-video-summarizer/scripts/bili_summarize.py`（新增 `fetch_subtitle`）
- Modify: `bilibili-video-summarizer/tests/test_bili_summarize.py`（新增用例）
- Create: `bilibili-video-summarizer/tests/fixtures/player_with_subtitle.json`
- Create: `bilibili-video-summarizer/tests/fixtures/player_no_subtitle.json`
- Create: `bilibili-video-summarizer/tests/fixtures/subtitle_sample.json`

**Interfaces:**
- Consumes: `fetch_video_info` 提供的 `cid`
- Produces:
  - `fetch_subtitle(bvid: str, cid: int, cookie: str, session=None) -> list[dict] | None`：调用 `https://api.bilibili.com/x/player/v2?bvid=<bvid>&cid=<cid>` 拿字幕列表，再拉第一条字幕 JSON。返回 `[{"start": float, "text": str}, ...]`；无字幕返回 `None`。

- [ ] **Step 1：写 fixtures**

`tests/fixtures/player_with_subtitle.json`：

```json
{"code": 0, "data": {"subtitle": {"subtitles": [{"lan": "zh-CN", "subtitle_url": "//example.com/sub.json"}]}}}
```

`tests/fixtures/player_no_subtitle.json`：

```json
{"code": 0, "data": {"subtitle": {"subtitles": []}}}
```

`tests/fixtures/subtitle_sample.json`：

```json
{"body": [
  {"from": 0.5, "to": 3.2, "content": "大家好"},
  {"from": 3.2, "to": 6.8, "content": "今天我们讲解一个新话题"}
]}
```

- [ ] **Step 2：写失败测试**

追加到 `tests/test_bili_summarize.py`：

```python
def test_fetch_subtitle_present():
    session = MagicMock()

    player_resp = MagicMock()
    player_resp.json.return_value = _fixture("player_with_subtitle.json")
    player_resp.raise_for_status = MagicMock()

    sub_resp = MagicMock()
    sub_resp.json.return_value = _fixture("subtitle_sample.json")
    sub_resp.raise_for_status = MagicMock()

    session.get.side_effect = [player_resp, sub_resp]

    segments = bs.fetch_subtitle("BV1", 1, "SESSDATA=x", session=session)
    assert segments == [
        {"start": 0.5, "text": "大家好"},
        {"start": 3.2, "text": "今天我们讲解一个新话题"},
    ]


def test_fetch_subtitle_none():
    session = MagicMock()
    resp = MagicMock()
    resp.json.return_value = _fixture("player_no_subtitle.json")
    resp.raise_for_status = MagicMock()
    session.get.return_value = resp

    assert bs.fetch_subtitle("BV1", 1, "SESSDATA=x", session=session) is None
```

- [ ] **Step 3：运行测试确认失败**

Run: `pytest bilibili-video-summarizer/tests -v`
Expected: 2 个新 FAIL。

- [ ] **Step 4：实现**

在 `bili_summarize.py` 中新增：

```python
PLAYER_URL = "https://api.bilibili.com/x/player/v2"


def _bili_headers(cookie):
    return {
        "Cookie": cookie,
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.bilibili.com",
    }


def fetch_subtitle(bvid, cid, cookie, session=None):
    sess = session or requests.Session()
    headers = _bili_headers(cookie)
    resp = sess.get(PLAYER_URL, params={"bvid": bvid, "cid": cid}, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    subs = (((data.get("data") or {}).get("subtitle") or {}).get("subtitles") or [])
    if not subs:
        return None
    url = subs[0]["subtitle_url"]
    if url.startswith("//"):
        url = "https:" + url
    sub_resp = sess.get(url, headers=headers, timeout=10)
    sub_resp.raise_for_status()
    body = sub_resp.json().get("body", [])
    return [{"start": float(item["from"]), "text": item["content"]} for item in body]
```

（同时将 Task 3 中的 `headers = {...}` 替换为调用 `_bili_headers(cookie)`，保持一致；此处允许一并做小重构。）

- [ ] **Step 5：运行测试确认通过**

Run: `pytest bilibili-video-summarizer/tests -v`
Expected: 全部 passed。

- [ ] **Step 6：提交**

```bash
git add SkillCollections/bilibili-video-summarizer
git commit -m "feat(bilibili-video-summarizer): fetch bilibili CC subtitles"
```

---

## Task 5：视频下载与关键帧抽取

**Files:**
- Modify: `bilibili-video-summarizer/scripts/bili_summarize.py`（新增 `download_video`、`extract_key_frames`）
- Modify: `bilibili-video-summarizer/tests/test_bili_summarize.py`（新增用例，使用 monkeypatch mock 掉外部命令）

**Interfaces:**
- Consumes: BV 号、cookie、workdir 路径
- Produces:
  - `download_video(url: str, workdir: Path, cookie: str, runner=subprocess.run) -> Path`：用 `yt-dlp` 下载至 `workdir/source.mp4`，返回该路径。`runner` 参数为可注入的执行器，方便测试。
  - `extract_key_frames(video: Path, frames_dir: Path, duration_sec: int, runner=subprocess.run) -> list[dict]`：先做场景检测抽帧，若产物少于 3 张则清空并降级为均匀抽帧（8~12 张之间：`min(12, max(8, duration_sec // 60 + 1))`）。返回 `[{"time": float, "path": str}, ...]`，`path` 是相对 `frames_dir.parent` 的路径。

- [ ] **Step 1：写失败测试**

追加：

```python
def test_extract_key_frames_scene_detection(tmp_path, monkeypatch):
    frames_dir = tmp_path / "frames"
    frames_dir.mkdir()

    # 模拟场景检测抽出 5 张帧
    def fake_run(cmd, *a, **kw):
        for t in [10, 40, 90, 150, 300]:
            (frames_dir / f"frame_{t:04d}.jpg").write_bytes(b"fake")
        rv = MagicMock()
        rv.returncode = 0
        return rv

    result = bs.extract_key_frames(tmp_path / "v.mp4", frames_dir, 600, runner=fake_run)
    assert len(result) == 5
    assert result[0] == {"time": 10.0, "path": "frames/frame_0010.jpg"}


def test_extract_key_frames_fallback(tmp_path):
    frames_dir = tmp_path / "frames"
    frames_dir.mkdir()

    calls = {"n": 0}

    def fake_run(cmd, *a, **kw):
        calls["n"] += 1
        # 第 1 次：场景检测只出 1 张 → 触发降级
        # 第 2 次：均匀抽帧写 8 张
        if calls["n"] == 1:
            (frames_dir / "frame_0005.jpg").write_bytes(b"x")
        else:
            for i in range(8):
                (frames_dir / f"frame_{i*60:04d}.jpg").write_bytes(b"x")
        rv = MagicMock(); rv.returncode = 0
        return rv

    result = bs.extract_key_frames(tmp_path / "v.mp4", frames_dir, 480, runner=fake_run)
    assert len(result) == 8
    assert calls["n"] == 2
```

- [ ] **Step 2：运行测试确认失败**

Run: `pytest bilibili-video-summarizer/tests -v -k extract_key_frames`
Expected: 2 FAIL。

- [ ] **Step 3：实现**

在 `bili_summarize.py` 中新增：

```python
import shutil
import subprocess
from pathlib import Path

SCENE_THRESHOLD = 0.4
MAX_FRAMES = 15
FALLBACK_MIN_FRAMES = 3


def download_video(url, workdir, cookie, runner=subprocess.run):
    if not shutil.which("yt-dlp"):
        raise RuntimeError("未检测到 yt-dlp，请先安装：pip install yt-dlp")
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    output = workdir / "source.mp4"
    cmd = [
        "yt-dlp",
        "--add-header", f"Cookie:{cookie}",
        "-f", "bv*+ba/b",
        "--merge-output-format", "mp4",
        "-o", str(output),
        url,
    ]
    result = runner(cmd, check=False)
    if result.returncode != 0:
        raise RuntimeError("yt-dlp 下载失败")
    return output


def _list_frames(frames_dir):
    items = []
    for p in sorted(frames_dir.glob("frame_*.jpg")):
        try:
            sec = int(p.stem.split("_")[1])
        except (IndexError, ValueError):
            continue
        rel = f"{frames_dir.name}/{p.name}"
        items.append({"time": float(sec), "path": rel})
    return items


def extract_key_frames(video, frames_dir, duration_sec, runner=subprocess.run):
    if not shutil.which("ffmpeg"):
        raise RuntimeError("未检测到 ffmpeg，请先安装")
    frames_dir = Path(frames_dir)
    frames_dir.mkdir(parents=True, exist_ok=True)

    # 场景检测
    scene_cmd = [
        "ffmpeg", "-y", "-i", str(video),
        "-vf", f"select='gt(scene,{SCENE_THRESHOLD})',showinfo",
        "-vsync", "vfr",
        "-frame_pts", "1",
        "-frames:v", str(MAX_FRAMES),
        str(frames_dir / "frame_%04d.jpg"),
    ]
    runner(scene_cmd, check=False)
    frames = _list_frames(frames_dir)

    if len(frames) >= FALLBACK_MIN_FRAMES:
        return frames[:MAX_FRAMES]

    # 降级：清空后均匀抽帧
    for p in frames_dir.glob("frame_*.jpg"):
        p.unlink()
    target = min(12, max(8, duration_sec // 60 + 1))
    interval = max(1, duration_sec // target)
    for i in range(target):
        t = i * interval
        out = frames_dir / f"frame_{t:04d}.jpg"
        runner([
            "ffmpeg", "-y", "-ss", str(t), "-i", str(video),
            "-frames:v", "1", str(out),
        ], check=False)
    return _list_frames(frames_dir)
```

因测试里没有真实 ffmpeg 产物、由 `fake_run` 写入 `frame_XXXX.jpg`，`_list_frames` 会正确扫描。

- [ ] **Step 4：运行测试确认通过**

Run: `pytest bilibili-video-summarizer/tests -v`
Expected: 全部 passed。

- [ ] **Step 5：提交**

```bash
git add SkillCollections/bilibili-video-summarizer
git commit -m "feat(bilibili-video-summarizer): download video and extract key frames"
```

---

## Task 6：Whisper 降级转录

**Files:**
- Modify: `bilibili-video-summarizer/scripts/bili_summarize.py`（新增 `transcribe_with_whisper`、`extract_audio`）
- Modify: `bilibili-video-summarizer/tests/test_bili_summarize.py`

**Interfaces:**
- Consumes: 视频文件路径
- Produces:
  - `extract_audio(video: Path, out_path: Path, runner=subprocess.run) -> Path`：用 ffmpeg 抽 16k 单声道 wav。
  - `transcribe_with_whisper(audio: Path, model_name: str = "base", whisper_loader=None) -> list[dict]`：加载 whisper 模型并转录，返回与字幕接口一致的 `[{"start", "text"}]`。`whisper_loader` 可注入，测试时避免真加载模型。

- [ ] **Step 1：写失败测试**

追加：

```python
def test_extract_audio(tmp_path):
    calls = []

    def fake_run(cmd, *a, **kw):
        calls.append(cmd)
        rv = MagicMock(); rv.returncode = 0; return rv

    audio = tmp_path / "a.wav"
    result = bs.extract_audio(tmp_path / "v.mp4", audio, runner=fake_run)
    assert result == audio
    assert "-ar" in calls[0] and "16000" in calls[0]


def test_transcribe_with_whisper(tmp_path):
    fake_model = MagicMock()
    fake_model.transcribe.return_value = {
        "segments": [
            {"start": 1.2, "text": " 你好"},
            {"start": 3.4, "text": " 世界"},
        ]
    }
    fake_loader = MagicMock(return_value=fake_model)

    result = bs.transcribe_with_whisper(tmp_path / "a.wav", "base", whisper_loader=fake_loader)
    assert result == [
        {"start": 1.2, "text": "你好"},
        {"start": 3.4, "text": "世界"},
    ]
    fake_loader.assert_called_once_with("base")
```

- [ ] **Step 2：运行测试确认失败**

Run: `pytest bilibili-video-summarizer/tests -v -k "audio or whisper"`
Expected: FAIL。

- [ ] **Step 3：实现**

在 `bili_summarize.py` 中新增：

```python
def extract_audio(video, out_path, runner=subprocess.run):
    if not shutil.which("ffmpeg"):
        raise RuntimeError("未检测到 ffmpeg")
    cmd = [
        "ffmpeg", "-y", "-i", str(video),
        "-vn", "-ac", "1", "-ar", "16000", "-f", "wav", str(out_path),
    ]
    result = runner(cmd, check=False)
    if result.returncode != 0:
        raise RuntimeError("音频抽取失败")
    return Path(out_path)


def transcribe_with_whisper(audio, model_name="base", whisper_loader=None):
    if whisper_loader is None:
        try:
            import whisper  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "未安装 openai-whisper，且视频无字幕。请 pip install openai-whisper 或改用有字幕的视频。"
            ) from exc
        whisper_loader = whisper.load_model

    model = whisper_loader(model_name)
    data = model.transcribe(str(audio))
    return [
        {"start": float(seg["start"]), "text": seg["text"].strip()}
        for seg in data.get("segments", [])
    ]
```

- [ ] **Step 4：运行测试确认通过**

Run: `pytest bilibili-video-summarizer/tests -v`
Expected: 全部 passed。

- [ ] **Step 5：提交**

```bash
git add SkillCollections/bilibili-video-summarizer
git commit -m "feat(bilibili-video-summarizer): whisper fallback transcription"
```

---

## Task 7：`fetch` 子命令编排

**Files:**
- Modify: `bilibili-video-summarizer/scripts/bili_summarize.py`（实现 `cmd_fetch`、`sanitize_dirname`）
- Modify: `bilibili-video-summarizer/tests/test_bili_summarize.py`（新增一体化测试，全部依赖用 monkeypatch）

**Interfaces:**
- Consumes: 前 6 个 Task 的函数
- Produces:
  - `sanitize_dirname(title: str) -> str`：把标题里 `/\:*?"<>|` 替换为 `_`，去除首尾空格。
  - `cmd_fetch(args) -> int`：串起 cookie→info→subtitle→(可能)download+whisper→抽帧，写 stdout JSON，退出码 0。若 cookie 不合法退出码 2 并输出 `{"error": "cookie invalid"}`。视频文件在成功后按 `--keep-video` 决定是否删除。

- [ ] **Step 1：写失败测试**

追加：

```python
def test_sanitize_dirname():
    assert bs.sanitize_dirname("A/B:C?<D>|E") == "A_B_C__D__E"
    assert bs.sanitize_dirname("  标题  ") == "标题"


def test_cmd_fetch_end_to_end(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("BILIBILI_COOKIE", "SESSDATA=abc; bili_jct=x")

    monkeypatch.setattr(bs, "validate_cookie", lambda c, session=None: {"valid": True, "uname": "u", "mid": 1})
    monkeypatch.setattr(bs, "parse_bvid", lambda url: "BV1xx411c7mD")
    monkeypatch.setattr(bs, "fetch_video_info", lambda bvid, cookie, session=None: {
        "title": "示例标题", "author": "UP", "duration_sec": 300, "cid": 1,
    })
    monkeypatch.setattr(bs, "fetch_subtitle", lambda bvid, cid, cookie, session=None: [
        {"start": 0.0, "text": "开场"}, {"start": 10.0, "text": "内容"},
    ])
    def fake_download(url, workdir, cookie, **kw):
        (Path(workdir) / "source.mp4").write_bytes(b"x")
        return Path(workdir) / "source.mp4"
    monkeypatch.setattr(bs, "download_video", fake_download)
    def fake_frames(video, frames_dir, duration_sec, **kw):
        Path(frames_dir).mkdir(parents=True, exist_ok=True)
        return [{"time": 5.0, "path": "frames/frame_0005.jpg"}]
    monkeypatch.setattr(bs, "extract_key_frames", fake_frames)

    ns = argparse.Namespace(
        url="https://www.bilibili.com/video/BV1xx411c7mD",
        outdir=str(tmp_path), keep_video=False,
    )
    code = bs.cmd_fetch(ns)
    assert code == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["title"] == "示例标题"
    assert payload["subtitle_source"] == "bilibili_cc"
    assert payload["segments"][0] == {"start": 0.0, "text": "开场"}
    assert payload["frames"] == [{"time": 5.0, "path": "frames/frame_0005.jpg"}]
    assert Path(payload["workdir"]).name == "示例标题"
    assert not (Path(payload["workdir"]) / "source.mp4").exists()


def test_cmd_fetch_falls_back_to_whisper(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("BILIBILI_COOKIE", "SESSDATA=abc")
    monkeypatch.setattr(bs, "validate_cookie", lambda c, session=None: {"valid": True, "uname": "u", "mid": 1})
    monkeypatch.setattr(bs, "parse_bvid", lambda url: "BV1")
    monkeypatch.setattr(bs, "fetch_video_info", lambda *a, **kw: {"title": "T", "author": "U", "duration_sec": 60, "cid": 1})
    monkeypatch.setattr(bs, "fetch_subtitle", lambda *a, **kw: None)  # 无字幕
    monkeypatch.setattr(bs, "download_video", lambda url, workdir, cookie, **kw: Path(workdir) / "source.mp4")
    monkeypatch.setattr(bs, "extract_audio", lambda video, out, **kw: out)
    monkeypatch.setattr(bs, "transcribe_with_whisper", lambda audio, model_name="base", whisper_loader=None: [{"start": 0.0, "text": "hi"}])
    monkeypatch.setattr(bs, "extract_key_frames", lambda *a, **kw: [])

    ns = argparse.Namespace(url="x", outdir=str(tmp_path), keep_video=True)
    code = bs.cmd_fetch(ns)
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["subtitle_source"] == "whisper"
    assert payload["segments"] == [{"start": 0.0, "text": "hi"}]


def test_cmd_fetch_rejects_invalid_cookie(monkeypatch, tmp_path, capsys):
    monkeypatch.delenv("BILIBILI_COOKIE", raising=False)
    ns = argparse.Namespace(url="x", outdir=str(tmp_path), keep_video=False)
    code = bs.cmd_fetch(ns)
    assert code == 2
    assert "cookie" in capsys.readouterr().out.lower()


import argparse  # 若文件顶部尚未导入
```

- [ ] **Step 2：运行测试确认失败**

Run: `pytest bilibili-video-summarizer/tests -v -k fetch`
Expected: FAIL（`sanitize_dirname` 不存在 / `cmd_fetch` 未实现）。

- [ ] **Step 3：实现**

在 `bili_summarize.py` 中新增/替换：

```python
INVALID_CHARS = '/\\:*?"<>|'


def sanitize_dirname(title):
    out = []
    for ch in title:
        out.append("_" if ch in INVALID_CHARS else ch)
    return "".join(out).strip()


def cmd_fetch(args):
    cookie = os.environ.get("BILIBILI_COOKIE")
    cookie_check = validate_cookie(cookie)
    if not cookie_check.get("valid"):
        print(json.dumps({"error": "cookie invalid", "detail": cookie_check}, ensure_ascii=False))
        return 2

    try:
        bvid = parse_bvid(args.url)
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 3

    info = fetch_video_info(bvid, cookie)
    workdir = Path(args.outdir) / sanitize_dirname(info["title"])
    workdir.mkdir(parents=True, exist_ok=True)
    frames_dir = workdir / "frames"

    segments = fetch_subtitle(bvid, info["cid"], cookie)
    subtitle_source = "bilibili_cc" if segments else "whisper"

    video_path = download_video(args.url, workdir, cookie)

    if segments is None:
        audio = extract_audio(video_path, workdir / "audio.wav")
        segments = transcribe_with_whisper(audio)
        try:
            Path(audio).unlink()
        except OSError:
            pass

    frames = extract_key_frames(video_path, frames_dir, info["duration_sec"])

    if not args.keep_video:
        try:
            Path(video_path).unlink()
        except OSError:
            pass

    payload = {
        "title": info["title"],
        "author": info["author"],
        "bvid": bvid,
        "duration_sec": info["duration_sec"],
        "workdir": str(workdir),
        "subtitle_source": subtitle_source,
        "segments": segments,
        "frames": frames,
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0
```

- [ ] **Step 4：运行测试确认通过**

Run: `pytest bilibili-video-summarizer/tests -v`
Expected: 全部 passed。

- [ ] **Step 5：提交**

```bash
git add SkillCollections/bilibili-video-summarizer
git commit -m "feat(bilibili-video-summarizer): implement fetch subcommand pipeline"
```

---

## Task 8：SKILL.md 编排指引与 references 排障文档

**Files:**
- Modify: `bilibili-video-summarizer/SKILL.md`（写完整流程）
- Create: `bilibili-video-summarizer/references/troubleshooting.md`

**Interfaces:**
- Consumes: `bili_summarize.py` 的 `check` 与 `fetch` 子命令契约
- Produces: 完整可用的 skill 说明。

- [ ] **Step 1：写 SKILL.md**

内容（完整覆写现有占位文件）：

````markdown
---
name: bilibili-video-summarizer
description: "输入 B 站视频链接，自动校验 BILIBILI_COOKIE 有效性、拉取字幕(无则本地 Whisper 转录)、抽取关键帧，生成带 Mermaid 图与截图的中文 Markdown 学习笔记。触发词：B 站视频总结、bilibili 学习笔记、视频知识点提炼。"
version: 1.0.0
---

# bilibili-video-summarizer

把一条 B 站视频转成一篇「面向学习」的 Markdown 笔记：全局知识结构图 + 分章节讲解 + 关键帧截图。

## 前置

- Python 3.9+，`pip install -r scripts/requirements.txt`
- 系统安装 `ffmpeg`
- 环境变量 `BILIBILI_COOKIE`：从浏览器登录 bilibili.com 后复制完整 Cookie 字符串（至少包含 `SESSDATA`）

## 执行流程

在**本 skill 目录**下执行脚本。

### 第 1 步：校验 cookie

```bash
python3 scripts/bili_summarize.py check
```

- 输出示例（合法）：`{"valid": true, "uname": "xxx", "mid": 123}`
- 输出示例（失效）：`{"valid": false, "reason": "invalid"}`
- 分支处理：
  - `not_set` → 提示用户设置 `BILIBILI_COOKIE` 并说明如何从浏览器复制，暂停等待。
  - `invalid` → 明确告知 cookie 已失效/非法，请重新提供，暂停等待。
  - `valid` → 显示登录用户名（`uname`），进入下一步。

### 第 2 步：向用户索取视频链接

明确请用户粘贴 B 站视频链接（`https://www.bilibili.com/video/BVxxx...`）。

### 第 3 步：取数据

```bash
python3 scripts/bili_summarize.py fetch --url "<视频链接>" --outdir "$(pwd)"
```

- 若字幕来源为 `whisper`，首次转录会较慢（可能几分钟），提前告知用户。
- 解析 stdout 的 JSON 到内存备用。

### 第 4 步：撰写学习笔记

在 `<workdir>/学习笔记.md` 写入以下结构（**必须有图**）：

1. 标题 + 元信息（视频标题、UP主、时长、原链接、字幕来源）
2. 一句话概述
3. **知识结构图（Mermaid）**——`graph TD` 或 `mindmap`，覆盖全视频知识点
4. 分章节详解：
   - 每章一个小标题（按内容逻辑分，不是机械按时间）
   - 要点讲解（基于 segments 提炼，不逐字复制）
   - 插入语义相关的关键帧截图：`![图注](frames/frame_XXXX.jpg)`，必须写图注
   - 流程/关系/对比处补 Mermaid 局部图
5. 重点总结

### 硬性要求

- 至少 1 张全局 Mermaid 结构图 + 若干关键帧截图
- 每张截图必须有语义图注，插入相关章节
- 中文撰写，术语保留英文
- 完成后向用户汇报：`学习笔记.md` 与 `frames/` 的绝对路径

## 常见问题

见 `references/troubleshooting.md`。
````

- [ ] **Step 2：写 troubleshooting.md**

`bilibili-video-summarizer/references/troubleshooting.md`：

```markdown
# 排障

## Cookie 相关

- `not_set`：环境变量 `BILIBILI_COOKIE` 未设置。从浏览器 DevTools > Application > Cookies 复制 `bilibili.com` 域下的完整 cookie 字符串（至少含 `SESSDATA`）。
- `invalid`：cookie 已失效或格式不对。重新登录 bilibili.com 复制新 cookie。

## yt-dlp / ffmpeg 缺失

- `未检测到 yt-dlp`：`pip install yt-dlp`
- `未检测到 ffmpeg`：macOS `brew install ffmpeg`

## 视频无字幕

自动降级为 Whisper 本地转录。若报 `未安装 openai-whisper`：
```bash
pip install openai-whisper
```
首次运行会下载模型（几百 MB）。

## 关键帧过少

场景检测抽到 <3 张时，脚本自动降级为均匀抽帧（8~12 张）。若均匀抽帧仍失败，检查视频文件是否成功下载。

## 链接解析失败

只接受包含 `BVxxxxxxxxxx` 的完整链接。若你有短链（如 `b23.tv/xxx`），先在浏览器打开跳转到完整链接，再复制回来。
```

- [ ] **Step 3：提交**

```bash
git add SkillCollections/bilibili-video-summarizer
git commit -m "docs(bilibili-video-summarizer): SKILL.md workflow and troubleshooting"
```

---

## Task 9：（已跳过）同步 SkillCollections 索引

> **已跳过**：技能改为写入 AiFlowScript 仓库顶层 `bilibili-video-summarizer/`，
> 不进入独立的 SkillCollections 仓库，因此无需更新其索引。保留本节仅作记录。

---

## Task 10：手工冒烟验证

**Files:**
- 无代码改动。

**Interfaces:**
- Consumes: 前 9 个 Task 的成果
- Produces: 一份成功生成的 `学习笔记.md`（不入库）作为验证。

- [ ] **Step 1：安装依赖**

```bash
cd SkillCollections/bilibili-video-summarizer
pip install -r scripts/requirements.txt
```

- [ ] **Step 2：设置 cookie 并跑 check**

```bash
export BILIBILI_COOKIE="<从浏览器复制的完整 cookie>"
python3 scripts/bili_summarize.py check
```

Expected: 输出含 `"valid": true` 与你的用户名。

- [ ] **Step 3：跑 fetch**

选一条有字幕的短视频（<10 分钟），执行：

```bash
python3 scripts/bili_summarize.py fetch --url "<你选的视频>" --outdir /tmp/bili-test
```

Expected: stdout 输出结构化 JSON；`/tmp/bili-test/<标题>/frames/` 存在若干 jpg。

- [ ] **Step 4：确认 SKILL.md 描述能触发**

在 Coco 里以自然语言触发（例如："帮我总结一下这个 B 站视频"），观察 skill 是否被建议使用；观察最终能否得到含 Mermaid 图与截图的 `学习笔记.md`。

- [ ] **Step 5：清理**

```bash
rm -rf /tmp/bili-test
```

---

## 自检

- **spec 覆盖**：
  - Cookie 环境变量 + 校验 → Task 2、Task 7（cookie 不合法早退）、SKILL.md 第 1 步。
  - 索取视频链接 → SKILL.md 第 2 步。
  - 字幕拉取 + 无字幕降级 Whisper → Task 4、Task 6、Task 7。
  - 关键帧抽取 + 场景检测/均匀降级 → Task 5。
  - Markdown 输出 + Mermaid + 截图 → Task 8 的 SKILL.md 撰写指引。
  - 视频标题命名工作目录 → Task 7 的 `sanitize_dirname`。
  - 索引同步 → Task 9。
- **占位符扫描**：无 TBD/TODO；所有测试代码、实现代码、命令均给出具体内容。
- **类型/命名一致性**：`segments = [{"start", "text"}]`、`frames = [{"time", "path"}]`、`workdir`、`subtitle_source`、`BILIBILI_COOKIE`、`SCENE_THRESHOLD` 等在 Task 3~7 与 Task 8 SKILL.md 中命名一致。
- **命令一致性**：`bili_summarize.py check` 与 `fetch --url --outdir [--keep-video]` 在 Task 1、2、7、8、10 完全一致。
