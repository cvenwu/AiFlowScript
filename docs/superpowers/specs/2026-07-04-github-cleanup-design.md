# GitHub 主页整理与开源产出提升 — 设计文档

- 日期：2026-07-04
- 目标账号：[github.com/cvenwu](https://github.com/cvenwu)（显示名 `cven`）
- 交付物：本设计文档 + 后续实施计划（writing-plans）
- 最终效果：他人看到主页即知「干净整洁、能同时做 Go 后端 & AI 工程、且有开源产出」

---

## 1. 背景与现状

### 1.1 账号快照

| 项 | 值 |
|---|---|
| 用户名 / 显示名 | `cvenwu` / `cven` |
| Followers / Following | 79 / 141 |
| 公开仓库总数 | 79（本文档逐仓覆盖） |
| 位置 / 博客 | Beijing / `yirufeng.top` |
| 徽章 | Pull Shark ×2、YOLO、Arctic Code Vault、Starstruck |
| 已有 Star Lists | 32 个（偏碎片化） |

### 1.2 核心问题

1. **信号被噪音淹没**：79 个仓库中，约有 10 个重复博客/主页仓、3 个图床仓、2 个模板仓、25 个纯学习记录仓、17 个 fork，把真正有价值的项目压在第 2、3 页。
2. **最强社会证明被埋没**：`SimpleERP`（112★ / 36 fork）在第 3 页；`GraduationProject`（14★，NLP/CNN）也不在首屏。
3. **主页 README 空缺**：`cvenwu/cvenwu`（Profile README 专用仓）内容极简，未承担「15 秒说清定位」的作用。
4. **无明确定位**：招聘方无法一眼看出「能同时做 Go 后端 & AI 工程」。
5. **Star 碎片化**：32 个列表过细；最近一批 AI/Agent star（superpowers、ECC、hello-agents 等）尚未归类。

### 1.3 关键技术约束

- **Star Lists 无写 API**：只能在 GitHub 网页 UI 手动编辑 → 该部分以「可复制文案 + 逐步 UI 操作清单」交付。
- **仓库操作需鉴权**：archive / rename / description / topics / README push 需 `gh` CLI 或 token。当前机器**无 `gh`、无 token** → 用户已确认「提供授权代执行」，执行阶段前需先完成鉴权。
- **Archive 是可逆只读**：归档后仓库仍可见、保留 star/fork，可随时 unarchive；本方案对**所有仓库零删除**。

---

## 2. 已确认的决策（来自 brainstorming）

| # | 决策点 | 结论 |
|---|---|---|
| 1 | 目标人群 | **AI / 后端招聘方**：展示可运行项目 + 深度学习产出 |
| 2 | 清理力度 | **保守**：Archive + 合并，**零删除**（含 fork，全程可逆） |
| 3 | Star 策略 | 32 列表 → **归并为 11 类精简分类** |
| 4 | 执行方式 | 用户提供授权，可自动化部分代执行；Star Lists 走 UI 引导 |
| 5 | 重点投入 | **主页 README + Pinned** 与 **AiFlow / AiKnowledge README 深度打磨** |
| 6 | 整体编排 | **清理优先**：① 清理 → ② 主页 → ③ 旗舰 README → ④ Star |
| 7 | 噪音学习仓合并力度 | **合并成 1 个 `study-notes` 总仓**（原仓归档） |
| 8 | Pinned 偏向 | **均衡（AI + 系统）** |
| 9 | 主页语言 | **中文主导**（关键术语保留英文） |
| 10 | Stats 卡片 | **加动态 stats 卡片** |
| 11 | 「关于我」定位 | 不写「转型」，写「**能同时胜任 Go 后端 & AI 工程**」双栈 |
| 12 | 旗舰打磨范围 | **仅 `AiFlow` 与 `AiKnowledge`**，两者都做**深度**打磨 |
| 13 | 文档位置 | `AiFlowScript/docs/superpowers/specs/` |
| 14 | Fork 处理 | **全部 fork 一律归档**（archive，不删除，可逆） |

---

## 3. 整体架构：四阶段流水线（清理优先）

```
阶段①  仓库清理           阶段②  主页门面            阶段③  旗舰打磨          阶段④  Star 重组
 ├─ 归档全部 fork(17)  →   ├─ cvenwu/cvenwu     →   ├─ AiFlow 深度     →   ├─ 32→11 类
 ├─ 合并→study-notes(25)   │   README 重写            └─ AiKnowledge 深度    ├─ 未分类 star 归位
 ├─ 归档噪音仓(22)         └─ 设置 6 个 Pinned                              └─ UI 手动执行
 └─ 保留+优化 meta(15)
    （需 gh/token）          （需 gh/token + UI）      （本地改 + push）       （纯 UI，无需 token）
```

每个阶段**独立可停**，完成即有可见收益。阶段①③可用脚本自动化；②的 Pinned 设置与④全程走 UI。

> **纯零删除方案**：本方案对所有仓库（含 fork）一律「保留 / 合并 / 归档」，不删除任何仓库，全程可逆。

---

## 4. 阶段①：仓库清理策略

### 4.1 五种处置动作

| 标记 | 动作 | 是否可逆 | 说明 |
|---|---|---|---|
| 📌 PIN | 保留 + 打磨 + 置顶 | — | 招聘方首屏 6 个 |
| ✅ KEEP | 保留 + 优化 description/topics | — | 有 star 或支撑定位的项目 |
| 🔀 MERGE | 内容迁入 `study-notes`，原仓归档 | 可逆 | 25 个纯学习仓合并成 1 仓 |
| 📦 ARCHIVE | 翻为只读归档 | 可逆（unarchive） | 博客/图床/模板/离题仓 + 全部 fork，star 保留 |

### 4.2 合并仓 `study-notes` 结构

新建 1 个聚合仓，25 个学习仓内容按目录归档，原仓翻为 archive（保留 star 与历史）：

```
study-notes/
├── README.md              # 目录导航 + 说明「历史学习笔记归档」
├── go/                    # GoDemo, OldBoyGolang, GoInAction, GinFrameworkDemo,
│                          #   Gin_vue, GoWorkFlow, GoAppTemplate, gin_blog, GithubWebhookGo
├── algorithm/             # LeetCodeSolutions, AlgoSolutions
├── cpp/                   # CppLibrary, CppTemplates
├── python/                # PythonNote, PythonCodeHelper
├── database/              # MySqlCookbook
├── ml/                    # ML_AndrewNg
├── interview/             # BasicCompu
├── crawler/               # CrawlDoubanMovie, BaiduMapSpider, CrawlITBooks
├── git/                   # GitCommandDemo
└── notes/                 # GitBook, Wiki, LearningRecord
```

> 迁移方式：保留原仓历史（`git subtree` 或按目录复制 + 在 study-notes 的 README 标注来源链接），原仓 archive。**内容不丢失、star 不丢失**（原仓归档仍可见）。

### 4.3 六个 Pinned 仓（均衡 AI + 系统）

| Pinned | 语言 | 价值定位 | star |
|---|---|---|---|
| `AiFlowScript` | Python | AI Agent 项目驱动学习与实战 | — |
| `AiFlow` | — | 103 个可公开 Agent Skill 合集（蹭 skills 热点） | — |
| `AiKnowledge` | VitePress | AI 学习知识库（已部署站点） | — |
| `OpenPresetBFF` | Go | Go BFF 服务 | 1 |
| `DistributedFileServer` | Go | Go 分布式文件上传服务 | 3 |
| `GraduationProject` | Python | 基于 CNN 与词向量的句子相似度（AI 方向对口） | 14 |

> `SimpleERP`（112★, Java 2018）不置顶：语言与年代不贴合 AI/Go 后端定位，改为 KEEP 保留，作为背景社会证明仍可见。
> Pinned 六仓覆盖 AI 应用（AiFlowScript/AiFlow/AiKnowledge）+ Go 后端分布式（OpenPresetBFF/DistributedFileServer）+ AI 学术产出（GraduationProject），整体偏 AI、兼顾后端。

### 4.4 全 79 仓决策表

> 说明：本方案零删除，所有仓库归入 保留 / 合并 / 归档 三类；⚠️ 仅在离题但有 star 的仓库上提示可复核。

#### 📌 PIN（6）
| 仓库 | 语言 | star | 动作 |
|---|---|---|---|
| AiFlowScript | Python | — | 保留+置顶（README 已精品，仅微调） |
| AiFlow | TS | — | 保留+置顶+**深度打磨 README** |
| AiKnowledge | VitePress | — | 保留+置顶+**深度打磨 README** |
| OpenPresetBFF | Go | 1 | 保留+置顶+补 meta |
| DistributedFileServer | Go | 3 | 保留+置顶+补 meta |
| GraduationProject | Python | 14 | 保留+置顶+补 meta（AI 方向对口） |

#### ✅ KEEP（9）
| 仓库 | 语言 | star | 动作 |
|---|---|---|---|
| cvenwu | — | — | Profile README 专用仓（阶段②重写） |
| PersonalResume | Astro | — | 保留，补 description |
| CheatSheetCollection | — | — | 保留（活跃、有用） |
| SimpleERP | Java | 112 | 保留+优化 meta（背景社会证明，不置顶） |
| GetLinksFromSoBooks | Python | 7 | 保留+优化 meta |
| AlgoBook | — | 6 | 保留（刷题文档，有 star） |
| ImageEntropy | Python | 5 | 保留 |
| BooksMark | HTML | 5 | 保留 |
| DistributedFileSystem | Go | 2 | 保留（分布式实践） |

#### 🔀 MERGE → `study-notes`（25，原仓归档）
GoDemo(1★) · OldBoyGolang(2★) · GoInAction · GinFrameworkDemo · Gin_vue · GoWorkFlow · GoAppTemplate · gin_blog · GithubWebhookGo · LeetCodeSolutions · AlgoSolutions · CppLibrary · CppTemplates · PythonNote · PythonCodeHelper · MySqlCookbook · ML_AndrewNg · BasicCompu · CrawlDoubanMovie · BaiduMapSpider(1★) · CrawlITBooks(1★) · GitCommandDemo · GitBook · Wiki · LearningRecord

#### 📦 ARCHIVE（22，只读、star 保留）
**博客/主页（10）**：VuePressPlumeTheme · stellar_blog · YiBlog · sivanWu0222.github.io · sivanWu0222.github.io.sourcecode · sivanWu0222.github.io2(1★) · sivanWu0222 · sivan0222.cn · love.sivanWu0222.github.io · resume.sivanWu0222.github.io
**图床（3）**：UpicGallery · UpicImageHosting · ImageHosting
**模板（2）**：MaterialDocTemplate · DocsifyTemplate
**离题/旧（7）**：OnlineDocuments · GithubApiVi · ResourceManage · ApplyMaster(1★) · LoveTimeLine(1★) · ChooseCourse(3★，旧 ASP.NET) · DiplomaProject（GraduationProject 的重复项）

#### 📦 ARCHIVE — 全部 fork（17，只读、star 保留、不删除）
ohmyzsh · Cloudreve · new-pac · LeetCode-Go · EasyLeetCode · prometheus-book · go-stress-testing · ego-kit · photo2cartoon · ZSH_Config · gin-cloud-storage · practice-in-go · books · interview-baguwen · geektime-books · os-guide-cn(1★) · rhzl-Agentic-Design-Patterns-cn

> 用户已确认：所有 fork 一律归档（archive），不删除。归档保留 star、可随时 unarchive、可重新对比 upstream。

> 合计：6(PIN) + 9(KEEP) + 25(MERGE) + 22(ARCHIVE 噪音仓) + 17(ARCHIVE fork) = **79** ✓

---

## 5. 阶段②：主页 README（`cvenwu/cvenwu`）

中文主导，关键术语保留英文；遵循中文技术写作规范（「」直角引号、CJK 与 Latin 间留空格）。

### 5.1 结构（从上到下）

1. **头图 Banner**：`cven` + 一句话定位「Go 服务端研发 & AI Agent 应用 / Harness 工程师」+ tagline；居中，配社交徽章（博客、followers）。
2. **关于我**（不写「转型」，强调双栈）：
   - 🧩 **双栈工程师**：既能做 **Go 服务端研发**（高并发、分布式、微服务治理），也能做 **AI Agent 应用 & Harness 工程**（Agent Loop、Tool Calling、上下文管理、评测）
   - 🏗️ 有大规模后端系统经验（可脱敏表述，如 10w+ QPS 延迟收益系统）
   - 🔬 偏好从第一性原理讲清底层机制，不止会用框架
3. **🚀 精选项目**：6 个 Pinned 的两列表格（一句话价值 + 技术标签），供 15 秒扫读。
4. **🛠️ 技术栈**：徽章行 Go / Python / AI Agent（LangGraph、MCP、Ollama）/ 分布式 / DevOps。
5. **📊 GitHub Stats**：`github-readme-stats` + top-langs + streak 卡片（动态自更新）。
6. **📫 联系方式**：博客 `yirufeng.top`，邮箱（可选）。

### 5.2 设计原则

- 首屏（关于我 + 精选项目）必须无需滚动即可看懂定位。
- 精选项目表格里的技术标签直接对齐招聘 JD 关键词（Go、分布式、AI Agent、RAG、LLM）。
- Stats 卡片依赖外部服务（`github-readme-stats`），若被墙/失效不影响核心信息（放在页面下半部）。

---

## 6. 阶段③：旗舰 README 深度打磨

仅 `AiFlow` 与 `AiKnowledge`，两者都做**深度**（badges + 一句话定位 + 快速开始 + 内容/skill 目录表 + Mermaid 架构图 + 截图/demo + 贡献指南）。`AiFlowScript` README 已是精品，仅微调。

### 6.1 `AiFlow`（最可能出圈的开源产出）

- **Badges**：License、Skill 数量、Stars、PRs Welcome、平台（TRAE/Claude/Codex）。
- **一句话定位**：通用 AI Agent Skill 合集，103 个可公开 Skill，一键安装。
- **Skill 分类目录表**：按领域分组（图像/视频、前端设计、Go/后端、文档、检索…），每个附一句话。
- **架构图（Mermaid）**：Skill 发现 → 加载 → 执行的机制图。
- **Demo**：一键安装 GIF/截图 + 一个 skill 调用示例。
- **贡献指南**：如何新增 skill、目录规范。

### 6.2 `AiKnowledge`（有已部署站点，加分）

- **Badges**：License、VitePress、部署状态（GitHub Pages）、在线站点链接。
- **一句话定位**：AI 学习知识库（面试题 + 分类学习 + 资源导航）。
- **内容地图**：interview / learning / resources 三大板块目录表 + 站点直达链接。
- **架构图（Mermaid）**：内容结构 / 部署流程。
- **截图**：站点首页与典型文章页。

---

## 7. 阶段④：Star 重组（32 → 11 类，UI 手动）

### 7.1 目标 11 类

| # | 分类 | 归并来源（原 32 列表） |
|---|---|---|
| 1 | AI / Agent | AIGC、项目（AI 部分）、+ 未分类 AI star |
| 2 | LLM 基础 | AIGC（模型/基础部分） |
| 3 | Go / 后端 | Go |
| 4 | 分布式 / 系统设计 | SystemDesign、Database、云原生、TSDB、Cloud Computing |
| 5 | 算法 | Algorithm |
| 6 | 面试 / 八股 | interview、Basic Knowledge 八股、resume |
| 7 | C / C++ | C++、C language、Assembly、Linux Kernel |
| 8 | Rust | Rust |
| 9 | 云原生 / DevOps | Devops、Docker、云原生、network、Linux |
| 10 | 工具 / 效率 | Tools、Font、README、frontend、IOT、游戏开发 |
| 11 | 软技能 / 职业 | SoftSkills、Books、Design Pattern、OS |

> 分类为「精简高层」，允许一个 star 归多个列表（GitHub 支持）。执行时以「新建 11 个列表 → 逐列表添加成员」的方式，不强行删除旧列表（旧列表可留可清，由用户 UI 决定）。

### 7.2 未分类新 star 归位（示例）

superpowers / ECC → AI/Agent；hello-agents / all-agentic-architectures / ai-agent-book → AI/Agent；md2wechat-skill / guizang-social-card-skill → 工具/效率；cc-switch / Understand-Anything → 工具/效率；mianshiya / AIGC-Interview-Book / ai-agent-interview-guide → 面试/八股；LLMForEverybody → LLM 基础。

### 7.3 交付形式（无 API）

- 每个新列表给出「名称 + 一句话描述」可复制文案。
- 给出逐步 UI 操作清单（新建列表 → 在每个 repo 的 Star ▾ 勾选归类）。
- 提供一份「repo → 目标列表」映射表，用户照表勾选。

---

## 8. 执行机制、安全与回滚

### 8.1 鉴权前置

执行阶段①③前需先满足其一：
- 安装 `gh` CLI 并 `gh auth login`，或
- 提供具备 `repo` 权限的 Personal Access Token（用于脚本调用 REST API）。

阶段②的 Pinned 设置与阶段④全程走 UI，无需 token。

### 8.2 安全护栏

- **零删除**：所有仓库（含 fork）一律 archive 或合并归档（可逆），不删除任何仓库。
- **合并保历史**：`study-notes` 迁移保留来源信息；原仓 archive 而非删除。
- **批量前 dry-run**：每个批量动作先输出待操作清单供用户确认，再执行。
- **分批提交**：README/仓库改动按仓提交，信息清晰，便于回滚。

### 8.3 回滚方式

| 动作 | 回滚 |
|---|---|
| Archive（含 fork） | UI/API `unarchive` |
| Rename | 改回原名（GitHub 保留重定向） |
| Merge | 原仓归档仍在，可 unarchive 恢复独立 |
| README | git 历史回退 |

---

## 9. 成功标准（招聘方视角）

1. 主页首屏：清晰定位 + 6 个 Pinned + stats，15 秒看懂「能做 Go 后端 & AI」。
2. 仓库列表首页不再被博客/图床/学习记录刷屏。
3. `AiFlow` / `AiKnowledge` 具备专业 README（badges + 架构图 + demo）。
4. Star 从 32 碎片列表 → 11 类，新 AI star 全部归位。
5. 全程可回滚、无原创内容丢失。

---

## 10. 范围与非目标（YAGNI）

- **本计划不做**：孵化某个明星开源项目（需持续投入，仅在后续单独立项）；重写 `AiFlowScript` README（已精品）；打磨除 AiFlow/AiKnowledge 外的旗舰 README；删除任何仓库。
- **可选、留待用户拍板**：Star 旧列表是否清空；`SimpleERP` 是否后续也补 topics。
