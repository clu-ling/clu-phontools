# -*- coding: utf-8 -*-

import unittest
from clu.phontools.alignment.parser import *


"""
Test behavior of clu.phontools.alignment.parser.queue.Queue
"""


class QueueTests(unittest.TestCase):
    def test_len(self):
        """`clu.phontools.alignment.parser.queue.Queue` should have length defined."""
        self.assertTrue(
            len(Queue()) == 0, f"len(Queue()) should be 0, but was {len(Queue())}"
        )
        q = Queue(
            [Symbol(original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD)]
        )
        self.assertTrue(len(q) == 1, f"len(q) should be 1, but was {len(q)}")

    def test_push(self):
        """`clu.phontools.alignment.parser.queue.Queue.push` should push an element into the first position of the queue."""
        q = Queue()
        symbol = [
            Symbol(original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD)
        ]
        q.push(symbol)
        self.assertTrue(len(q) == 1, f"len(q) should be 1, but was {len(q)}")

    def test_pop(self):
        """`clu.phontools.alignment.parser.queue.Queue.pop` should delete the first element in the queue """
        q = Queue(
            [Symbol(original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD)]
        )
        q.pop()
        self.assertTrue(len(q) == 0, f"len(q) should be 1, but was {len(q)}")

    def test_is_empty(self):
        """`clu.phontools.alignment.parser.queue.Queue` should support .is_empty()"""
        ps = Symbol(original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD)
        q = Queue()
        # empty
        self.assertTrue(q.is_empty(), f"s.is_empty() for empty queue returned False")
        ## non-empty
        q.push(ps)
        self.assertFalse(
            q.is_empty(), f"s.is_empty() for non-empty queue returned True"
        )
        # empty
        q.pop()
        self.assertTrue(q.is_empty(), f"s.is_empty() for empty queue returned False")

