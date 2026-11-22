# 数据结构与算法 · 可视化教程

28 章中文课程，围绕**操作语义、正确性不变量、复杂度、可执行代码与工程权衡**组织学习路径。阅读入口：[课程首页](https://1998x-stack.github.io/data-structures-tutorial/)（须启用仓库 GitHub Pages 后可访问）。

## 现在可以学习什么

| 阶段 | 章节 | 状态 |
| --- | --- | --- |
| 核心概念 | 01 为什么要学数据结构、02 复杂度分析、03 数组与字符串 | **本轮深度图解重构** |
| 线性结构 | 04–07 | 原有课程保留，待精修 |
| 树 / 堆 / 图 | 08–13 | 原有课程保留，待精修 |
| 算法设计 | 14–18 | 原有课程保留，待精修 |
| 高级索引 | 19–22 | 原有课程保留，待精修 |
| 工程应用 | 23–28 | 原有课程保留，待精修 |

## 快速开始

打开根目录 `index.html` 即可查看**静态完整目录**。在线交互增强需要 JavaScript；页面内容、图示和导航无需联网即可阅读。也可以运行本地 HTTP 服务：

```bash
python3 -m http.server 8000
# 浏览器访问 http://localhost:8000/
```

检查内容、图示及链接：

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
│   ├── 01.html .. 03.html          # 三篇深度重构的独立文章
│   ├── 04.html .. 28.html          # 保留原内容，等待逐篇重构
│   ├── theme.css                   # 原章节专用兼容样式
│   └── index.html                  # 原章节返回首页的兼容入口
├── assets/
│   ├── css/{site,article}.css      # 首页与文章各自的样式
│   ├── js/{home,interactive}.js    # 渐进增强
│   └── svg/*.svg                   # 可独立访问的原生矢量图
├── examples/algorithms.py          # 最小可运行参考算法
├── tests/                           # 内容、文件和代码测试
├── archive/original/01.html ..     # 首批三章的原始版本
├── 01.html .. 28.html              # 老链接兼容跳转
├── AGENTS.md                       # 未来 Agent 编辑与验收契约
└── .github/workflows/site.yml      # CI 与 Pages 部署
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

工作流在 `main` 分支通过验证后可部署静态站点。需在仓库 **Settings → Pages → Build and deployment → Source** 中选择 **GitHub Actions**。工作流存在不代表网站已上线；发布后需独立检查页面和图示的 HTTP 状态。

## 内容许可与使用

本仓库内容由维护者持续修订。未在仓库中明确提供额外许可证前，不推定特定再分发许可。
