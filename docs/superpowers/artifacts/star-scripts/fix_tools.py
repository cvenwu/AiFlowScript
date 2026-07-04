#!/usr/bin/env python3
"""补勾"工具 / 效率"类（菜单最后一项，需 scrollintoview 才能点中）。"""
import subprocess, sys, time, re

WS = "/Users/bytedance/Documents/workspace/personal_workspace/github_workspace"
REPOS = [l.strip() for l in open(f"{WS}/.github-cleanup/tools-repos.txt") if l.strip()]
LOG = open(f"{WS}/.github-cleanup/tools-fix.log", "a")
TARGET = "工具 / 效率"

def ab(*a, timeout=40):
    try:
        r = subprocess.run(["agent-browser", *a], capture_output=True, text=True, timeout=timeout)
        return r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT"

start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
count = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
for i, repo in enumerate(REPOS[start:start+count], start=start):
    ab("open", f"https://github.com/{repo}"); time.sleep(2.2)
    snap = ab("snapshot")
    addref = None
    for line in snap.splitlines():
        if "Add this repository to a list" in line:
            mm = re.search(r'ref=(e\d+)', line) or re.search(r'(e\d+)', line)
            if mm: addref = mm.group(1)
            break
    if not addref:
        print(f"[{i}] {repo} NO_BTN"); LOG.write(f"{i}\t{repo}\tNO_BTN\n"); LOG.flush(); continue
    ab("click", f"@{addref}")
    time.sleep(2.2)
    msnap = ab("snapshot")
    if f'option "{TARGET}"' not in msnap:
        time.sleep(1.5); msnap = ab("snapshot")   # 菜单渲染慢，重抓一次
    # 找目标 option 的 ref + 是否已选
    ref = None; sel = False
    for line in msnap.splitlines():
        if f'option "{TARGET}"' in line:
            mm = re.search(r'e\d+', line); ref = mm.group(0) if mm else None
            sel = 'selected]' in line
            break
    if ref and not sel:
        ab("scrollintoview", f"@{ref}")
        time.sleep(0.5)
        ab("click", f"@{ref}")
        time.sleep(1.0)
        status = "checked"
    elif sel:
        status = "already"
    else:
        status = "OPT_NOT_FOUND"
    cm = re.search(r'"Close" \[ref=(e\d+)', ab("snapshot"))
    if cm: ab("click", f"@{cm.group(1)}")
    time.sleep(0.5)
    print(f"[{i}] {repo} -> {status}")
    LOG.write(f"{i}\t{repo}\t{status}\n"); LOG.flush()
LOG.close()
print("TOOLS FIX DONE")
