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
- JSON 字段：`title` / `author` / `bvid` / `duration_sec` / `workdir` / `subtitle_source`（`bilibili_cc` 或 `whisper`）/ `segments`（`[{"start", "text"}]`）/ `frames`（`[{"time", "path"}]`）。
- **关于 `frames[].time`**：当字幕/画面走场景检测抽帧时，`time` 接近真实秒数；当降级为均匀抽帧时，`time` 仅表示帧的先后顺序、并非精确时间戳。因此把截图对齐到章节时，用它做「大致排序」即可，不要当作精确时间引用。

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
