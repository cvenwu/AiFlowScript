# Star Lists 重组操作手册（32 → 11 类）

> ⚠️ 现实约束：你共有 **918 个 star**，其中现有 32 个列表仅覆盖约 165 个。GitHub Star Lists **没有写 API**，只能在网页 UI 手动操作。本手册配套自动分类结果，帮你按表批量勾选。

## 配套文件（已生成）

- `star-map.csv`：全部 918 个 `repo → 命中列表`（一个 repo 可多类，或 `UNCATEGORIZED`）。
- `star-lists/*.txt`：每个目标列表的成员清单（每行一个 `owner/repo`），共 11 个 + 1 个未分类。
- `starred-all.txt` / `starred-meta.jsonl`：原始 star 全量与元数据。

## 一、11 个目标列表（名称 + 描述，可直接复制）

| # | 列表名 | 描述 | 自动归类数 |
|---|--------|------|-----------|
| 01 | AI / Agent | AI Agent、多智能体、Agent 框架与实战 | 63 |
| 02 | LLM 基础 | 大模型原理、训练推理、深度学习 | 145 |
| 03 | Go / 后端 | Go 语言、Web 框架、后端工程 | 275 |
| 04 | 分布式 / 系统设计 | 分布式系统、系统设计、数据库、存储 | 110 |
| 05 | 算法 | 算法与数据结构、刷题 | 91 |
| 06 | 面试 / 八股 | 面试题库、八股、简历 | 102 |
| 07 | C / C++ | C、C++、汇编、Linux 内核 | 92 |
| 08 | Rust | Rust 语言与生态 | 32 |
| 09 | 云原生 / DevOps | K8s、Docker、监控、网络、Linux | 120 |
| 10 | 工具 / 效率 | CLI 工具、效率、前端、模板、IoT | 166 |
| 11 | 软技能 / 职业 | 软技能、书籍、设计模式、路线图 | 159 |

> 注：一个 repo 可同时归多个列表，故上表合计 > 918；未命中 181 个见 `star-lists/99-uncategorized.txt`。

## 二、创建列表步骤（每个列表重复一次）

1. 打开 https://github.com/cvenwu?tab=stars
2. 右侧 `Lists` → `Create list`
3. 粘贴上表「列表名」与「描述」→ Create

## 三、批量归类步骤（按清单勾选）

对每个列表 `star-lists/NN-xxx.txt`：

1. 打开该 txt，得到成员 `owner/repo` 清单。
2. 逐个访问 `https://github.com/<owner>/<repo>`，点 `Star` 旁的 `▾` → 勾选目标列表。
   - 或在 https://github.com/cvenwu?tab=stars 搜索框输入 repo 名，就地勾选更快。

> 建议优先处理与求职最相关的 3 类：**01 AI/Agent、03 Go/后端、06 面试/八股**（招聘方最看重）。其余列表可分批慢慢补。

## 四、旧列表归并映射（原 32 → 新 11）

- AI / Agent ← AIGC、项目（AI 部分）
- LLM 基础 ← AIGC（模型/基础部分）
- Go / 后端 ← Go
- 分布式 / 系统设计 ← SystemDesign、Database、云原生、TSDB、Cloud Computing
- 算法 ← Algorithm
- 面试 / 八股 ← interview、Basic Knowledge 八股、resume
- C / C++ ← C++、C language、Assembly、Linux Kernel
- Rust ← Rust
- 云原生 / DevOps ← Devops、Docker、云原生、network、Linux
- 工具 / 效率 ← Tools、Font、README、frontend、IOT、游戏开发
- 软技能 / 职业 ← SoftSkills、Books、Design Pattern、OS

> 旧列表可保留或清空，由你决定。GitHub 支持一个 star 属于多个列表，归并时无需先删旧列表。

## 五、说明

自动分类基于每个 repo 的 language / topics / description 关键词匹配，属**辅助草稿**，非 100% 准确——请在勾选时快速扫一眼确认。未命中的 181 个多为描述稀疏或跨领域项目，需人工判断。
