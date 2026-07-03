# bili-summary-BV1zSDMBUE5o · AI 应用技术串讲总结

把一个 B 站视频转成一份**单文件、可离线打开、带思维脑图**的技术总结 HTML。

- **视频**：《近年 AI 应用技术串讲与优质文档分享｜Agent、Skill、OpenClaw、Harness……》
- **UP 主**：堂吉诃德拉曼查的英豪 · 时长 33:45
- **原链接**：https://www.bilibili.com/video/BV1zSDMBUE5o/
- **产物**：`AI应用技术串讲-Agent-Skill-OpenClaw-Harness.html`（双击即用，无需联网）

## 产物内容

一条主线串起 12 个知识点（不重不漏），每节含要点 + Mermaid 原理/时序图 + 视频截图 + 参考文档：

`LLM/Transformer → Prompt 工程 → Fine-tuning/LoRA → RAG → Function Call → MCP → Agent/ReAct → Multi-Agent → Context Engineering → Agent Skill → OpenClaw → Harness`

顶部含**思维脑图**（五层：基石 → 让模型答得更好 → 赋予行动力 → 走向自主 → 复用与规模化）与**演进主线流程图**。

## 复现流程（踩坑记录）

管线：`下载 → 转写 → 截图 → 理解与对齐 → 生成 HTML`。

1. **yt-dlp 被 B 站 HTTP 412 拦截**：直连 `api.bilibili.com` 兜底——
   `/x/web-interface/view` 取 aid/cid/标题；`/x/player/playurl` 取 DASH 直链；
   用 `curl` 带 `Referer: <视频页>` 下载音视频流，再 `ffmpeg` mux + 抽 16k 单声道 wav。
2. **该视频无字幕**：`whisper-cli`（whisper.cpp，`ggml-large-v3-turbo`，Metal 加速）本地转写 → `transcript.srt`。
3. **关键帧**：`ffmpeg` 场景检测，讲解型视频阈值需调低（这里用 `0.08`）才能抓够转场，共 40 帧。
4. **生成 HTML**：`python3 build_report.py`——图片 base64 内嵌、`mermaid.min.js` 内联，
   零外部依赖；用 `agent-browser` 无头渲染实测 14/14 Mermaid 图渲染成功、0 报错。

## 与 Go 经验的类比（学习视角）

- **协议演进 = 中间件/IDL 的复用抽象**：Function Call（单点调用）→ MCP（工具跨应用复用，类似统一 RPC/IDL）→ Agent Skill（整个 Agent 打包复用，类似可分发的 SDK/插件包）。
- **Agent Loop = 状态机 + 事件循环**：思考→行动→观察，由模型输出决定是否终止，很像 `for { select {} }` 的决策循环。
- **Context Engineering = 内存/缓存预算管理**：上下文窗口是稀缺资源，Write/Select/Compress/Isolate 类比缓存淘汰与分片隔离。
- **Harness = 运维 + CI/CD 护栏**：约束边界、喂全上下文、写单测/推流水线验证、出错自愈——把 Agent 当成需要 Guardrail 的执行体。

## 备注

- `cookies.txt` 与原始音视频（`*.mp4/*.m4s/*.wav`）、签名直链（`*_url.txt`）、API dump 已在 `.gitignore` 中排除，**不入库**。
- 仓库保留 `transcript.srt` + `frames/` + `build_report.py`，凭这些即可离线重建 HTML。
