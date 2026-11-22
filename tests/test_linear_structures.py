"""Deterministic exhaustive and regression tests for chapters 04–08."""
import itertools
import sys
import unittest
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from linear_structures import (
    CircularQueue, LRUCache, Node, Stack, TreeNode, bfs_distance, daily_temperatures,
    evaluate_rpn, from_values, has_cycle, height_edges, inorder, largest_rectangle_area,
    level_order, linked_values, postorder, preorder, preorder_iter, remove_value,
    reverse_list, sample_tree, sliding_window_max, toy_bucket, two_sum_unsorted,
    valid_brackets,
)


class LinkedListTests(unittest.TestCase):
    def test_remove_and_reverse_exhaustive(self):
        for n in range(6):
            for values in itertools.product((-1, 0, 1), repeat=n):
                for target in (-1, 0, 1, 9):
                    result = remove_value(from_values(values), target)
                    self.assertEqual(linked_values(result), [x for x in values if x != target])
                head = from_values(values)
                reversed_head = reverse_list(head)
                self.assertEqual(linked_values(reversed_head), list(reversed(values)))
                self.assertEqual(linked_values(reverse_list(reversed_head)), list(values))

    def test_cycle_identity_and_empty(self):
        self.assertFalse(has_cycle(None))
        for n in range(1, 8):
            nodes = [Node(1) for _ in range(n)]  # equal values, distinct identities
            for i in range(n - 1):
                nodes[i].next = nodes[i + 1]
            self.assertFalse(has_cycle(nodes[0]))
            for target in range(n):
                nodes[-1].next = nodes[target]
                self.assertTrue(has_cycle(nodes[0]))
                with self.assertRaises(ValueError):
                    linked_values(nodes[0])
                nodes[-1].next = None


class StackTests(unittest.TestCase):
    def test_contract(self):
        s=Stack()
        with self.assertRaises(IndexError):
            s.pop()
        with self.assertRaises(IndexError):
            s.peek()
        for x in range(10):
            s.push(x)
            self.assertEqual(s.peek(), x)
        self.assertEqual([s.pop() for _ in range(10)], list(reversed(range(10))))

    def test_brackets(self):
        for s in ("", "()", "[]", "{[()]}","([]{})"):
            self.assertTrue(valid_brackets(s))
        for s in ("(", ")(", "([)]", "{[(])}", "(]", "]"):
            self.assertFalse(valid_brackets(s))
        with self.assertRaises(ValueError):
            valid_brackets("a()")

    def test_rpn(self):
        self.assertEqual(evaluate_rpn(["3","4","+","2","*"]), 14)
        self.assertEqual(evaluate_rpn(["6","2","-"]), 4)
        self.assertEqual(evaluate_rpn(["-5","2","*"]), -10)
        for invalid in ([], ["1","2"], ["+"], ["1","+"]):
            with self.assertRaises(ValueError):
                evaluate_rpn(invalid)

    def test_daily_temperatures_exhaustive(self):
        for n in range(7):
            for seq in itertools.product((0,1,2), repeat=n):
                expected=[]
                for i,x in enumerate(seq):
                    expected.append(next((j-i for j in range(i+1,n) if seq[j]>x),0))
                self.assertEqual(daily_temperatures(seq),expected)

    def test_histogram_exhaustive(self):
        for n in range(6):
            for seq in itertools.product((0,1,3), repeat=n):
                brute=max((min(seq[l:r])*(r-l) for l in range(n) for r in range(l+1,n+1)),default=0)
                self.assertEqual(largest_rectangle_area(seq),brute)
        self.assertEqual(largest_rectangle_area([]),0)
        with self.assertRaises(ValueError):
            largest_rectangle_area([1,-1,2])


class QueueTests(unittest.TestCase):
    def test_circular_fifo_exhaustive(self):
        with self.assertRaises(ValueError):
            CircularQueue(0)
        for capacity in (1,2,3):
            for actions in itertools.product((0,1),repeat=7):
                q,oracle=CircularQueue(capacity),deque()
                for i,action in enumerate(actions):
                    if action==1:
                        if len(oracle)==capacity:
                            with self.assertRaises(OverflowError):
                                q.enqueue(i)
                        else:
                            q.enqueue(i)
                            oracle.append(i)
                    else:
                        if not oracle:
                            with self.assertRaises(IndexError):
                                q.dequeue()
                        else:
                            self.assertEqual(q.dequeue(),oracle.popleft())
                    self.assertEqual(len(q),len(oracle))
                while oracle:
                    self.assertEqual(q.dequeue(),oracle.popleft())

    def test_sliding_max_exhaustive(self):
        with self.assertRaises(ValueError):
            sliding_window_max([],1)
        for n in range(1,7):
            for seq in itertools.product((-2,0,2),repeat=n):
                for k in range(1,n+1):
                    expected=[max(seq[i:i+k]) for i in range(n-k+1)]
                    self.assertEqual(sliding_window_max(seq,k),expected)
        with self.assertRaises(ValueError):
            sliding_window_max([1,2],0)
        with self.assertRaises(ValueError):
            sliding_window_max([1,2],3)

    def test_bfs_cycles_and_disconnected(self):
        graph={0:[1,2],1:[0,2,3],2:[0,1,4],3:[4],4:[3],5:[]}
        self.assertEqual(bfs_distance(graph,0),{0:0,1:1,2:1,3:2,4:2})
        self.assertEqual(bfs_distance(graph,5),{5:0})


class HashTests(unittest.TestCase):
    def test_toy_collision(self):
        self.assertEqual([toy_bucket(x) for x in (12,17,22)],[2,2,2])
        self.assertEqual(toy_bucket(-3),2)
        with self.assertRaises(ValueError):
            toy_bucket(1,0)

    def test_two_sum_exhaustive(self):
        for n in range(6):
            for seq in itertools.product((-1,0,2),repeat=n):
                for target in range(-4,6):
                    ans=two_sum_unsorted(seq,target)
                    valid=any(seq[i]+seq[j]==target for i in range(n) for j in range(i+1,n))
                    self.assertEqual(ans is not None,valid)
                    if ans is not None:
                        i,j=ans
                        self.assertTrue(i<j)
                        self.assertEqual(seq[i]+seq[j],target)

    def test_lru_eviction_and_update(self):
        with self.assertRaises(ValueError):
            LRUCache(0)
        cache=LRUCache(3)
        for key in ("A","B","C"):
            cache.put(key,key.lower())
        self.assertEqual(cache.get("A"),"a")
        cache.put("D","d")
        self.assertEqual(list(cache.entries),["C","A","D"])
        cache.put("C","new")
        self.assertEqual(list(cache.entries),["A","D","C"])
        self.assertIsNone(cache.get("missing"))
        one=LRUCache(1)
        one.put("x",1)
        one.put("y",2)
        self.assertIsNone(one.get("x"))
        self.assertEqual(one.get("y"),2)
        with self.assertRaises(ValueError):
            one.put("z",None)


class TreeTests(unittest.TestCase):
    def test_sample_orders_and_height(self):
        t=sample_tree()
        self.assertEqual(preorder(t),[4,2,1,3,6,5])
        self.assertEqual(preorder_iter(t),preorder(t))
        self.assertEqual(inorder(t),[1,2,3,4,5,6])
        self.assertEqual(postorder(t),[1,3,2,5,6,4])
        self.assertEqual(level_order(t),[[4],[2,6],[1,3,5]])
        self.assertEqual(height_edges(t),2)

    def test_empty_single_and_skew(self):
        self.assertEqual(preorder(None),[])
        self.assertEqual(inorder(None),[])
        self.assertEqual(postorder(None),[])
        self.assertEqual(level_order(None),[])
        self.assertEqual(height_edges(None),-1)
        t=TreeNode(3)
        self.assertEqual(height_edges(t),0)
        for n in range(2,90):
            t=TreeNode(0)
            cur=t
            for i in range(1,n):
                cur.right=TreeNode(i)
                cur=cur.right
            self.assertEqual(height_edges(t),n-1)
            self.assertEqual(preorder_iter(t),list(range(n)))
            self.assertEqual(preorder(t),preorder_iter(t))
            self.assertEqual(len(inorder(t)),n)
            self.assertEqual(len(postorder(t)),n)


if __name__=="__main__":
    unittest.main()
