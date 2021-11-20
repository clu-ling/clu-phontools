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


    def test_push(self):
        """`clu.phontools.alignment.parser.stack.Stack` should support .push()"""
        s = Stack()
        ps = ParseSymbol(original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD)
        s.push(ps)
        self.assertTrue(
            len(s) == 1, f"length of empty stack after pushing 1 element should be 1, but was {len(s)}"
        )

    def test_pop(self):
        """`clu.phontools.alignment.parser.stack.Stack` should support .pop()"""
        ps = ParseSymbol(original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD)
        s = Stack([ps])
        s.pop()
        self.assertTrue(
            len(s) == 0, f"length of stack with 1 element after popping 1 element should be 0, but was {len(s)}"
        )

    def test_is_empty(self):
        """`clu.phontools.alignment.parser.stack.Stack` should support .is_empty()"""
        ps = ParseSymbol(original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD)
        s = Stack()
        # empty
        self.assertTrue(
            s.is_empty(), f"s.is_empty() for empty stack returned False"
        )
        # non-empty
        s.push(ps)
        self.assertFalse(
            s.is_empty(), f"s.is_empty() for non-empty stack returned True"
        )
        # empty
        s.pop()
        self.assertTrue(
          s.is_empty(), f"s.is_empty() for empty stack returned False"
        )