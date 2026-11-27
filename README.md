# 数据结构与算法 · 可视化教程

28 章中文课程，围绕**操作语义、正确性不变量、复杂度、可执行代码与工程权衡**组织学习路径。阅读入口：[课程首页](https://1998x-stack.github.io/data-structures-tutorial/)（须启用仓库 GitHub Pages 后可访问）。

## 现在可以学习什么

| 阶段 | 章节 | 状态 |
| --- | --- | --- |
| 核心概念 | 01–03：结构选择、复杂度、数组与字符串 | **已精修** |
| 线性结构 | 04–07：链表、栈、队列、哈希表与 LRU | **本批深度图解重构** |
| 树 / 堆 / 图 | 08：树基础与四种遍历 | **已精修** |
| 树 / 堆 / 图 | 09–11：二叉搜索树、平衡二叉树、堆与优先队列 | **本批深度图解重构** |
| 树 / 堆 / 图 | 12：图基础 | **本批深度图解重构** |
| 树 / 堆 / 图 | 13：图算法 | **本批深度图解重构** |
| 算法设计 | 14–18：排序、递归分治、回溯、动态规划、贪心 | **本批深度图解重构** |
| 高级索引 | 19：并查集 | **本批深度图解重构** |
| 高级索引 | 20：线段树与树状数组 | **本批深度图解重构** |
| 高级索引 | 21：字典树（Trie） | **本批深度图解重构** |
| 高级索引 | 22：跳表与 B+ 树 | **本批深度图解重构** |
| 工程应用 | 25：系统设计中的数据结构 | **本批深度图解重构** |
| 工程应用 | 26：数据结构性能分析 | **本批深度图解重构** |
| 工程应用 | 27：AI 与数据结构的交叉 | **本批深度图解重构** |
| 工程应用 | 23：LeetCode 刷题方法论 | **本批深度图解重构** |
| 工程应用 | 24：大厂面试高频题精讲 | **本批深度图解重构** |
| 工程应用 | 28：学习路线与综合项目 | **本批深度图解重构** |

## 快速开始

打开根目录 `index.html` 即可查看**静态完整目录**。在线交互增强需要 JavaScript；页面内容、图示和导航无需联网即可阅读。也可以运行本地 HTTP 服务：

```bash
python3 -m http.server 8000
# 浏览器访问 http://localhost:8000/
```

检查内容、图示及链接（浏览器验收由 GitHub Actions 自动执行）：

```bash
python3 tests/validate_site.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

## 仓库结构

```text
.
├── index.html                      # GitHub Pages / 课程首页
├── courses.json                    # 28 章机器可读课程清单
├── lessons/
│   ├── 01.html .. 22.html          # 深度重构文章（01–19 及 20–22）
│   ├── 23.html, 24.html            # 深度重构（刷题方法论、面试高频题）
│   ├── 25.html, 26.html, 27.html    # 深度重构（系统设计、性能分析、AI 交叉）
│   ├── 28.html                      # 深度重构（学习路线与 MiniRedis 项目）
│   ├── theme.css                   # 原章节专用兼容样式
│   └── index.html                  # 原章节返回首页的兼容入口
├── assets/
│   ├── css/{site,article}.css      # 首页与文章各自的样式
│   ├── js/{home,interactive}.js    # 渐进增强
│   └── svg/*.svg                   # 可独立访问的原生矢量图
├── examples/{algorithms,linear_structures,bst,balanced_trees,heaps,graphs,graph_algorithms,sorting,recursion,backtracking,dynamic_programming,greedy,union_find,range_queries,trie,skip_list,benchmarking,learned_index,system_design}.py # 可运行参考算法
├── tests/                           # 内容、文件和代码测试
├── archive/original/01.html .. 22.html、25.html .. 27.html # 改写前的原始版本
├── 01.html .. 28.html              # 老链接兼容跳转
├── AGENTS.md                       # 未来 Agent 编辑与验收契约
└── .github/workflows/site.yml      # CI、浏览器质量门禁
```

**迁移政策：**任何原始章节的主要内容都不会静默丢失。根目录 `01.html`–`28.html` 永久转向 `lessons/`；旧章节内的相对链接和样式仍有效。改造完整篇章时先保存原始稿，再替换目标 `lessons/XX.html`。

## 教学编辑原则

- 章节必须自足：不假定读者看过其他网页，首次出现的概念需给出语境、定义和例子。
- 一幅 SVG 回答一个具体问题：给出节点/数据流、可核查的标题、说明和图注；不把装饰性插图当作解释。
- 用明确定义的输入规模和操作模型分析复杂度，区分最坏、平均、均摊；不要混淆 Python 对象模型和 C 连续数值数组。
- 可运行代码必须覆盖边界测试，并区分教学简化与实现约束。
- 参考了 [Olah-style-posts](https://github.com/1998x-stack/Olah-style-posts/tree/main/skills/olah-style-paper-posts) 的叙事与图解设计规范，未复制其图文资产。
- 详细工作流参见 [AGENTS.md](AGENTS.md)。

## GitHub Pages

仓库已有 GitHub Pages 的 `pages build and deployment` 历史记录。本轮保留原有 Pages 来源设置，`site.yml` **仅运行质量检查**，不在未知配置下另建一个竞争的部署任务。合并到 `main` 后仍由仓库现有 Pages 配置负责发布；发布完成需独立检查首页、章节和 SVG 的实际 HTTP 状态。

## 内容许可与使用

本仓库内容由维护者持续修订。未在仓库中明确提供额外许可证前，不推定特定再分发许可。
