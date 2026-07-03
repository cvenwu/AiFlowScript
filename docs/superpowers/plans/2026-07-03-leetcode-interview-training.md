# LeetCode Interview Training Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a reusable 12-week LeetCode interview training package under `learning-resources/leetcode-interview-training/`.

**Architecture:** The package is documentation-first. `README.md` explains the training system, `12-week-calendar.md` gives the day-by-day execution order, `progress-tracker.md` tracks weekly and daily completion, and `problem-note-template.md` standardizes per-problem review notes. The package is independent from code projects and does not add runtime dependencies.

**Tech Stack:** Markdown, LeetCode 中文网, Python for primary solutions, Go for weekly high-frequency rewrites, Git.

## Global Constraints

- 训练周期：12 周。
- 工作日投入：每天 60-90 分钟。
- 周末投入：每天 2-3 小时。
- 主刷语言：Python，用于提高表达速度和适配 AI 应用岗位。
- 辅助语言：Go，每周选择 1-2 道高频题复写，用于保持后端岗位手感。
- 题量目标：核心题 90-100 道，加强题 30-40 道，模拟面试题 10-15 道。
- 如果实际时间不足，优先保证每周 P0 题和错题二刷，不追求完成所有加强题。
- 每道题完成后记录题型标签、核心不变量、复杂度和面试复述。
- 错题按 1 / 3 / 7 / 14 天复刷。

---

## File Structure

- Create `learning-resources/leetcode-interview-training/README.md`: training overview, weekly rhythm, role branches, success criteria.
- Create `learning-resources/leetcode-interview-training/12-week-calendar.md`: Day 1 to Day 84 execution calendar.
- Create `learning-resources/leetcode-interview-training/progress-tracker.md`: weekly checklist and review metrics.
- Create `learning-resources/leetcode-interview-training/problem-note-template.md`: per-problem note template.

### Task 1: Training Package Overview

**Files:**
- Create: `learning-resources/leetcode-interview-training/README.md`

**Interfaces:**
- Consumes: `docs/superpowers/specs/2026-07-03-leetcode-interview-training-design.md`
- Produces: A human-readable entry point that links to the calendar, tracker, and note template.

- [ ] **Step 1: Create the overview file**

Create `learning-resources/leetcode-interview-training/README.md` with:

```markdown
# LeetCode 多岗位面试刷题训练

这是一套 12 周算法训练计划，用于同时准备后端研发、AI Agent 应用工程师、AI Harness / 基础架构方向的技术面试。

计划以 LeetCode 中文网为主要刷题平台。训练目标不是追求题量最大化，而是形成稳定的题型识别、模板迁移、复杂度分析和面试复述能力。

## 文件说明

- `12-week-calendar.md`：第 1 天到第 84 天的刷题顺序。
- `progress-tracker.md`：每周进度、错题二刷、模拟面试记录。
- `problem-note-template.md`：每道题的复盘模板。

## 训练节奏

| 时间 | 训练内容 | 目标 |
|---|---|---|
| 周一 | 学模板 + 2 道基础题 | 建立本周题型框架 |
| 周二 | 2 道同类变形题 | 识别输入变化和边界条件 |
| 周三 | 2 道中等题 | 独立完成主干逻辑 |
| 周四 | 1 道中等题 + 1 道错题 | 提高稳定性 |
| 周五 | 1 道综合题 + 本周总结 | 形成可复述模板 |
| 周六 | 岗位分支题 2-3 道 | 面向后端、AI 应用、Harness 加强 |
| 周日 | 错题二刷 + 45 分钟模拟 | 检查表达和限时能力 |

## 训练原则

### 题型优先

刷题顺序按题型能力递进，不按 LeetCode 热度榜顺刷。多岗位面试共用一套算法底座，先建立「看到题能归类」的能力，比随机刷题更重要。

### 共用底座 + 岗位分支

周一到周五训练共同题型：

- 数组、字符串、哈希
- 双指针、滑动窗口
- 栈、队列、链表、二分
- 树、DFS、BFS、回溯
- 图、拓扑排序、并查集
- 堆、TopK、贪心、动态规划

周六按目标岗位做分支加强：

- 后端研发：缓存、TopK、二分、链表、堆、设计类题。
- AI Agent 应用：字符串、滑动窗口、矩阵搜索、Trie、TopK、检索排序。
- AI Harness / Infra：图、拓扑排序、状态搜索、优先队列、调度类题。

### 每题固定产出

每道题完成后记录 4 项内容：

- 题型标签：例如「滑动窗口」「拓扑排序」「树形 DP」。
- 核心不变量：例如窗口内始终满足什么条件。
- 复杂度：时间复杂度和空间复杂度。
- 面试复述：用 1-2 分钟讲清思路和边界条件。

## 成功标准

12 周结束时应达到以下状态：

- 能独立完成 80% 的 Easy / Medium 高频题。
- 对数组、哈希、滑动窗口、链表、树、图、堆、DP 有稳定模板。
- 能在 45 分钟内完成 1 道 Medium，并讲清复杂度。
- 能把算法题和后端、AI 应用、Harness 面试问题建立类比。
- 至少完成 30 道错题二刷。
```

- [ ] **Step 2: Verify the overview file**

Run:

```bash
rg -n "TB[D]|TO[D]O|待[定]|PLACE[H]OLDER" learning-resources/leetcode-interview-training/README.md
```

Expected: no output.

- [ ] **Step 3: Commit Task 1**

Run:

```bash
git add learning-resources/leetcode-interview-training/README.md
git commit -m "docs: add leetcode training overview"
```

Expected: commit succeeds with only `README.md` staged.

### Task 2: Day 1-28 Calendar

**Files:**
- Create: `learning-resources/leetcode-interview-training/12-week-calendar.md`

**Interfaces:**
- Consumes: Training overview from Task 1.
- Produces: The first 4 weeks of the execution calendar.

- [ ] **Step 1: Create the calendar file with weeks 1-4**

Create `learning-resources/leetcode-interview-training/12-week-calendar.md` with:

```markdown
# 12 周刷题日历

## 使用方式

- 每天按「当日题目 -> 复述 -> 记录」执行。
- 标记为「Go 复写」的题，先用 Python AC，再用 Go 复写核心逻辑。
- 周日不追求新题数量，优先完成错题二刷和 45 分钟模拟。
- 如果某天时间不足，保留 P0 题，分支题顺延到周六或周日。

## 第 1 周：数组、字符串、哈希

目标：建立最基础的数据定位和计数能力。

| 天数 | 任务 | 题目 |
|---|---|---|
| Day 1 | 哈希入门 | 1. 两数之和；217. 存在重复元素 |
| Day 2 | 字符计数 | 242. 有效的字母异位词；49. 字母异位词分组 |
| Day 3 | 集合与原地数组 | 128. 最长连续序列；283. 移动零 |
| Day 4 | 前后缀数组 + 错题复查 | 238. 除自身以外数组的乘积；复查 Day 1 任意 1 题 |
| Day 5 | 周总结 + Go 复写 | Go 复写 1. 两数之和；复述 49. 字母异位词分组 |
| Day 6 | 岗位分支 | 后端：560. 和为 K 的子数组；AI 应用：387. 字符串中的第一个唯一字符；Harness：705. 设计哈希集合 |
| Day 7 | 错题二刷 + 模拟 | 二刷本周 2 道错题；45 分钟模拟：128. 最长连续序列 |

## 第 2 周：双指针、滑动窗口

目标：掌握「左右边界移动」和「窗口内状态维护」。

| 天数 | 任务 | 题目 |
|---|---|---|
| Day 8 | 对撞指针 | 125. 验证回文串；167. 两数之和 II - 输入有序数组 |
| Day 9 | 双指针枚举 | 15. 三数之和；11. 盛最多水的容器 |
| Day 10 | 滑动窗口基础 | 3. 无重复字符的最长子串；209. 长度最小的子数组 |
| Day 11 | 固定窗口与计数 | 438. 找到字符串中所有字母异位词；567. 字符串的排列 |
| Day 12 | 周总结 + Go 复写 | Go 复写 3. 无重复字符的最长子串；复述 15. 三数之和 |
| Day 13 | 岗位分支 | 后端：42. 接雨水；AI 应用：76. 最小覆盖子串；Harness：904. 水果成篮 |
| Day 14 | 错题二刷 + 模拟 | 二刷本周 2 道错题；45 分钟模拟：76. 最小覆盖子串 |

## 第 3 周：栈、队列、前缀和

目标：掌握括号匹配、表达式求值、队列模拟和区间和。

| 天数 | 任务 | 题目 |
|---|---|---|
| Day 15 | 栈基础 | 20. 有效的括号；155. 最小栈 |
| Day 16 | 栈队列互转 | 232. 用栈实现队列；225. 用队列实现栈 |
| Day 17 | 表达式与前缀和 | 150. 逆波兰表达式求值；303. 区域和检索 - 数组不可变 |
| Day 18 | 前缀和 + 哈希 | 560. 和为 K 的子数组；二刷 Day 15 任意 1 题 |
| Day 19 | 周总结 + Go 复写 | Go 复写 155. 最小栈；复述 560. 和为 K 的子数组 |
| Day 20 | 岗位分支 | 后端：622. 设计循环队列；AI 应用：239. 滑动窗口最大值；Harness：735. 行星碰撞 |
| Day 21 | 错题二刷 + 模拟 | 二刷本周 2 道错题；45 分钟模拟：239. 滑动窗口最大值 |

## 第 4 周：链表、二分查找

目标：掌握指针变化、边界收敛和有序空间搜索。

| 天数 | 任务 | 题目 |
|---|---|---|
| Day 22 | 链表基础 | 206. 反转链表；21. 合并两个有序链表 |
| Day 23 | 快慢指针 | 141. 环形链表；142. 环形链表 II |
| Day 24 | 链表定位 | 876. 链表的中间结点；19. 删除链表的倒数第 N 个结点 |
| Day 25 | 二分基础 | 704. 二分查找；35. 搜索插入位置；34. 在排序数组中查找元素的第一个和最后一个位置 |
| Day 26 | 旋转数组 + Go 复写 | 33. 搜索旋转排序数组；153. 寻找旋转排序数组中的最小值；Go 复写 206. 反转链表 |
| Day 27 | 岗位分支 | 后端：146. LRU 缓存；AI 应用：74. 搜索二维矩阵；Harness：162. 寻找峰值 |
| Day 28 | 错题二刷 + 阶段模拟 | 二刷前 4 周 3 道错题；45 分钟模拟：33. 搜索旋转排序数组 |
```

- [ ] **Step 2: Verify weeks 1-4 are present**

Run:

```bash
rg -n "Day 1|Day 14|Day 28|第 4 周" learning-resources/leetcode-interview-training/12-week-calendar.md
```

Expected: all four patterns appear.

- [ ] **Step 3: Commit Task 2**

Run:

```bash
git add learning-resources/leetcode-interview-training/12-week-calendar.md
git commit -m "docs: add first month leetcode calendar"
```

Expected: commit succeeds with only `12-week-calendar.md` staged.

### Task 3: Day 29-56 Calendar

**Files:**
- Modify: `learning-resources/leetcode-interview-training/12-week-calendar.md`

**Interfaces:**
- Consumes: Calendar file from Task 2.
- Produces: Weeks 5-8 appended to the same calendar.

- [ ] **Step 1: Append weeks 5-8**

Append this content to `learning-resources/leetcode-interview-training/12-week-calendar.md`:

```markdown

## 第 5 周：二叉树基础

目标：建立递归遍历、层序遍历和二叉搜索树判断能力。

| 天数 | 任务 | 题目 |
|---|---|---|
| Day 29 | 树递归基础 | 104. 二叉树的最大深度；100. 相同的树 |
| Day 30 | 结构变换 | 226. 翻转二叉树；101. 对称二叉树 |
| Day 31 | 深度与路径 | 543. 二叉树的直径；110. 平衡二叉树；112. 路径总和 |
| Day 32 | 层序遍历 | 102. 二叉树的层序遍历；199. 二叉树的右视图 |
| Day 33 | BST + Go 复写 | 98. 验证二叉搜索树；230. 二叉搜索树中第 K 小的元素；Go 复写 104. 二叉树的最大深度 |
| Day 34 | 岗位分支 | 后端：236. 二叉树的最近公共祖先；AI 应用：105. 从前序与中序遍历序列构造二叉树；Harness：297. 二叉树的序列化与反序列化 |
| Day 35 | 错题二刷 + 模拟 | 二刷本周 2 道错题；45 分钟模拟：236. 二叉树的最近公共祖先 |

## 第 6 周：DFS、BFS、回溯

目标：把树上的搜索迁移到矩阵、集合和组合空间。

| 天数 | 任务 | 题目 |
|---|---|---|
| Day 36 | 矩阵 DFS | 200. 岛屿数量；695. 岛屿的最大面积 |
| Day 37 | 矩阵 BFS | 994. 腐烂的橘子；79. 单词搜索 |
| Day 38 | 枚举空间 | 46. 全排列；78. 子集 |
| Day 39 | 组合搜索 | 77. 组合；39. 组合总和 |
| Day 40 | 剪枝 + Go 复写 | 40. 组合总和 II；22. 括号生成；Go 复写 200. 岛屿数量 |
| Day 41 | 岗位分支 | 后端：127. 单词接龙；AI 应用：17. 电话号码的字母组合；Harness：51. N 皇后 |
| Day 42 | 错题二刷 + 模拟 | 二刷本周 2 道错题；45 分钟模拟：79. 单词搜索 |

## 第 7 周：图、拓扑排序、并查集

目标：掌握依赖关系建模、连通性判断和任务调度。

| 天数 | 任务 | 题目 |
|---|---|---|
| Day 43 | 拓扑排序 | 207. 课程表；210. 课程表 II |
| Day 44 | 图遍历 | 133. 克隆图；841. 钥匙和房间 |
| Day 45 | 连通性 | 547. 省份数量；684. 冗余连接 |
| Day 46 | 并查集应用 | 721. 账户合并；785. 判断二分图 |
| Day 47 | 周总结 + Go 复写 | Go 复写 207. 课程表；复述 721. 账户合并 |
| Day 48 | 岗位分支 | 后端：399. 除法求值；AI 应用：797. 所有可能的路径；Harness：743. 网络延迟时间 |
| Day 49 | 错题二刷 + 模拟 | 二刷本周 2 道错题；45 分钟模拟：207. 课程表 |

## 第 8 周：堆、TopK、排序、区间

目标：掌握优先级处理、TopK 和区间合并。

| 天数 | 任务 | 题目 |
|---|---|---|
| Day 50 | TopK 基础 | 215. 数组中的第 K 个最大元素；347. 前 K 个高频元素 |
| Day 51 | TopK 字符串与数据流 | 692. 前 K 个高频单词；703. 数据流中的第 K 大元素 |
| Day 52 | 堆应用 | 973. 最接近原点的 K 个点；56. 合并区间 |
| Day 53 | 区间处理 | 57. 插入区间；435. 无重叠区间 |
| Day 54 | 贪心区间 + Go 复写 | 452. 用最少数量的箭引爆气球；Go 复写 347. 前 K 个高频元素 |
| Day 55 | 岗位分支 | 后端：295. 数据流的中位数；AI 应用：208. 实现 Trie；Harness：23. 合并 K 个升序链表 |
| Day 56 | 错题二刷 + 阶段模拟 | 二刷第 5-8 周 3 道错题；45 分钟模拟：215. 数组中的第 K 个最大元素 |
```

- [ ] **Step 2: Verify weeks 5-8 are present**

Run:

```bash
rg -n "Day 29|Day 42|Day 56|第 8 周" learning-resources/leetcode-interview-training/12-week-calendar.md
```

Expected: all four patterns appear.

- [ ] **Step 3: Commit Task 3**

Run:

```bash
git add learning-resources/leetcode-interview-training/12-week-calendar.md
git commit -m "docs: add middle leetcode calendar"
```

Expected: commit succeeds with only `12-week-calendar.md` staged.

### Task 4: Day 57-84 Calendar

**Files:**
- Modify: `learning-resources/leetcode-interview-training/12-week-calendar.md`

**Interfaces:**
- Consumes: Calendar file from Tasks 2 and 3.
- Produces: Complete Day 1-84 execution calendar.

- [ ] **Step 1: Append weeks 9-12**

Append this content to `learning-resources/leetcode-interview-training/12-week-calendar.md`:

```markdown

## 第 9 周：贪心、单调栈

目标：掌握局部选择、区间决策和单调结构。

| 天数 | 任务 | 题目 |
|---|---|---|
| Day 57 | 股票与局部最优 | 121. 买卖股票的最佳时机；122. 买卖股票的最佳时机 II |
| Day 58 | 跳跃与覆盖 | 55. 跳跃游戏；45. 跳跃游戏 II |
| Day 59 | 环形与区间 | 134. 加油站；763. 划分字母区间 |
| Day 60 | 单调栈基础 | 739. 每日温度；496. 下一个更大元素 I |
| Day 61 | 单调栈变形 + Go 复写 | 503. 下一个更大元素 II；Go 复写 121. 买卖股票的最佳时机 |
| Day 62 | 岗位分支 | 后端：84. 柱状图中最大的矩形；AI 应用：316. 去除重复字母；Harness：402. 移掉 K 位数字 |
| Day 63 | 错题二刷 + 模拟 | 二刷本周 2 道错题；45 分钟模拟：739. 每日温度 |

## 第 10 周：动态规划基础

目标：掌握状态定义、转移方程和滚动数组优化。

| 天数 | 任务 | 题目 |
|---|---|---|
| Day 64 | 一维 DP | 70. 爬楼梯；746. 使用最小花费爬楼梯 |
| Day 65 | 打家劫舍 | 198. 打家劫舍；213. 打家劫舍 II |
| Day 66 | 完全背包 | 322. 零钱兑换；518. 零钱兑换 II |
| Day 67 | 序列与路径 | 139. 单词拆分；300. 最长递增子序列 |
| Day 68 | 网格 DP + Go 复写 | 62. 不同路径；64. 最小路径和；Go 复写 322. 零钱兑换 |
| Day 69 | 岗位分支 | 后端：337. 打家劫舍 III；AI 应用：152. 乘积最大子数组；Harness：279. 完全平方数 |
| Day 70 | 错题二刷 + 模拟 | 二刷本周 2 道错题；45 分钟模拟：300. 最长递增子序列 |

## 第 11 周：动态规划进阶、字符串综合

目标：训练子序列、编辑距离、回文和字符串处理。

| 天数 | 任务 | 题目 |
|---|---|---|
| Day 71 | 子序列 DP | 1143. 最长公共子序列；72. 编辑距离 |
| Day 72 | 回文问题 | 5. 最长回文子串；647. 回文子串 |
| Day 73 | 背包变形 | 416. 分割等和子集；494. 目标和 |
| Day 74 | 矩阵与字符串 | 221. 最大正方形；14. 最长公共前缀 |
| Day 75 | 字符串综合 + Go 复写 | 151. 反转字符串中的单词；Go 复写 1143. 最长公共子序列 |
| Day 76 | 岗位分支 | 后端：309. 买卖股票的最佳时机含冷冻期；AI 应用：28. 找出字符串中第一个匹配项的下标；Harness：10. 正则表达式匹配 |
| Day 77 | 错题二刷 + 模拟 | 二刷本周 2 道错题；45 分钟模拟：72. 编辑距离 |

## 第 12 周：综合模拟、设计类题

目标：完成限时训练和岗位化表达。

| 天数 | 任务 | 题目 |
|---|---|---|
| Day 78 | 缓存设计 | 146. LRU 缓存；380. O(1) 时间插入、删除和获取随机元素 |
| Day 79 | Trie 设计 | 208. 实现 Trie；211. 添加与搜索单词 - 数据结构设计 |
| Day 80 | 数据流与序列化 | 295. 数据流的中位数；297. 二叉树的序列化与反序列化 |
| Day 81 | 表达式解析 | 224. 基本计算器；227. 基本计算器 II |
| Day 82 | 综合 Go 复写 | Go 复写 146. LRU 缓存；Go 复写 208. 实现 Trie |
| Day 83 | 岗位分支 | 后端：460. LFU 缓存；AI 应用：212. 单词搜索 II；Harness：355. 设计推特 |
| Day 84 | 终局模拟 + 复盘 | 45 分钟模拟 2 轮；整理 12 周错题 Top 10；整理岗位化复述材料 |
```

- [ ] **Step 2: Verify Day 1-84 coverage**

Run:

```bash
rg -n "Day 1|Day 28|Day 56|Day 84|第 12 周" learning-resources/leetcode-interview-training/12-week-calendar.md
```

Expected: all five patterns appear.

- [ ] **Step 3: Commit Task 4**

Run:

```bash
git add learning-resources/leetcode-interview-training/12-week-calendar.md
git commit -m "docs: complete leetcode training calendar"
```

Expected: commit succeeds with only `12-week-calendar.md` staged.

### Task 5: Progress Tracker And Problem Note Template

**Files:**
- Create: `learning-resources/leetcode-interview-training/progress-tracker.md`
- Create: `learning-resources/leetcode-interview-training/problem-note-template.md`

**Interfaces:**
- Consumes: Complete calendar from Task 4.
- Produces: Reusable tracking and review files for daily execution.

- [ ] **Step 1: Create the progress tracker**

Create `learning-resources/leetcode-interview-training/progress-tracker.md` with:

```markdown
# 刷题进度追踪

## 总进度

| 指标 | 目标 | 当前 |
|---|---:|---:|
| 核心题 | 90-100 | 0 |
| 加强题 | 30-40 | 0 |
| 模拟面试题 | 10-15 | 0 |
| 错题二刷 | 30 | 0 |
| Go 复写 | 12-24 | 0 |

## 周进度

| 周 | 主题 | 完成 P0 题 | 完成分支题 | 错题二刷 | 模拟面试 | 周总结 |
|---|---|---:|---:|---:|---:|---|
| 第 1 周 | 数组、字符串、哈希 | 0 | 0 | 0 | 0 | 未完成 |
| 第 2 周 | 双指针、滑动窗口 | 0 | 0 | 0 | 0 | 未完成 |
| 第 3 周 | 栈、队列、前缀和 | 0 | 0 | 0 | 0 | 未完成 |
| 第 4 周 | 链表、二分查找 | 0 | 0 | 0 | 0 | 未完成 |
| 第 5 周 | 二叉树基础 | 0 | 0 | 0 | 0 | 未完成 |
| 第 6 周 | DFS、BFS、回溯 | 0 | 0 | 0 | 0 | 未完成 |
| 第 7 周 | 图、拓扑排序、并查集 | 0 | 0 | 0 | 0 | 未完成 |
| 第 8 周 | 堆、TopK、排序、区间 | 0 | 0 | 0 | 0 | 未完成 |
| 第 9 周 | 贪心、单调栈 | 0 | 0 | 0 | 0 | 未完成 |
| 第 10 周 | 动态规划基础 | 0 | 0 | 0 | 0 | 未完成 |
| 第 11 周 | 动态规划进阶、字符串综合 | 0 | 0 | 0 | 0 | 未完成 |
| 第 12 周 | 综合模拟、设计类题 | 0 | 0 | 0 | 0 | 未完成 |

## 每日记录

| 日期 | Day | 题目 | 是否 AC | 是否复述 | 错因 | 下次复刷日期 |
|---|---:|---|---|---|---|---|
|  | 1 | 1. 两数之和 | 否 | 否 |  |  |
|  | 1 | 217. 存在重复元素 | 否 | 否 |  |  |

## 每周复盘问题

- 本周最稳定的题型是什么？
- 本周最容易误判的题型是什么？
- 哪道题可以类比到后端系统设计？
- 哪道题可以类比到 AI Agent / RAG / Harness？
- 下周需要提前复习哪个模板？
```

- [ ] **Step 2: Create the problem note template**

Create `learning-resources/leetcode-interview-training/problem-note-template.md` with:

```markdown
# 单题复盘模板

## 题目

- 编号：
- 名称：
- 难度：
- 题型：
- 首次完成日期：
- 最近复刷日期：

## 思路

- 关键观察：
- 核心不变量：
- 边界条件：

## 复杂度

- 时间复杂度：
- 空间复杂度：

## 面试复述

1. 先说明为什么选择这个数据结构或算法。
2. 再说明状态如何变化。
3. 最后说明复杂度和边界条件。

## 错因

- 首次错误：
- 修复方式：
- 下次遇到同类题的识别信号：

## 岗位类比

- 后端研发：
- AI Agent 应用：
- AI Harness / Infra：
```

- [ ] **Step 3: Verify tracker and template**

Run:

```bash
rg -n "总进度|每周复盘问题|岗位类比|核心不变量" learning-resources/leetcode-interview-training/progress-tracker.md learning-resources/leetcode-interview-training/problem-note-template.md
```

Expected: all four patterns appear.

- [ ] **Step 4: Commit Task 5**

Run:

```bash
git add learning-resources/leetcode-interview-training/progress-tracker.md learning-resources/leetcode-interview-training/problem-note-template.md
git commit -m "docs: add leetcode training tracker"
```

Expected: commit succeeds with only the tracker and template staged.

### Task 6: Final Documentation Verification

**Files:**
- Verify: `learning-resources/leetcode-interview-training/README.md`
- Verify: `learning-resources/leetcode-interview-training/12-week-calendar.md`
- Verify: `learning-resources/leetcode-interview-training/progress-tracker.md`
- Verify: `learning-resources/leetcode-interview-training/problem-note-template.md`

**Interfaces:**
- Consumes: Tasks 1-5.
- Produces: Verified documentation package ready for daily training.

- [ ] **Step 1: Confirm all files exist**

Run:

```bash
test -f learning-resources/leetcode-interview-training/README.md
test -f learning-resources/leetcode-interview-training/12-week-calendar.md
test -f learning-resources/leetcode-interview-training/progress-tracker.md
test -f learning-resources/leetcode-interview-training/problem-note-template.md
```

Expected: all commands exit with status 0.

- [ ] **Step 2: Scan for plan red flags**

Run:

```bash
rg -n "TB[D]|TO[D]O|待[定]|PLACE[H]OLDER|implement [l]ater|fill in [d]etails" learning-resources/leetcode-interview-training
```

Expected: no output.

- [ ] **Step 3: Confirm calendar coverage**

Run:

```bash
rg -n "Day 1|Day 14|Day 28|Day 42|Day 56|Day 70|Day 84" learning-resources/leetcode-interview-training/12-week-calendar.md
```

Expected: all seven patterns appear.

- [ ] **Step 4: Confirm scoped git status**

Run:

```bash
git status --short learning-resources/leetcode-interview-training docs/superpowers/plans/2026-07-03-leetcode-interview-training.md
```

Expected: no unstaged changes after the final task commits, except this plan file if it has not been committed yet.

- [ ] **Step 5: Commit this implementation plan if needed**

Run:

```bash
git add docs/superpowers/plans/2026-07-03-leetcode-interview-training.md
git commit -m "docs: add leetcode training implementation plan"
```

Expected: commit succeeds with only the plan file staged.
