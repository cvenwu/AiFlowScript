#!/usr/bin/env python3
"""按 11 类规则对 starred repos 自动分类。一个 repo 可归多个列表。"""
import json, re, sys
from collections import defaultdict, OrderedDict

WS = "/Users/bytedance/Documents/workspace/personal_workspace/github_workspace"
SRC = f"{WS}/.github-cleanup/starred-meta.jsonl"

# 11 类：每类 = (关键词正则, 命中的语言集合)。关键词匹配 name+topics+description（小写）
RULES = OrderedDict([
    ("AI / Agent", (r"agent|langchain|langgraph|autogpt|crewai|multi-agent|agentic|\bdify\b|\bcoze\b|\bmcp\b|\brag\b|copilot|aigc|stable-diffusion|comfyui|text-to-image|diffusion|prompt-eng|prompt engineer", set())),
    ("LLM 基础", (r"\bllm\b|large-language|large language|transformer|\bgpt\b|\bbert\b|fine-?tun|pre-?train|deep-?learning|machine learning|machine-learning|neural network|nlp\b|大模型|深度学习|机器学习", {"Jupyter Notebook"})),
    ("Go / 后端", (r"golang|\bgin\b|beego|microservice|micro-service|\bgrpc\b|\bbackend\b|kitex|hertz|服务端|后端", {"Go"})),
    ("分布式 / 系统设计", (r"distributed|system-design|system design|systemdesign|consensus|\braft\b|paxos|\bkafka\b|\betcd\b|database|storage|\bmysql\b|postgres|\bredis\b|\btidb\b|clickhouse|middleware|high-availability|scalab|分布式|数据库", set())),
    ("算法", (r"algorithm|leetcode|data-structure|data structure|\bacm\b|competitive-programming|刷题|算法|数据结构", set())),
    ("面试 / 八股", (r"interview|面试|八股|resume|简历|\boffer\b|求职|校招|social-recruit", set())),
    ("C / C++", (r"\bc\+\+|\bcpp\b|clang|assembly|\bkernel\b|操作系统", {"C++", "C", "Assembly"})),
    ("Rust", (r"\brust\b|\bcargo\b|\btokio\b", {"Rust"})),
    ("云原生 / DevOps", (r"kubernetes|\bk8s\b|docker|container|devops|prometheus|grafana|\bhelm\b|istio|service-mesh|ci-cd|ci/cd|cloud-native|云原生|monitoring|\blinux\b|\bnginx\b", set())),
    ("工具 / 效率", (r"\bcli\b|\btool\b|toolkit|awesome-|productivity|vscode|neovim|dotfiles|frontend|\breact\b|\bvue\b|template|\breadme\b|\biot\b|efficiency|utility|插件|效率", {"Vue", "CSS"})),
    ("软技能 / 职业", (r"soft-skill|soft skill|\bcareer\b|\bbook\b|books\b|设计模式|design-pattern|design pattern|guide|handbook|roadmap|tutorial|职业|职场", set())),
])

def classify(d):
    hay = f"{d['full_name']} {' '.join(d.get('topics',[]))} {d.get('description','')}".lower()
    lang = d.get("language") or ""
    hits = []
    for cat, (pat, langs) in RULES.items():
        if re.search(pat, hay) or (lang in langs and langs):
            hits.append(cat)
    return hits

rows = []
by_cat = defaultdict(list)
uncat = []
for line in open(SRC):
    d = json.loads(line)
    hits = classify(d)
    if hits:
        for c in hits:
            by_cat[c].append(d["full_name"])
    else:
        uncat.append(d["full_name"])
    rows.append((d["full_name"], ";".join(hits) if hits else "UNCATEGORIZED"))

# 输出映射 CSV
with open(f"{WS}/.github-cleanup/star-map.csv", "w") as f:
    f.write("repo,lists\n")
    for name, cats in rows:
        f.write(f"{name},{cats}\n")

# 统计
print("=== 每类命中数（一个 repo 可多类）===")
for c in RULES:
    print(f"{len(by_cat[c]):4d}  {c}")
print(f"{len(uncat):4d}  UNCATEGORIZED")
print(f"\n总 star = {len(rows)}，已归类 = {len(rows)-len(uncat)}，未命中 = {len(uncat)}")
