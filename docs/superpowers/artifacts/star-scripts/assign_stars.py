#!/usr/bin/env python3
"""按 star-map.csv 给每个 repo 勾选其命中的所有列表。
   一个 repo 打开一次页面，处理它的全部目标列表。
   用法: python3 assign_stars.py <start_index> <count>
   分批：可指定从第几个 repo 开始、处理多少个。"""
import csv, subprocess, sys, time, re

WS = "/Users/bytedance/Documents/workspace/personal_workspace/github_workspace"
CSV = f"{WS}/.github-cleanup/star-map.csv"
LOG = f"{WS}/.github-cleanup/assign-progress.log"

# CSV 分类名 -> UI 实际列表名
NAME_MAP = {
    "AI / Agent": "AI Agent",
    "Go / 后端": "Go",
    # 其余同名
}

def ab(*args, timeout=30):
    try:
        r = subprocess.run(["agent-browser", *args], capture_output=True, text=True, timeout=timeout)
        return r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT"

def snapshot():
    return ab("snapshot")

def ref_for_option(snap, label):
    # 在快照里找 option "label" 的 ref
    for line in snap.splitlines():
        if f'option "{label}"' in line:
            m = re.search(r'e\d+', line)
            if m: return m.group(0), ('[selected]' in line or 'selected]' in line)
    return None, False

def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
    rows = [r for r in csv.DictReader(open(CSV)) if r["lists"] != "UNCATEGORIZED"]
    batch = rows[start:start+count]
    logf = open(LOG, "a")
    for i, r in enumerate(batch, start=start):
        repo = r["repo"]
        cats = [NAME_MAP.get(c, c) for c in r["lists"].split(";")]
        ab("open", f"https://github.com/{repo}", timeout=40)
        time.sleep(2.2)
        snap = snapshot()
        m = re.search(r'"Add this repository to a list" \[expanded=false, ref=(e\d+)', snap)
        if not m:
            m = re.search(r'ref=(e\d+)\]?\n?\s*[^\n]*Add this repository to a list', snap)
        if not m:
            # try find by text
            addref = None
            for line in snap.splitlines():
                if "Add this repository to a list" in line:
                    mm = re.search(r'e\d+', line); addref = mm.group(0) if mm else None; break
            if not addref:
                print(f"[{i}] {repo} SKIP (no add button)"); logf.write(f"{i}\t{repo}\tNO_BTN\n"); logf.flush(); continue
        else:
            addref = m.group(1)
        ab("click", f"@{addref}")
        time.sleep(1.5)
        msnap = snapshot()
        done = []
        for cat in cats:
            ref, sel = ref_for_option(msnap, cat)
            if ref and not sel:
                ab("click", f"@{ref}")
                time.sleep(0.7)
                done.append(cat)
            elif sel:
                done.append(cat + "(already)")
        # close menu
        cm = re.search(r'"Close" \[ref=(e\d+)', snapshot())
        if cm: ab("click", f"@{cm.group(1)}")
        time.sleep(0.6)
        print(f"[{i}] {repo} -> {done}")
        logf.write(f"{i}\t{repo}\t{';'.join(done)}\n"); logf.flush()
    logf.close()
    print("BATCH DONE")

if __name__ == "__main__":
    main()
