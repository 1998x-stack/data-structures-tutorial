"""第 24 章配套：大厂面试高频题的参考实现与复杂度注释。

每个函数对应文章中的一道题，返回约定与文章一致。链表/树节点在本模块
内自带定义，方便单独导入运行。
"""
from __future__ import annotations

from collections import deque
from typing import List, Optional


def two_sum(nums: List[int], target: int) -> List[int]:
    """LeetCode 1. 两数之和 — 哈希表，时间 O(n)，额外空间 O(n)。"""
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return [-1, -1]


def three_sum(nums: List[int]) -> List[List[int]]:
    """LeetCode 15. 三数之和 — 排序 + 双指针，时间 O(n^2)，额外空间 O(log n)。"""
    nums = sorted(nums)
    res = []
    n = len(nums)
    for i in range(n - 2):
        if nums[i] > 0:                       # 排序后首数 > 0，后面不可能和为 0
            break
        if i > 0 and nums[i] == nums[i - 1]:  # 跳过重复的 i
            continue
        left, right = i + 1, n - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                res.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif s < 0:
                left += 1
            else:
                right -= 1
    return res


class ListNode:
    def __init__(self, val: int = 0, nxt: "Optional[ListNode]" = None):
        self.val = val
        self.next = nxt


def build_list(values: List[int], pos: int = -1) -> Optional[ListNode]:
    """构建链表；pos >= 0 时让尾节点指向下标 pos，用于造环。"""
    dummy = ListNode()
    tail = dummy
    nodes = []
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos >= 0 and nodes:
        tail.next = nodes[pos]
    return dummy.next


def to_list(head: Optional[ListNode], limit: int = 100) -> List[int]:
    out = []
    while head and len(out) < limit:
        out.append(head.val)
        head = head.next
    return out


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """LeetCode 206. 反转链表 — 三指针迭代，时间 O(n)，空间 O(1)。"""
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev


def detect_cycle(head: Optional[ListNode]) -> Optional[ListNode]:
    """LeetCode 142. 环形链表 II — 快慢指针，时间 O(n)，空间 O(1)。"""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:            # 相遇说明有环
            break
    else:
        return None
    slow = head                     # 一个从头，一个从相遇点，同步走
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow


def is_valid(s: str) -> bool:
    """LeetCode 20. 有效括号 — 栈，时间 O(n)，空间 O(n)。"""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
        else:
            stack.append(ch)
    return not stack


def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """LeetCode 239. 滑动窗口最大值 — 单调递减双端队列，时间 O(n)，空间 O(k)。"""
    if k <= 0 or not nums:
        return []
    dq = deque()          # 存下标，对应值单调递减
    result = []
    for i, num in enumerate(nums):
        if dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result


class TreeNode:
    def __init__(self, val: int = 0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """LeetCode 94. 中序遍历（递归）。"""
    res: List[int] = []

    def dfs(node):
        if not node:
            return
        dfs(node.left)
        res.append(node.val)
        dfs(node.right)
    dfs(root)
    return res


def inorder_traversal_iterative(root: Optional[TreeNode]) -> List[int]:
    """LeetCode 94. 中序遍历（手动模拟栈）。"""
    res, stack, curr = [], [], root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        res.append(curr.val)
        curr = curr.right
    return res


def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """LeetCode 102. 层序遍历 — BFS 模板，时间 O(n)，空间 O(n)。"""
    if not root:
        return []
    res = []
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):    # 先固定本层节点数
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(level)
    return res


def num_islands(grid: List[List[str]]) -> int:
    """LeetCode 200. 岛屿数量 — DFS 淹没法，时间 O(m*n)，空间 O(m*n) 最坏栈深。"""
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                dfs(r, c)
    return count


def climb_stairs(n: int) -> int:
    """LeetCode 70. 爬楼梯 — 滚动变量 DP，时间 O(n)，空间 O(1)。"""
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


def length_of_lis(nums: List[int]) -> int:
    """LeetCode 300. 最长递增子序列 — 贪心 + 二分，时间 O(n log n)，空间 O(n)。"""
    tails = []      # tails[i] = 长度为 i+1 的递增子序列的最小末尾值
    for num in nums:
        left, right = 0, len(tails)
        while left < right:                 # 找第一个 >= num 的位置
            mid = (left + right) // 2
            if tails[mid] < num:
                left = mid + 1
            else:
                right = mid
        if left == len(tails):
            tails.append(num)
        else:
            tails[left] = num
    return len(tails)


def longest_common_subsequence(text1: str, text2: str) -> int:
    """LeetCode 1143. 最长公共子序列 — 二维 DP，时间 O(m*n)，空间 O(m*n)。"""
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """LeetCode 23. 合并 K 个升序链表 — 分治两两合并，时间 O(N log k)，空间 O(log k)。"""
    import heapq
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    dummy = ListNode()
    tail = dummy
    while heap:
        _, i, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next


def trap(height: List[int]) -> int:
    """LeetCode 42. 接雨水 — 左右双指针，时间 O(n)，空间 O(1)。"""
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if height[left] < height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water


class _DNode:
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev: Optional["_DNode"] = None
        self.next: Optional["_DNode"] = None


class LRUCache:
    """LeetCode 146. LRU 缓存 — 哈希表 + 双向链表（带哨兵），get/put 均 O(1)。"""

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.cache = {}
        self.head = _DNode()   # 虚拟头，head.next 是最近使用
        self.tail = _DNode()   # 虚拟尾，tail.prev 是最久未使用
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_head(node)
        else:
            if len(self.cache) >= self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
            node = _DNode(key, value)
            self.cache[key] = node
            self._add_to_head(node)
