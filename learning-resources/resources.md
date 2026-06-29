# AI 学习资源收藏

> 按 AI 学习路径整理：基础理论 → 提示词 → Agent → 工程化 → 面试求职

---

## 一、AI 基础与理论

| 名称 | 链接 | 备注 |
|------|------|------|
| 斯坦福 CS336《从零构建语言模型》中文电子书 | [github.com/feigaobox10/llm-from-scratch-reader](https://github.com/feigaobox10/llm-from-scratch-reader) | 17 讲完整整理，从分词到对齐，配原创图；[在线预览](https://feigaobox10.github.io/llm-from-scratch-reader/) |
| 《计算机视觉基础》Foundations of Computer Vision | [visionbook.mit.edu](https://visionbook.mit.edu) | MIT 出品，图像处理与机器学习视角 |
| AI 术语定义 Glossary | [jimmysong.io/zh/glossary/](https://jimmysong.io/zh/glossary/) | 中英对照术语表 |
| AliceLabs AI 知识库 | [alicelabs.ai](https://alicelabs.ai/en/) | AI 知识点与面试点讲解 |

---

## 二、大模型训练与推理

| 名称 | 链接 | 备注 |
|------|------|------|
| AI Infra 基础设施 | [github.com/Infrasys-AI/AIInfra](https://github.com/Infrasys-AI/AIInfra) | AI 基础设施相关资源合集 |
| 《推理工程》Inference Engineering 电子书 | [baseten.co/inference-engineering](https://www.baseten.co/inference-engineering/digital-download/) | Baseten 出品，需填邮箱下载；涵盖推理优化全链路 |

---

## 三、提示词工程（Prompt Engineering）

| 名称 | 链接 | 备注 |
|------|------|------|
| Kimi 官方《提示词 Prompt 最佳实践》 | [platform.kimi.com/docs/guide/prompt-best-practice](https://platform.kimi.com/docs/guide/prompt-best-practice) | 官方文档，全面系统 |
| 写作提示词电子书 | [飞书文件](https://r9hngt2bty.feishu.cn/file/O2HNb3MwKo799Nx42jycW7mJnid) | 提炼自 How I Write 播客（David Perell），含多位知名作家/学者的写作心得 |

---

## 四、AI Agent 核心概念与实现

### 4.1 入门概念

| 名称 | 链接 | 备注 |
|------|------|------|
| Agent 的概念、原理与构建模式（视频） | [B站 b23.tv/wsMyjlP](https://b23.tv/wsMyjlP) | 马克的技术工坊出品，从零打造简化版 Claude Code |
| React 从零到一实现（代码） | [GitHub](https://github.com/MarkTechStation/VideoCode/blob/main/Agent%E7%9A%84%E6%A6%82%E5%BF%B5%E3%80%81%E5%8E%9F%E7%90%86%E4%B8%8E%E6%9E%84%E5%BB%BA%E6%A8%A1%E5%BC%8F/agent.py) | 配套视频的代码实现 |
| LangChain Plan and Execute 实现 | [langchain-ai.github.io](https://langchain-ai.github.io/langgraph/tutorials/plan-and-execute/plan-and-execute/) | LangGraph 官方教程 |

### 4.2 系统学习

| 名称 | 链接 | 备注 |
|------|------|------|
| Agent Learning Hub（完整学习路线） | [github.com/datawhalechina/Agent-Learning-Hub](https://github.com/datawhalechina/Agent-Learning-Hub) | Datawhale 出品，从最小 Agent Loop 到 Skills/MCP/A2A/评测/trace/安全 |
| 《智能体构建指南》 | [jimmysong.io/zh/book/ai-handbook/](https://jimmysong.io/zh/book/ai-handbook/) | Jimmy Song 的 Agent 构建手册 |
| 《智能体 AI 漫游指南：从基础到系统》 | [arxiv.org/abs/2606.24937](https://arxiv.org/abs/2606.24937) | 面向实践者的综合性参考书，覆盖 Transformer → 训练 → 对齐 → Agent → 多智能体 → 部署全链路 |
| AI Agent 架构：从单体到企业级多智能体 | [waylandz.com/ai-agent-book/](https://waylandz.com/ai-agent-book/) | 系统讲解 Agent 架构演进 |

### 4.3 Agent 框架与工具

| 名称 | 链接 | 备注 |
|------|------|------|
| AI Agent Frameworks 2026 排名 | [alicelabs.ai](https://alicelabs.ai/en/insights/best-ai-agent-frameworks-2026) | 生产环境实测排名 |
| 《图解 Skill —— AI 提效实战指南》开源项目 | [github.com/JimLiu/Illustrated-Agent-Skills](https://github.com/JimLiu/Illustrated-Agent-Skills) | 配套开源项目，含作者自用 Skills |

### 4.4 Agent 工程实践

| 名称 | 链接 | 备注 |
|------|------|------|
| Loop Engineering 概念解析、思考与实践 | [微信公众号文章](https://mp.weixin.qq.com/s?__biz=Mzg4NTczNzg2OA==&mid=2247509834&idx=1&sn=b514f1bc2616df514cb218a5bad28296) | Agent 循环工程深度解析 |
| Building Pi With Pi（Armin Ronacher） | [lucumr.pocoo.org](https://lucumr.pocoo.org/2026/5/24/pi-oss/) | Pi 维护者的 Agent 工程反思，含 dogfooding 实践经验 |
| 另一篇 Agent 相关微信文章 | [微信公众号文章](https://mp.weixin.qq.com/s?__biz=Mzg4NTczNzg2OA==&mid=2247509639&idx=1&sn=bac09af0c76f4383f03c0d96cb48bd0a) | Agent 相关深度文章 |

---

## 五、Harness 工程

| 名称 | 链接 | 备注 |
|------|------|------|
| Learn Harness Engineering | [github.com/walkinglabs/learn-harness-engineering/](https://github.com/walkinglabs/learn-harness-engineering/) | 基于项目的课程：12 个概念单元 + 6 个动手项目 + 资源库 |
| Harness Books | [github.com/wquguru/harness-books](https://github.com/wquguru/harness-books) | Harness 工程教学项目 |

---

## 六、RAG 与知识检索

| 名称 | 链接 | 备注 |
|------|------|------|
| RAG 应用开发与实战手册 | [jimmysong.io/zh/book/rag-handbook/](https://jimmysong.io/zh/book/rag-handbook/) | 构建长期复利型知识基础设施 |

---

## 七、大模型评测（Evals）

| 名称 | 链接 | 备注 |
|------|------|------|
| Evals 概念详解 | （见下方说明） | 用户整理的系统化评测知识 |

> **Evals = 给 LLM/Agent 建立可量化的考试系统**
>
> 一个 eval 由三部分组成：**数据集**（输入 + 期望表现）、**运行器**（喂给模型收集输出）、**评分器**（判断对错）。
>
> 评分方式：
> - **精确/规则匹配**：数学题、代码、分类
> - **LLM-as-judge**：用强模型打分，适用于开放式回答、摘要、对话质量
> - **人工标注**：最准但贵，用于黄金基准、对齐/安全
> - **任务成功率**：Agent 是否真的完成了任务
>
> 两个层面：
> - **公开基准（benchmark）**：MMLU、GSM8K、HumanEval、SWE-bench、Terminal-bench
> - **私有/业务 evals**：自己业务场景的测试集（最重要）
>
> 7 个 AI 岗位都需要 evals：Agent 开发（任务成功率/回归）、Harness 工程（eval 基础设施）、后训练（判断 SFT/RLHF 效果）、产品经理（Bad Case 归因）

---

## 八、面试与求职

| 名称 | 链接 | 备注 |
|------|------|------|
| AI 应用开发工程师面试宝典 | [github.com/guocong-bincai/ai-interview-guide](https://github.com/guocong-bincai/ai-interview-guide) | 24 模块、341+ 题，系统化 + 实战导向 |
| 国内大厂 AI 工程师面试真题 | [面试真题目录](https://github.com/guocong-bincai/ai-interview-guide/tree/main/docs/18-big-tech-interview-questions) | 面试宝典子目录 |
| 简历与面试技巧 | [技巧目录](https://github.com/guocong-bincai/ai-interview-guide/tree/main/docs/16-resume-interview-tips) | 面试宝典子目录 |

---

## 九、综合教程平台

| 名称 | 链接 | 备注 |
|------|------|------|
| Jimmy Song 教程手册合集 | [jimmysong.io/zh/categories/tutorials/](https://jimmysong.io/zh/categories/tutorials/) | 各类教程和手册汇总 |
| 马克的技术工坊（B站） | 哔哩哔哩 | Agent 相关视频教程 |

---

## 十、个人想法与待探索

| 想法 | 说明 |
|------|------|
| 本地模型接入 | 将本地模型通过类似调用云端大模型 API 的方式，使代码能使用本地模型 |
| 观测平台 | 搭建 Agent 运行观测/监控平台 |

---

## 附：学习平台

- **哔哩哔哩**：视频教程主阵地
- **马克的技术工坊**：Agent 系列视频作者
- **AliceLabs**：AI 知识点与面试
- **Jimmy Song**：系统化教程与手册
- **Datawhale**：开源学习社区
