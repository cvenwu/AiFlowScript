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
import sys

import requests


NAV_URL = "https://api.bilibili.com/x/web-interface/nav"
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
