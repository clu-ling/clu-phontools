# -*- coding: utf-8 -*-

import unittest
from clu.phontools.alignment.parser import *


"""
Test behavior of clu.phontools.alignment.parser.stack.Stack
"""


class StackTests(unittest.TestCase):
    def test_len(self):
        """`clu.phontools.alignment.parser.stack.Stack` should have length defined."""
        self.assertTrue(
            len(Stack()) == 0, f"len(Stack()) should be 0, but was {len(Stack())}"
        )
        s = Stack(
            [
                ParseSymbol(
                    original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD
                )
            ]
        )
        self.assertTrue(len(s) == 1, f"len(s) should be 1, but was {len(s)}")
