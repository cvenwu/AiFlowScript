# AI 七岗位 · GPT-Image 2 岗位信息卡海报提示词（高密度完整版 · 含中文文字）

> 运行模式：**Mode C（仅提示词）**。GPT-Image 2 未启用 Garden，本文件产出 7 条可直接复制的高质量 prompt，丢进任意 GPT-Image 2 / DALL·E / Nano Banana / ChatGPT 出图工具执行。
> 每张卡 = 一个岗位的**完整档案页**，包含 5 个分区：① 定位介绍 ② 硬性要求 ③ 加分项 ④ 高频技能(P0/P1/P2) ⑤ 代表 JD 摘录。
> 视觉基底：沿用《AI 七岗位 Dossier》机密档案美学 —— 深蓝近黑底 #0a0f1c + 细网格纹理 + 衬线大标题 + JetBrains Mono 等宽英文 + 每岗一种专属强调色。
> 规格：竖版 **3:4**（文字多，建议 1024x1536 或更长），所有中文必须清晰、字形正确；技能标签用 P0(玫瑰红 #ff8a7a) / P1(琥珀 #f4b740) / P2(青绿 #5be0c0) 三档色点区分。

---

## 文字渲染说明（重要）

每张卡中文信息量很大，GPT-Image 2 渲染大段中文易出错。三种应对：
1. **优先**：照下方 prompt 出图，出错的字单独重出强调。
2. **降级**：把「代表 JD 摘录」改为 1 条精简引用，减少文字量。
3. **混排**：分区小标题用英文（POSITION / REQUIREMENTS / PLUS / SKILLS / JD），正文用中文，渲染更稳。

---

## 01 · AI Agent 开发工程师（应用主干 · 强调色：青绿 Teal）

```
Vertical 3:4 high-density "career intelligence dossier" infographic poster, deep navy-black #0a0f1c background with faint technical grid texture and a teal radial glow, thin dashed teal-amber frame with filigree corners, top stamp "CONFIDENTIAL · CAREER INTELLIGENCE". Editorial multi-section layout, serif Chinese headlines + JetBrains Mono English labels, teal as the single accent color. ALL Chinese text must be rendered accurately and legibly.

HEADER: monospace "// ROLE 01 · APPLICATION", large serif Chinese title "AI Agent 开发工程师", monospace alias "AI AGENT ENGINEER · APPLICATION ENGINEER".
POSITION PITCH (highlighted quote bar): "把大模型从会聊天的 demo 做成能稳定完成多步骤真实任务的产品 —— 设计 agent 行为、工具策略、上下文构造与评测闭环。"
A small teal flat-illustration on the side: an agent loop (model → tool call → result feedback → re-decide) with tool icons.

SECTION ① 硬性要求:
  · 学历：海外不卡，国内本科及以上
  · 语言：Python 必备，国内后台常加 Go/Java/C++
  · 经验：构建/上线过 LLM 驱动产品，海外资深 5–8 年
  · 核心技能：Prompt 工程、工具调用、上下文构造、Evals、RAG、结构化输出、多 agent 编排、MCP
SECTION ② 加分项:
  · 熟悉 LangChain / LangGraph / AutoGen / CrewAI
  · 代码生成模型、开发者工具方向研究
  · 处理大规模脏数据 / 生产日志
  · 重度使用 Claude Code / Cursor / Codex / Manus
  · 有 SFT / RLHF 基础认知，能与算法对话
SECTION ③ 高频技能 (colored priority dots):
  P0: Python · Tool/Function Calling · Evals · Prompt/Context
  P1: RAG · Agent 框架 · MCP · Multi-agent 编排 · Planning/Memory
  P2: SFT/RLHF 概念 · 分布式后端 · 生产故障调试
SECTION ④ 代表 JD 摘录 (dashed quote cards):
  · OpenAI · Codex Core Agent：把 Codex agent 从 demo 做成可靠工具，构建并运行 evals，提升 prompt/tool-use/context 策略
  · DeepSeek Harness 团队：熟悉 Tool Use/Planning/长期记忆/Multi-Agent，深度使用过 Claude Code、Manus
  · 阿里云 AI Coding：设计 Agent 服务框架（推理决策/记忆/RAG），实现基于 MCP 的工具注册与调用

FOOTER: "AI · ROLE · DOSSIER · 2026 · 与模型距离：远 · 应用层".
No clutter, clear alignment, accurate legible Chinese.
```

---

## 02 · AI Harness 工程师（工程主干 · 强调色：玫瑰红 Rose）

```
Vertical 3:4 high-density "career intelligence dossier" infographic poster, deep navy-black #0a0f1c background with faint grid texture and a rose-red radial glow, thin dashed rose-amber frame, top stamp "CONFIDENTIAL · CAREER INTELLIGENCE". Editorial multi-section layout, serif Chinese headlines + JetBrains Mono English labels, rose-red accent. ALL Chinese text accurate and legible.

HEADER: monospace "// ROLE 02 · INFRASTRUCTURE", large serif Chinese title "AI Harness 工程师", monospace alias "AGENT RUNTIME / INFRA · PLATFORM ENGINEER".
POSITION PITCH (highlighted quote bar): "构建让模型能真正干活的那层 —— agent 循环 / 工具调度 / 沙箱执行 / 上下文管理 / eval harness / 大规模 agent 运行时。"
Side rose-red flat-illustration: isolated sandbox containers with shields, a tool-scheduler dispatching parallel jobs, Kubernetes hexagon cluster.

SECTION ① 硬性要求:
  · 学历：海外不卡，国内 infra 岗本科及以上
  · 经验：Anthropic 该岗最低 8+ 年系统/分布式经验
  · 核心技能：容器化(Kata/Firecracker/gVisor/Sysbox/K8s)、系统编程、分布式、安全基础设施、Tool-use SDK、Eval/RL 基础设施、FastAPI/gRPC、Terraform
SECTION ② 加分项:
  · 虚拟化/容器化运行时性能调优
  · LangChain / AutoGen 等 agent 框架源码经验
  · RL environments 与 agent 执行框架集成
  · 0→1 再扩展到 1,000,000x 的工程经验
  · MCP / Tool Use / Function Calling 协议设计
SECTION ③ 高频技能 (colored priority dots):
  P0: 容器化/Sandbox · Kubernetes · 系统编程 · 分布式系统
  P1: Eval Harness · Tool-use SDK · FastAPI/gRPC · Terraform/IaC · Agent 循环/编排
  P2: RL Environments · 运行时性能优化 · 可观测性
SECTION ④ 代表 JD 摘录 (dashed quote cards):
  · OpenAI · Agent Infrastructure：参与超越 K8s 能力上限的自研容器编排平台；点名 Kata/Firecracker/gVisor/Sysbox
  · Anthropic · Agents Infrastructure：构建沙箱代码执行环境与 tool-use SDK；最低 8+ 年经验，需 LangChain 经验
  · Scale AI · Agents：构建训练和评估自主 agent 的真实 RL environments，并行运行多个训练/评测任务

FOOTER: "AI · ROLE · DOSSIER · 2026 · 与模型距离：中 · 工程系统".
No clutter, clear alignment, accurate legible Chinese.
```

---

## 03 · AI 算法工程师（模型主干 · 强调色：靛蓝 Indigo）

```
Vertical 3:4 high-density "career intelligence dossier" infographic poster, deep navy-black #0a0f1c background with faint grid texture and an indigo radial glow, thin dashed indigo-amber frame, top stamp "CONFIDENTIAL · CAREER INTELLIGENCE". Editorial multi-section layout, serif Chinese headlines + JetBrains Mono English labels, indigo accent. ALL Chinese text accurate and legible.

HEADER: monospace "// ROLE 03 · MODEL CORE", large serif Chinese title "AI 算法工程师", monospace alias "RESEARCH ENGINEER · ML ENGINEER (LLM)".
POSITION PITCH (highlighted quote bar): "设计、实现并迭代大规模 ML 系统，把研究想法落地为可大规模训练 / 部署的 AI 能力，横跨研究与工程两端。"
Side indigo flat-illustration: stacked Transformer attention blocks with multi-head arrows, a descending loss curve, a multi-GPU training rack.

SECTION ① 硬性要求:
  · 学历：七岗中最宽松，本/硕/博皆可（DeepMind RE 明确）
  · 经验：构建过复杂/大规模分布式系统是核心硬指标
  · 核心技能：Python、PyTorch（或 JAX）、Transformer、分布式训练(FSDP/DeepSpeed/Megatron)、GPU 使用
SECTION ② 加分项:
  · GPU 优化、kernel 级实现、CUDA
  · Kubernetes、OS internals、云平台
  · 对 AI 社会影响有思考（OpenAI / Anthropic 反复强调）
SECTION ③ 高频技能 (colored priority dots):
  P0: Python · PyTorch · Transformer/LLM · 分布式训练
  P1: CUDA/GPU · FSDP/DeepSpeed/Megatron · 软件工程能力
  P2: JAX/TPU · RAG/Prompt(应用侧) · K8s/Docker
SECTION ④ 代表 JD 摘录 (dashed quote cards):
  · OpenAI · Research Engineer：设计、实现并改进大规模分布式 ML 系统；强编程 + 大规模分布式经验。薪资 $250K–$445K
  · DeepMind · Research Engineer：具备深厚 ML 理解的软件工程师，结合工程、数学与研究能力
  · 字节 Seed：覆盖 LLM/Foundation/多模态/Posttrain/AI Search，强调大规模分布式训练与底层系统建设

FOOTER: "AI · ROLE · DOSSIER · 2026 · 与模型距离：近 · 模型层".
No clutter, clear alignment, accurate legible Chinese.
```

---

## 04 · 预训练工程师（基座层 · 强调色：琥珀金 Amber）

```
Vertical 3:4 high-density "career intelligence dossier" infographic poster, deep navy-black #0a0f1c background with faint grid texture and a warm amber-gold radial glow, thin dashed amber frame, top stamp "CONFIDENTIAL · CAREER INTELLIGENCE". Editorial multi-section layout, serif Chinese headlines + JetBrains Mono English labels, amber-gold accent. ALL Chinese text accurate and legible.

HEADER: monospace "// ROLE 04 · FOUNDATION", large serif Chinese title "预训练工程师", monospace alias "PRETRAINING ENGINEER · FOUNDATION MODEL TRAINING".
POSITION PITCH (highlighted quote bar): "基座大模型从架构、数据、优化器到分布式训练全链路 —— 在数千张 GPU/TPU 上把训练效率、稳定性与模型质量推到极限。"
Side amber-gold flat-illustration: endless rows of glowing GPU/TPU server racks receding into a starfield, a 3D-parallelism diagram (data/tensor/pipeline three axes), a scaling-law curve rising.

SECTION ① 硬性要求:
  · 学历：偏硕博(CS/ML/数学/统计)，接受同等经验
  · 经验：DeepMind Gemini 预训练要求 5 年推理优化模型设计；普遍要求大规模 LLM 训练实操
  · 核心技能：3D 并行(数据/张量/流水线)、Megatron/DeepSpeed/FSDP/JAX+TPU+XLA、Transformer 架构、optimizer、大规模 ETL、训练稳定性
SECTION ② 加分项:
  · Scaling laws、inference-optimized 设计
  · XLA 原语与 JAX-on-TPU 实际机制
  · NVIDIA 生态：Megatron-Core / NeMo / TensorRT-LLM
  · 了解 RL / RLHF（衔接后训练）
SECTION ③ 高频技能 (colored priority dots):
  P0: 3D 并行/Megatron/DeepSpeed · PyTorch/JAX · CUDA/GPU 集群 · 大规模训练基础设施
  P1: Transformer 架构设计 · 数据处理/ETL · Optimizer/Scaling laws
  P2: TPU/XLA · 推理优化协同 · K8s/OS internals
SECTION ④ 代表 JD 摘录 (dashed quote cards):
  · Anthropic · Pre-training RE/RS：模型架构、算法、数据处理、优化器开发，全栈贡献。薪资 $350K–$850K
  · DeepMind · Pretraining (Gemini)：理解 XLA 原语 + JAX 在 TPU 上的运行；覆盖预训练/微调/serving
  · 月之暗面 Kimi 校招：明确开设大模型预训练/分布式训练/CUDA/高性能存储/AI Infra 方向

FOOTER: "AI · ROLE · DOSSIER · 2026 · 与模型距离：最近 · 模型底座".
No clutter, clear alignment, accurate legible Chinese.
```

---

## 05 · 后训练工程师（行为塑形 · 强调色：紫罗兰 Violet）

```
Vertical 3:4 high-density "career intelligence dossier" infographic poster, deep navy-black #0a0f1c background with faint grid texture and a violet radial glow, thin dashed violet-amber frame, top stamp "CONFIDENTIAL · CAREER INTELLIGENCE". Editorial multi-section layout, serif Chinese headlines + JetBrains Mono English labels, violet accent. ALL Chinese text accurate and legible.

HEADER: monospace "// ROLE 05 · ALIGNMENT", large serif Chinese title "后训练工程师", monospace alias "POST-TRAINING ENGINEER · ALIGNMENT · RLHF".
POSITION PITCH (highlighted quote bar): "在基座之上用 SFT/RLHF/RLAIF/DPO/GRPO 把模型调成听话、安全、有用、会推理用工具的产品级模型。2026 年权重显著上升的岗位。"
Side violet flat-illustration: an alignment chain SFT → Reward Model → RLHF/PPO → DPO → GRPO left-to-right, a reward gauge, thumbs-up/down preference-pair cards, a model gaining a glowing aligned halo.

SECTION ① 硬性要求:
  · 学历：两极 —— 研究岗常硕博，工程岗 1–3 年生产 LLM 训练 + 硕士
  · 经验：明确要求 LLM 训练/微调/后训练实操；掌握 SFT/RLHF/reward modeling 之一；多节点训练
  · 核心技能：SFT、RLHF、DPO、reward model、PPO/GRPO、TRL、transformers、flash attention、NeMo-RL、数据策略/evals
SECTION ② 加分项:
  · Agent / 多工具 rollout / 多智能体 RL（2026 强上升）
  · Reasoning 模型训练经验
  · 偏好数据构造、合成数据、评测体系
  · 系统优化与 GPU 集群架构理解
SECTION ③ 高频技能 (colored priority dots):
  P0: SFT · RLHF · DPO · Reward Model
  P1: PPO/GRPO · TRL/NeMo-RL · Alignment/安全 · PyTorch/transformers
  P2: RLAIF/RLVR · Agent/Tool 训练 · 数据 curation
SECTION ④ 代表 JD 摘录 (dashed quote cards):
  · Scale AI · Post-Training Research：SFT、RLHF、reward modeling 专长；优化数据 curation 与评测。博/硕士
  · Scale AI · Agent Post-training：为 multi-agent/multi-tool rollouts 开发下一代训练算法；CUDA/PyTorch/transformers/flash attention
  · Hugging Face TRL v1.0：过去一年 LLM 重心从预训练转向后训练；SFT + Reward + DPO + GRPO 统一栈

FOOTER: "AI · ROLE · DOSSIER · 2026 · 与模型距离：近 · 行为塑形".
No clutter, clear alignment, accurate legible Chinese.
```

---

## 06 · AI Infra 工程师（底层系统 · 强调色：玫瑰红+琥珀机械感）

```
Vertical 3:4 high-density "career intelligence dossier" infographic poster, deep navy-black #0a0f1c background with faint grid texture and a rose+amber dual radial glow, thin dashed amber frame, top stamp "CONFIDENTIAL · CAREER INTELLIGENCE". Editorial multi-section layout, serif Chinese headlines + JetBrains Mono English labels, rose+amber accents, technical machine aesthetic. ALL Chinese text accurate and legible.

HEADER: monospace "// ROLE 06 · ML SYSTEMS", large serif Chinese title "AI Infra 工程师", monospace alias "ML INFRASTRUCTURE · INFERENCE / TRAINING SYSTEMS".
POSITION PITCH (highlighted quote bar): "让超大规模模型在 GPU 集群上训得动、训得快、推得省、不宕机。分布式训练、推理服务化、性能优化、底层算子与通信。"
Side flat-illustration: a CUDA GPU die with glowing kernel grid, NVLink/InfiniBand cables, an inference-serving pipeline with KV-cache blocks and batched requests, latency/throughput gauges.

SECTION ① 硬性要求:
  · 学历：本科及以上（国内大厂硕博优先）
  · 经验：OpenAI Model Inference 明确 5 年+；国内大厂 2 年+，千卡训练经验强加分
  · 核心技能：Python + C/C++(或 Rust)；CUDA/Triton/CUTLASS/Flash Attention；vLLM/SGLang/TensorRT-LLM；NCCL/NVLink/IB/MPI；Megatron/DeepSpeed/FSDP；量化/KV cache/batching/speculative decoding
SECTION ② 加分项:
  · 千卡/万卡级训练实战
  · HPC 背景(InfiniBand/MPI/NVLink)
  · 开源贡献、顶会论文、可量化性能突破
  · Nsight 等 profiling、内存带宽瓶颈优化
SECTION ③ 高频技能 (colored priority dots):
  P0: CUDA/GPU kernel · vLLM/SGLang/TensorRT-LLM · PyTorch/JAX · 分布式训练/NCCL
  P1: Megatron/DeepSpeed/FSDP · 量化/KV cache/批处理 · C/C++/Rust · Kubernetes/CI-CD
  P2: Triton/CUTLASS/Flash Attention · InfiniBand/MPI/HPC
SECTION ④ 代表 JD 摘录 (dashed quote cards):
  · OpenAI · Model Inference：优化 latency/throughput/efficiency；PyTorch/CUDA/NCCL/IB/MPI/NVLink。$295K–$555K
  · Anthropic · GPU Performance：为下一代硬件协同设计 attention/算子；量化与混合精度 custom kernel；planet-scale 分布式训练
  · xAI · Inference：目标 100% uptime、0% error rate、优秀尾延迟；vLLM/SGLang/TensorRT-LLM/量化/speculative decoding
  · 腾讯混元 · 推理加速：vLLM/SGLang/TRT/算子融合/量化/动态批处理/KV 缓存优化

FOOTER: "AI · ROLE · DOSSIER · 2026 · 与模型距离：最近 · 系统底层".
No clutter, clear alignment, accurate legible Chinese.
```

---

## 07 · AI 产品经理（用户/商业层 · 强调色：青绿+琥珀暖调）

```
Vertical 3:4 high-density "career intelligence dossier" infographic poster, deep navy-black #0a0f1c background with faint grid texture and a teal+amber warm radial glow, thin dashed amber frame, top stamp "CONFIDENTIAL · CAREER INTELLIGENCE". Editorial multi-section layout, serif Chinese headlines + JetBrains Mono English labels, teal+amber accents. ALL Chinese text accurate and legible.

HEADER: monospace "// ROLE 07 · PRODUCT", large serif Chinese title "AI 产品经理", monospace alias "AI PRODUCT MANAGER · LLM PRODUCT MANAGER".
POSITION PITCH (highlighted quote bar): "把大模型能力与边界翻译成可落地、有商业价值的产品 —— 需求洞察、PRD、技术路径评估、效果评测、数据闭环、跨职能推动上线。"
Side teal-amber flat-illustration: a glowing LLM core on one side, product UI mockups / user avatars on the other, connected by a PRD document, a requirements magnifier, an evaluation feedback loop and a rising value arrow.

SECTION ① 硬性要求:
  · 学历：本科及以上；Scale AI 明确技术学位(CS/工程)或等同经验
  · 经验：海外资深 4 年+ ML 产品；国内多需 AIGC/大模型产品实习或项目
  · 核心技能：LLM 应用范式(Prompt/RAG/Agent/AIGC/多模态)、能力边界与局限理解、产品基本功、技术路径与成本评估、评测与数据闭环、跨职能协作、Python/SQL/数据分析
SECTION ② 加分项:
  · 有自做的 Agent / RAG / AIGC 项目
  · 企业级 B 端 / 增长 / 实验平台经验
  · 商业化、定价、ML pipeline 理解
SECTION ③ 高频技能 (colored priority dots):
  P0: LLM 能力与边界理解 · RAG · Agent · Prompt Engineering · 需求洞察/竞品
  P1: PRD/原型/体验 · 评测/Bad Case 归因 · 跨职能协作
  P2: Python/SQL/数据分析 · AIGC/多模态/NLP
SECTION ④ 代表 JD 摘录 (dashed quote cards):
  · Google DeepMind · PM Gemini App：在基础性不确定中引领产品、快速战略转向；理解并代表用户需求
  · Scale AI · AI PM (GenAI)：技术学位 + 4 年 ML 产品；理解 GenAI 企业应用；Python 编码能力
  · 小红书 · AI 产品经理：理解能力边界(幻觉/时效/安全)，跟踪 LLM/Agent/RAG；Prompt Engineering 加分
  · 字节 · 豆包/飞书 AI PM：熟悉海内外大模型产品；了解 ML/深度学习原理；AIGC 实战项目经验为门槛

FOOTER: "AI · ROLE · DOSSIER · 2026 · 与模型距离：远 · 用户/商业层".
No clutter, clear alignment, accurate legible Chinese.
```

---

## 使用建议

- **批量出图**：逐条复制到 GPT-Image 2 / ChatGPT 出图，尺寸建议 `1024x1536`（3:4），quality `high`。
- **文字太密出错时**：优先按「文字渲染说明」降级（精简 JD 摘录到 1 条 / 分区标题改英文）。
- **保系列感**：7 张共用同一套 Dossier 基底，仅强调色 + 中心视觉 + 文案不同，拼起来即成一套档案册。
- **想要总览页**：可另出 1 张「七岗位 2×4 网格总表」横版海报作封面（如需我可补 prompt）。
