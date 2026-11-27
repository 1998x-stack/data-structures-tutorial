"""第 23 章配套：刷题方法论里出现的可运行参考实现。

覆盖三类内容：
* 反转链表的递归 / 迭代写法（文章中作为“一类题”的核心骨架）；
* 两数之和（文章中作为口述复杂度分析的例子）；
* 间隔复习排期（把错题本里的复习计划算成具体天数）。
"""
from __future__ import annotations

from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, nxt: "Optional[ListNode]" = None):
        self.val = val
        self.next = nxt


def build(values: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> List[int]:
    out: List[int] = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def reverse_list_iterative(head: Optional[ListNode]) -> Optional[ListNode]:
    prev = None
    curr = head
    while curr:
        nxt = curr.next   # 先保存下一个节点
        curr.next = prev  # 再反转指针
        prev = curr       # 移动 prev
        curr = nxt        # 移动 curr
    return prev


def reverse_list_recursive(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head  # 让后继节点指回自己
    head.next = None       # 断开旧指针，避免成环
    return new_head


def two_sum(nums: List[int], target: int) -> List[int]:
    """时间 O(n)，额外空间 O(n)；哈希表查找是平均 O(1)。"""
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return [-1, -1]


REVIEW_INTERVALS_DAYS = [1, 3, 7, 30]


def review_days(start_day: int, intervals: Optional[List[int]] = None) -> List[int]:
    """把“错题当天”映射成 1 天 / 3 天 / 1 周 / 1 月后的复习日。"""
    if intervals is None:
        intervals = REVIEW_INTERVALS_DAYS
    return [start_day + d for d in intervals]
