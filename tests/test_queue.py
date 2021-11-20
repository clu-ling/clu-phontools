# -*- coding: utf-8 -*-

import unittest
from clu.phontools.alignment.parser import *


"""
Test behavior of clu.phontools.alignment.parser.stack.Stack
"""


class QueueTests(unittest.TestCase):
    def test_len(self):
        """`clu.phontools.alignment.parser.queue.Queue` should have length defined."""
        self.assertTrue(
            len(Queue()) == 0, f"len(Queue()) should be 0, but was {len(Queue())}"
        )
        q = Queue(
            [
                ParseSymbol(
                    original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD
                )
            ]
        )
        self.assertTrue(len(q) == 1, f"len(q) should be 1, but was {len(q)}")
