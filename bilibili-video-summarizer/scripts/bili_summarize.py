#!/usr/bin/env python3
"""bilibili-video-summarizer 主脚本。

提供两个子命令：
    check              校验 BILIBILI_COOKIE 是否合法
    fetch --url --outdir   拉取视频信息、字幕/转录、关键帧并输出 JSON
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import requests


NAV_URL = "https://api.bilibili.com/x/web-interface/nav"
VIEW_URL = "https://api.bilibili.com/x/web-interface/view"
PLAYER_URL = "https://api.bilibili.com/x/player/v2"
BVID_RE = re.compile(r"(BV[0-9A-Za-z]{10})")

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

    # 降级：清空后均匀抽帧（单次 ffmpeg 调用，用 fps 滤镜）
    for p in frames_dir.glob("frame_*.jpg"):
        p.unlink()
    target = min(12, max(8, duration_sec // 60 + 1))
    fps_value = target / duration_sec if duration_sec else 0.1
    fallback_cmd = [
        "ffmpeg", "-y", "-i", str(video),
        "-vf", f"fps={fps_value}",
        "-frames:v", str(target),
        str(frames_dir / "frame_%04d.jpg"),
    ]
    runner(fallback_cmd, check=False)
    return _list_frames(frames_dir)


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


def parse_bvid(url):
    match = BVID_RE.search(url or "")
    if not match:
        raise ValueError(f"无法从 URL 中解析 BV 号: {url}")
    return match.group(1)


def fetch_video_info(bvid, cookie, session=None):
    sess = session or requests.Session()
    headers = _bili_headers(cookie)
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


def validate_cookie(cookie, session=None):
    if not cookie:
        return {"valid": False, "reason": "not_set"}
    if "SESSDATA=" not in cookie:
        return {"valid": False, "reason": "invalid"}

    sess = session or requests.Session()
    headers = _bili_headers(cookie)
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


def cmd_check(_args: argparse.Namespace) -> int:
    cookie = os.environ.get("BILIBILI_COOKIE")
    result = validate_cookie(cookie)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result.get("valid") else 1


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
