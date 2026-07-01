# Bilibili 视频学习笔记生成 Skill 设计文档

- 日期：2026-07-01
- Skill 名：`bilibili-video-summarizer`
- 目标位置：`SkillCollections/bilibili-video-summarizer/`

## 1. 目标与背景

用户希望有一个 skill，能够：

1. 通过环境变量存储 B 站 cookie，每次使用前校验 cookie 是否合法/有效；若非法、失效或未设置，则提示用户重新提供。
2. cookie 合法后，请用户输入 B 站视频链接。
3. 分析该视频主要讲解的内容，将其总结为一篇面向"学习"的 Markdown 文档。
4. Markdown 文档中必须有图（关键帧截图 + Mermaid 知识图表）。

## 2. 整体架构与职责边界

### 目录结构

```
bilibili-video-summarizer/
├── SKILL.md                      # 编排流程 + Markdown 撰写指引 + Mermaid 规范
├── scripts/
│   ├── bili_summarize.py         # 主脚本：取数流水线，输出 JSON
│   └── requirements.txt          # yt-dlp 等依赖
└── references/
    └── troubleshooting.md        # cookie 失效、无字幕、抽帧失败等排障
```

### 职责边界

- **脚本层（确定性取数，低自由度）**：cookie 校验、视频元信息获取、字幕拉取/降级转录、关键帧抽取。只输出数据，不做内容理解。
- **Agent 层（内容理解，高自由度）**：读取脚本输出的 JSON，理解视频讲解内容，撰写 Markdown，设计 Mermaid 图，插入截图并配图注。

设计原则遵循 skill-creator：脆弱/需精确语法的操作用脚本封装，内容理解与创作留给 Agent 临场发挥。

## 3. 主脚本输入输出契约

`bili_summarize.py` 提供两个子命令。

### 子命令 1：`check` —— 校验 cookie

```bash
python bili_summarize.py check
```

- 读环境变量 `BILIBILI_COOKIE`，调用 B 站导航接口 `https://api.bilibili.com/x/web-interface/nav`（带 cookie）。
- 输出 JSON：
  - 合法：`{"valid": true, "uname": "xxx", "mid": 123}`
  - 非法：`{"valid": false, "reason": "not_set | invalid | expired"}`
- 退出码：合法 0，非法/失效非 0。

### 子命令 2：`fetch` —— 取全量数据

```bash
python bili_summarize.py fetch --url "<视频链接>" --outdir "<输出根目录>"
```

流程：解析 BV 号 → 拉元信息（标题/UP主/简介/分P）→ 拉字幕（无则降级 Whisper）→ 抽关键帧 → 落盘。

输出 JSON（stdout）：

```json
{
  "title": "视频标题",
  "author": "UP主",
  "bvid": "BVxxx",
  "duration_sec": 615,
  "workdir": "<输出根目录>/<清洗后的标题>",
  "subtitle_source": "bilibili_cc | whisper",
  "segments": [
    {"start": 12.5, "text": "这段讲了..."}
  ],
  "frames": [
    {"time": 30.0, "path": "frames/frame_0030.jpg"}
  ]
}
```

要点：
- `segments` 带时间轴，便于将截图与讲解文字对齐。
- `frames.path` 为相对 `workdir` 的相对路径，便于 Markdown 引用。
- 若 `check` 未通过，`fetch` 直接拒绝执行并提示重新提供 cookie。

## 4. 关键帧抽取策略

目标：截图要有代表性、能对应讲解内容，而非均匀乱截。

### 默认策略：场景切换检测

- 使用 ffmpeg 场景检测：`select='gt(scene,0.4)'`，在画面明显切换处抽帧（PPT 翻页、镜头切换）。这类切换点通常对应知识点切换处。
- 设上限（默认最多 15 张），避免动画类视频截图爆炸。

### 降级策略：定时抽帧

- 若场景检测得到的帧过少（默认 < 3 张，如纯口播/固定画面视频），降级为按时间均匀抽帧（总数控制在 8～12 张）。

### 视频获取与产物

- 用 yt-dlp（带 cookie）下载视频；抽完帧后默认删除源视频文件，只保留截图。提供 `--keep-video` 开关，默认不保留。
- 截图存 `workdir/frames/`，命名含时间戳（如 `frame_0030.jpg` 表示第 30 秒）。
- 每帧在 JSON 中带 `time`，Agent 据此把截图插入对应讲解段落旁。

### 可调参数（脚本内常量）

- 场景阈值：0.4
- 最多帧数：15
- 降级阈值：3

## 5. Markdown 学习文档输出规范

Agent 拿到 JSON 后，撰写 `<workdir>/学习笔记.md`，面向"学习"目的（不是逐字转录）。

### 文档结构

1. **标题 + 元信息**：视频标题、UP主、时长、原链接、字幕来源（B站字幕/Whisper）。
2. **一句话概述**：视频核心讲了什么。
3. **知识结构图（Mermaid）**：用 `graph TD` 或 `mindmap` 把知识点/流程画成一张全局结构图，放在开头建立整体认知。
4. **分章节详解**：按内容逻辑（非机械按时间）分章。每章包含：
   - 小标题
   - 要点讲解（基于 segments 提炼，非逐字复制）
   - 插入对应关键帧截图：`![说明](frames/frame_0030.jpg)`，按 `time` 匹配到相关章节，并配图注说明该图内容。
   - 必要处补充局部 Mermaid 流程图。
5. **重点总结 / 关键结论**：便于回顾。

### 图片使用硬性要求

- 文档必须有图：至少 1 张全局 Mermaid 结构图 + 若干关键帧截图。
- 每张截图必须有图注，且插在语义相关章节，不允许把截图全堆在文末。
- 若某章节讲的是流程/关系/对比，优先补 Mermaid 图强化理解。

### 语言

- 中文撰写，术语保留英文原词。

## 6. 错误处理与交互流程

### 完整交互流程（SKILL.md 编排）

1. 用户触发 skill → Agent 先跑 `check`。
2. cookie 分支：
   - 未设置 → 提示用户设置环境变量 `BILIBILI_COOKIE` 并说明获取方式，暂停等待。
   - 失效/非法（`expired`/`invalid`）→ 明确告知 cookie 已失效，请重新提供，暂停等待。
   - 合法 → 显示登录用户名，进入下一步。
3. cookie 合法后，请用户输入 B 站视频链接。
4. 跑 `fetch` 取数 → 读 JSON → 撰写 `学习笔记.md`。
5. 完成后告知用户输出路径。

### 关键错误处理

| 场景 | 处理 |
|---|---|
| cookie 未设置/失效 | 停止，提示重新提供（核心需求） |
| 链接非法/解析不出 BV 号 | 提示用户重新给有效链接 |
| 无 B 站字幕 | 自动降级 Whisper 转录（首次提示可能较慢） |
| yt-dlp/ffmpeg 未安装 | 脚本检测并给出安装提示 |
| 抽帧过少 | 自动降级为定时抽帧 |
| Whisper 也不可用 | 告知无法转录，终止并说明原因 |

### 收尾

- 按仓库 CLAUDE.md 规则，新增 skill 后同步更新 `SkillCollections/README.md` 索引（技能总数 116→117，追加目录行）。

## 7. 依赖

- `yt-dlp`（下载视频/字幕，支持 cookie）
- `ffmpeg`（关键帧抽取、音频提取）
- Whisper（无字幕时本地语音转录；具体实现方式在 plan 阶段确定）
- Python 标准库 + `requests`（调用 B 站接口）
