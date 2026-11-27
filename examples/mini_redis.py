"""第 28 章配套：MiniRedis 参考实现（可运行、可测试的 Redis 子集）。

包含三部分：
* 跳表 SkipList —— 支撑有序集合 ZSet；
* 最小堆管理的惰性过期 TTL；
* AOF 追加日志与启动重放（可选，默认关闭，便于测试）。
"""
from __future__ import annotations

import heapq
import random
import time
from typing import Callable, Dict, List, Optional, Tuple


class SkipListNode:
    __slots__ = ("score", "member", "forward")

    def __init__(self, score: float, member: Optional[str], level: int):
        self.score = score
        self.member = member
        self.forward: List[Optional["SkipListNode"]] = [None] * (level + 1)


class SkipList:
    """按 (score, member) 有序的跳表；member 已存在时更新其 score。"""

    MAX_LEVEL = 16
    P = 0.5

    def __init__(self, rng: Optional[random.Random] = None):
        self.head = SkipListNode(float("-inf"), None, self.MAX_LEVEL)
        self.level = 0
        self._rng = rng or random.Random()

    def _random_level(self) -> int:
        lvl = 0
        while self._rng.random() < self.P and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    @staticmethod
    def _less(a_score, a_member, b_score, b_member) -> bool:
        return a_score < b_score or (a_score == b_score and a_member < b_member)

    def _update_for(self, score, member) -> List[Optional["SkipListNode"]]:
        """从顶层向下，找到每层 score 之前的前驱节点。"""
        update: List[Optional[SkipListNode]] = [None] * (self.MAX_LEVEL + 1)
        curr = self.head
        for i in range(self.level, -1, -1):
            while curr.forward[i] and self._less(
                curr.forward[i].score, curr.forward[i].member, score, member
            ):
                curr = curr.forward[i]
            update[i] = curr
        return update

    def remove(self, score: float, member: str) -> bool:
        update = self._update_for(score, member)
        target = update[0].forward[0]
        if not target or target.member != member:
            return False
        for i in range(self.level + 1):
            if update[i].forward[i] is not target:
                break
            update[i].forward[i] = target.forward[i]
        while self.level > 0 and self.head.forward[self.level] is None:
            self.level -= 1
        return True

    def insert(self, score: float, member: str) -> None:
        """ZADD：member 已存在则先删旧节点再插入（分数可能变化）。"""
        node = self.head.forward[0]
        while node:
            if node.member == member:
                if node.score == score:
                    return
                self.remove(node.score, member)
                break
            node = node.forward[0]
        update = self._update_for(score, member)
        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.head
            self.level = lvl
        new_node = SkipListNode(score, member, lvl)
        for i in range(lvl + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def range_by_rank(self, start: int, end: int) -> List[Tuple[str, float]]:
        """ZRANGE：按排名区间（0-indexed，含两端，负号从尾数）。"""
        items = self._ordered()
        n = len(items)
        if start < 0:
            start += n
        if end < 0:
            end += n
        start = max(start, 0)
        end = min(end, n - 1)
        return items[start:end + 1] if start <= end else []

    def range_by_score(self, min_score: float, max_score: float) -> List[Tuple[str, float]]:
        """ZRANGEBYSCORE：按分数区间（含两端）获取成员。"""
        return [(m, s) for m, s in self._ordered() if min_score <= s <= max_score]

    def _ordered(self) -> List[Tuple[str, float]]:
        out: List[Tuple[str, float]] = []
        curr = self.head.forward[0]
        while curr:
            out.append((curr.member, curr.score))
            curr = curr.forward[0]
        return out


class MiniRedis:
    """简化版 Redis：字符串 + 有序集合 + TTL + 可选 AOF。

    clock 可注入（返回秒级时间戳），TTL 因此可确定性测试。
    """

    def __init__(self, aof_path: Optional[str] = None,
                 clock: Callable[[], float] = time.time):
        self.data: Dict[str, str] = {}
        self.zsets: Dict[str, SkipList] = {}
        self.ttl_heap: List[Tuple[float, str]] = []
        self.ttl_map: Dict[str, float] = {}
        self.aof_path = aof_path
        self._clock = clock
        if aof_path:
            self._load_aof()

    # ---------- String ----------
    def set(self, key: str, value) -> None:
        self.data[key] = str(value)
        self._append_aof(f"SET {key} {value}")

    def get(self, key: str) -> Optional[str]:
        self._expire_keys()
        return self.data.get(key)

    def delete(self, key: str) -> None:
        self.data.pop(key, None)
        self.ttl_map.pop(key, None)   # 惰性：堆中旧项会在弹出时被忽略
        self._append_aof(f"DEL {key}")

    # ---------- ZSet ----------
    def zadd(self, name: str, score, member: str) -> None:
        self.zsets.setdefault(name, SkipList()).insert(float(score), member)
        self._append_aof(f"ZADD {name} {score} {member}")

    def zrange(self, name: str, start: int, end: int) -> List[Tuple[str, float]]:
        sl = self.zsets.get(name)
        return sl.range_by_rank(start, end) if sl else []

    def zrange_by_score(self, name: str, lo, hi) -> List[Tuple[str, float]]:
        sl = self.zsets.get(name)
        return sl.range_by_score(lo, hi) if sl else []

    # ---------- TTL（最小堆 + 惰性删除） ----------
    def expire(self, key: str, seconds: float) -> None:
        expiry = self._clock() + seconds
        heapq.heappush(self.ttl_heap, (expiry, key))
        self.ttl_map[key] = expiry

    def _expire_keys(self) -> None:
        now = self._clock()
        while self.ttl_heap and self.ttl_heap[0][0] <= now:
            expiry, key = heapq.heappop(self.ttl_heap)
            if self.ttl_map.get(key) == expiry:   # 未被重新设置才真删
                self.data.pop(key, None)
                del self.ttl_map[key]

    # ---------- AOF ----------
    def _append_aof(self, command: str) -> None:
        if not self.aof_path:
            return
        with open(self.aof_path, "a", encoding="utf-8") as f:
            f.write(command + "\n")

    def _load_aof(self) -> None:
        try:
            with open(self.aof_path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
        except FileNotFoundError:
            return
        for line in lines:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "SET" and len(parts) >= 3:
                self.data[parts[1]] = " ".join(parts[2:])
            elif parts[0] == "DEL" and len(parts) == 2:
                self.data.pop(parts[1], None)
            elif parts[0] == "ZADD" and len(parts) == 4:
                self.zsets.setdefault(parts[1], SkipList()).insert(float(parts[2]), parts[3])
