# 第一批技术事实交叉校验

> 本文件是维护记录，不出现在读者正文的主视觉区域。

## 第 01 章
- 区分 ADT 与实现，强调链表表头已知、数组下标访问、哈希表期望复杂度、平衡 BST 的前提。
- 图 `01-structures.svg` 展示结构拓扑，不假定 CPython 对象内存布局；`01-tradeoffs.svg` 每一格给出操作前提。
- 主要延伸：MIT 6.006 数据结构讲义；Python 标准库 Data Structures。
- 仍需复查：后续 04–28 章的术语一致性及引用。

## 第 02 章
- `T(n)∈O(g(n))` 为渐进上界；`Θ` 才是上下界同阶。
- 容量翻倍是说明均摊分析的示意模型，**不是 CPython 的真实增长比例**。
- `02-growth.svg` 仅显示数学函数值；禁止改写为声称测得的 CPU 时延。
- 来源：MIT 6.006 课程笔记，Python 官方 `timeit` 文档。

## 第 03 章
- Python 官方 FAQ 明确：list 使用连续的对象引用数组；不能写成 Python 整数本体连续。
- 左闭右开 `[l,r)` 与 `P[r]-P[l]` 精确对应，允许负数。
- 前缀和 + 哈希必须先查 `prefix-k` 再登记当前 `prefix`，避免空子数组误计。
- 双指针两数之和示例假定输入升序；带负数的窗口和条件不能直接套单调缩窗。
- Unicode 字符串按码点计长度，和用户感知的字素簇不同。
- 来源：Python Design FAQ、Unicode HOWTO，MIT 6.006。

## 质量边界
- `tests/test_algorithms.py` 检查算法正确性、空输入、重复、负数与小规模穷举。
- `tests/validate_site.py` 检查完整路径、链接、H1 和 SVG 解析。
- 此记录不替代 Chromium 的移动端、打印、键盘和交互验收；它们必须另行执行和记录。

## 第二批：04–08 章

| 章节 | 已检查的关键语义 | 主参考 | 边界用例 |
| --- | --- | --- | --- |
| 04 链表 | 操作 O(1) 必须已定位；哨兵统一删除；先保存 nxt 再反转；环用节点身份而非值比较 | MIT 6.006 Sequence Data Structures | 空、单、连续删除、重复值、入口成环 |
| 05 栈 | LIFO 属于 ADT；括号必须匹配嵌套次序；单调栈的严格比较；直方图虚拟哨兵不变更用户输入 | Python Data Structures、MIT 6.006 | 空栈、非法右括号、同温度、全零柱 |
| 06 队列 | 环形队列 front/rear/size 准确定义；候选索引入/出至多一次；BFS 最短边数仅针对无权模型 | Python collections.deque、MIT 6.006 | 回绕、满/空、重复窗口值、有环与非连通图 |
| 07 哈希 | 链/开放寻址分开；完整键比较；平均/期望与均摊区别；LRU 的访问排序不等于字典插入排序 | Python dict、Data Model、OrderedDict、MIT 6.006 | 冲突、负键、重复键、容量1、访问更新 |
| 08 树 | 边数高度约定；普通二叉树不保证 BST 有序；递归列表拼接可能 O(n²)；DFS/BFS 空间依赖形状 | MIT 6.006 Binary Trees | 空树、单节点、深链、层序与后序 |

- 所有图形由本项目独立绘制，图示本身仅表达所声明的教学模型，不暗示真实指针地址、CPU 时延或底层 Python 实现的内部版式。
- 所有可运行的参考算法位于 `examples/linear_structures.py`，对应小规模穷举与回归检查位于 `tests/test_linear_structures.py`；图解交互由 `assets/js/interactive.js` 增强。
- 本地和 GitHub Actions 的静态/Chromium 质量检查属于独立质量门禁；只对确实运行成功的测试记为通过。
