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

## 2026-11 后续精修批次（09–11）
- 09–11（二叉搜索树、平衡二叉树、堆与优先队列）已按同一图解体系重写；12–28 仍是原稿。README 的状态表与本节必须同步更新，不得把未改章节说成已精修。
- 本批原稿存入 `archive/original/09.html`–`11.html`；`courses.json` 中这三章的 `revision` 已改为 `illustrated`，其余保持 `original`。
- 运行参考：`examples/bst.py`、`examples/balanced_trees.py`、`examples/heaps.py`；测试：`tests/test_bst.py`、`tests/test_balanced_trees.py`、`tests/test_heaps.py`。
- 必须区分：BST 的全子树区间不变量与“中序升序”推论；平衡因子用边数或节点数约定时差值相同；AVL 高度上界与红黑树高度上界出处不同；堆只保证父子序、不等于有序，建堆 O(n) 是求和论证而非实测。

## 2026-11 后续精修批次（12–13）
- 12–13（图基础、图算法）已按同一图解体系重写；14–28 仍是原稿。README 的状态表与本节必须同步更新，不得把未改章节说成已精修。
- 本批原稿存入 `archive/original/12.html`、`archive/original/13.html`；`courses.json` 中这两章的 `revision` 已改为 `illustrated`，其余保持 `original`。
- 运行参考：`examples/graphs.py`（表示与遍历）、`examples/graph_algorithms.py`（最短路/拓扑/MST）；测试：`tests/test_graphs.py`、`tests/test_graph_algorithms.py`。
- 必须区分：邻接表 O(n+m) 与邻接矩阵 O(n²) 的适用边界；DFS/BFS 只在无权图、BFS 才保证最少边数最短路；Dijkstra 仅在权重非负时正确，负权用 Bellman-Ford；拓扑排序要求有向无环图且结果不唯一；最小生成树优化全树总权重、与最短路径树目标不同。
- 图示为外链 `assets/svg/12-*.svg`、`assets/svg/13-*.svg`，与 01–11 一致（skills 自带的 `validate.py` 要求内联 `<svg>`，与本仓库外链约定冲突，此差异只在交付说明中记录）。

## 2026-11 后续精修批次（14–19）
- 14–18（排序全览、递归与分治、回溯、动态规划、贪心）与 19（并查集）已按同一图解体系重写；20–28 仍是原稿。README 的状态表与本节必须同步更新，不得把未改章节说成已精修。
- 本批原稿存入 `archive/original/14.html`–`archive/original/19.html`；`courses.json` 中这六章的 `revision` 已改为 `illustrated`，其余保持 `original`。
- 运行参考：`examples/sorting.py`、`examples/recursion.py`、`examples/backtracking.py`、`examples/dynamic_programming.py`、`examples/greedy.py`、`examples/union_find.py`；测试：`tests/test_sorting.py`、`tests/test_recursion.py`、`tests/test_backtracking.py`、`tests/test_dynamic_programming.py`、`tests/test_greedy.py`、`tests/test_union_find.py`。
- 必须区分：排序的稳定/原地性质与实测速度（同阶算法常数不同）；递归的调用深度与栈溢出风险；回溯的“撤销选择”与 DP 的“状态转移”不是同一回事；DP 要求最优子结构 + 重叠子问题同时成立；贪心只在贪心选择性质 + 最优子结构成立时正确（找零 1/3/4 是反例）；并查集的 O(α(n)) 是摊还上界，且它只支持合并、不支持断开。
- 图示为外链 `assets/svg/14-*.svg`–`assets/svg/19-*.svg`，与 01–13 一致（skills 自带的 `validate.py` 要求内联 `<svg>`，与本仓库外链约定冲突，此差异只在交付说明中记录）。

## 2026-11 后续精修批次（20–22、25–27）
- 20–22（线段树与树状数组、字典树 Trie、跳表与 B+ 树）与 25（系统设计中的数据结构）、26（数据结构性能分析）、27（AI 与数据结构的交叉）已按同一图解体系重写；23–24、28 仍是原稿。README 的状态表与本节必须同步更新，不得把未改章节说成已精修。
- 本批原稿存入 `archive/original/20.html`–`archive/original/22.html`、`archive/original/25.html`、`archive/original/26.html`、`archive/original/27.html`；`courses.json` 中这六章的 `revision` 已改为 `illustrated`，其余保持 `original`。
- 运行参考：`examples/range_queries.py`、`examples/trie.py`、`examples/skip_list.py`、`examples/benchmarking.py`、`examples/learned_index.py`、`examples/system_design.py`；测试：`tests/test_range_queries.py`、`tests/test_trie.py`、`tests/test_skip_list.py`、`tests/test_benchmarking.py`、`tests/test_learned_index.py`、`tests/test_system_design.py`。
- 必须区分：线段树/树状数组的 O(log n) 与“实测耗时”（同阶常数不同）；Trie 的“前缀存在”与“完整词存在”（靠 is_end 区分）；跳表的 O(log n) 是期望而非最坏保证；B+ 树优势来自“多 key/页 + 叶链”而非渐进复杂度更低。
- 性能与 AI 章节：硬件数量级（内存/缓存/磁盘）须标注“教学示意”，不得编造“实测”数字或来源；学习型索引的预测是近似，ANN 不保证精确最近邻。
- 图示为外链 `assets/svg/20-*.svg`、`assets/svg/21-*.svg`、`assets/svg/22-*.svg`、`assets/svg/25-*.svg`、`assets/svg/26-*.svg`、`assets/svg/27-*.svg`，与 01–19 一致。

## 2026-11 后续精修批次（23、24、28，收尾）
- 23（LeetCode 刷题方法论）、24（大厂面试高频题精讲）、28（学习路线与综合项目）已按同一图解体系重写；至此 28 章全部为 `illustrated`。README 的状态表与本节同步更新。
- 本批原稿存入 `archive/original/23.html`、`archive/original/24.html`、`archive/original/28.html`；`courses.json` 中这三章的 `revision` 已改为 `illustrated`。
- 运行参考：`examples/study_patterns.py`（反转链表、两数之和、间隔复习排期）、`examples/interview_problems.py`（15 道高频题）、`examples/mini_redis.py`（跳表 + TTL + AOF）；测试：`tests/test_study_patterns.py`、`tests/test_interview_problems.py`、`tests/test_mini_redis.py`。
- 必须区分：方法论章的“刷够 N 题就稳”“命中率 X%”等无来源数字须标注为教学示意或删除；面试章中两数之和的 O(1) 查找是平均复杂度；反转链表迭代 O(1) 空间 / 递归 O(n) 调用栈；岛屿数量 DFS 的最坏递归栈为 O(m·n)（不是 O(min(m,n))）；LIS 的 tails 数组不是某个具体子序列；跳表的 O(log n) 是期望而非最坏保证；TTL 用“最小堆 + 惰性删除”，过期时间被重设时靠 ttl_map 比对避免误删。
- 图示为外链 `assets/svg/23-*.svg`、`assets/svg/24-*.svg`、`assets/svg/28-*.svg`，与 01–22、25–27 一致。
- 交付说明：skills 自带的 `validate.py` 要求内联 `<svg>`，与本仓库外链 SVG 约定冲突，故其报 “No SVG illustrations” 属已知差异；仓库自带的 `tests/validate_site.py` 通过。
