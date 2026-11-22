# AGENTS.md — 数据结构与算法课程维护规约

## 项目目标
把 28 篇中文数据结构与算法教程打磨成**每页独立、技术正确、渐进图解、可执行验证**的长期学习资源。对新读者负责，不要写“讲义介绍了……”“本讲义将提到……”替代实际解释。

## 首先检查
1. 读取 `courses.json`、`README.md`、目标 `lessons/XX.html`；调查现有示例的正确性和页面依赖。
2. 读取上游 [Olah-style Paper Posts SKILL](https://github.com/1998x-stack/Olah-style-posts/blob/main/skills/olah-style-paper-posts/SKILL.md) 及其叙事、SVG、HTML 设计、浏览器检查参考文件；遵循**理解机制 > 视觉包装**。
3. 将原章节版本留在 `archive/original/XX.html` 再替换正文。只重构指定篇数，不批量生成空壳页面。

## 文件与迁移契约
- 唯一正文路径：`lessons/01.html` … `lessons/28.html`；所有页面引用使用相对路径以支持仓库级 Pages 子路径。
- 根目录 `01.html` … `28.html` 仅作为历史 URL 跳转，切勿删除；旧章节的 `theme.css` 与 `index.html` 在 `lessons/` 留兼容版本。
- 首页静态渲染全部 28 章，`courses.json` 是课程元数据的单一来源，变更章节时同步更新；禁止依赖 `fetch` 才能出现目录。
- 公共 CSS：`assets/css/site.css` 是门户，`assets/css/article.css` 是文章；避免大量 inline CSS；JavaScript 应仅增强，不妨碍阅读。
- SVG 放 `assets/svg/NN-topic.svg`，每个图都有 `viewBox`、`title`、`desc`、唯一 ID、可靠标签和解释性图注。

## 逐篇写作规则
一篇至少有：现实或计算情境 → 问题与失败基线 → 数据组织方式和关键不变量 → 逐步图解 → 复杂度的计数依据 → 运行代码与边界测试 → 陷阱 / 适用边界 → 总结及学习衔接。章节单独打开必须自足。
必须严格区分：数学上的抽象数组 / C 定长数组 / CPython `list` 的连续引用槽；算法上界 / 最坏输入 / 平均输入 / 均摊操作；模型示意 / 精确运行指标。任何实验数值不可伪造。
代码块注明语言和必要前置条件，优先 Python 标准库，无第三方网络依赖。示例在 `examples/algorithms.py` 和 `tests/` 中同步验证；不要让文章“示例输出”与程序不一致。
交互遵循 Progressive Enhancement：静态图已解释关键关系，键盘可操作，`aria-live` 显示计算结果；减少动画并尊重 reduced-motion。

## CSS / SVG 与无障碍
- 文章 `<main><article>`、唯一 H1、可折叠目录和有序 H2/H3；可见键盘焦点和 skip link。
- 正文字号约 17px、行高 1.8、合理行宽；宽表格/代码/公式只能在自身容器滚动；不使用横向全局隐藏。
- SVG 标注最低推荐 13px，箭头必须对应真实依赖；图形的颜色有语义也要带文字，不依靠颜色辨识。
- 用原生 MathML 公式，公式较长时放可聚焦横向滚动容器；不把 MathML 放入 SVG 文本。
- 检查 1440、768、390、360 像素宽，深色模式若有，打印、键盘、JS 禁用和低动态偏好。
- 教程正文不要混入“生成说明”“制作规范”“SVG 自夸”或无依据的绝对化描述。

## 质量门禁和发布
1. `python3 tests/validate_site.py`：本地资源、首页/章节 H1、SVG XML 和 28 个旧链接。
2. `python3 -m unittest discover -s tests -p 'test_*.py'`：至少覆盖空、单、重复、负数、边界和异常。
3. 浏览器用 Playwright/Chromium 测 1440×900、768×1024、390×844、360×800；核对横向溢出、图形可读性、图片加载、交互更新、控制台报错、打印。未执行即明确写“未验证”。
4. 在 PR 上检查差异及 CI，再合并；Pages 的实际可访问性需 HTTP 验证，不得以 workflow 存在宣称上线。
5. 每批完成记录“已精修/保留原版/待复查”，不要将 28 篇都声称已升级。

## 2026-11-22 精修批次约定
- 01–08 已按新的图解体系重写；09–28 仍是原稿，不要在 README 或课程首页将其当成深度精修篇。
- 新增 04–08 原稿在 `archive/original/`；编辑者必须保留旧 URL 和课程元数据标记 `revision`。
- 本批算法的运行参考在 `examples/linear_structures.py`，测试在 `tests/test_linear_structures.py`，每篇交互演示在 `assets/js/interactive.js`，图形故事板在 `docs/design-system.md`。
- 链表必须说明“已知前驱”的操作条件；栈和队列必须区分 ADT 与实现；哈希的 O(1) 必须标明假设；普通二叉树不能被写成天然有序。
