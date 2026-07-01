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
