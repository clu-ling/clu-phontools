# -*- coding: utf-8 -*-

import unittest
from clu.phontools.alignment.parser import *


"""
Test behavior of clu.phontools.alignment.parser.constraints.Constraints
"""


class ConstraintsTests(unittest.TestCase):
    # for testing: participates_in_an_edge, is_a_parent, is_a_child
    symbol = Symbol(original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD)
    graph = Graph(
        edges=[
            Edge(
                source=Symbol(
                    original_index=0,
                    index=0,
                    symbol="a",
                    source=TranscriptTypes.TRANSCRIPT,
                ),
                destination=Symbol(
                    original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD,
                ),
                label=Actions.ALIGN,
            ),
            Edge(
                source=Symbol(
                    original_index=0,
                    index=0,
                    symbol="a",
                    source=TranscriptTypes.TRANSCRIPT,
                ),
                destination=Symbol(
                    original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD,
                ),
                label=Actions.ALIGN,
            ),
        ]
    )

    def test_stack_top_two_different_sources(self):
        """`clu.phontools.alignment.parser.constraints.Constraints.stack_top_two_different_sources` should verify the top two symbols are of different sources."""
        transcript = Symbol(
            original_index=0, index=0, symbol="a", source=TranscriptTypes.TRANSCRIPT
        )
        gold = Symbol(
            original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD
        )
        stack = Stack()
        # empty
        self.assertTrue(
            stack.is_empty(), f"stack.is_empty() for empty stack returned False"
        )
        # push
        stack.push(transcript)
        stack.push(gold)
        # check len
        self.assertTrue(len(stack) == 2, f"len(stack) should be 2")

        self.assertTrue(
            Constraints.stack_top_two_different_sources(stack) == True,
            f"Constraints.stack_top_two_different_sources(stack) should return bool(True)",
        )

    def test_participate_in_an_edge(self):
        """`clu.phontools.alignment.parser.constraints.Constraints.participates_in_an_edge` should check if the provided Symbol participates in an edge"""
        self.assertTrue(
            Constraints.participates_in_an_edge(symbol, graph) == False,
            f"Constraints.participates_in_an_edge(symbol, graph) should return bool(False)",
        )

    def test_is_a_parent(self):
        """`clu.phontools.alignment.parser.constraints.Constraints.is_a_parent` should check if the provided Symbol is a parent (source) in an edge"""
        self.assertTrue(
            Constraints.is_a_parent(symbol, graph) == False,
            f"Constraints.is_a_parent(symbol, graph) should return bool(False)",
        )

    def test_is_a_child(self):
        """`clu.phontools.alignment.parser.constraints.Constraints.is_a_child` should check if the provided Symbol is a child (destination) in an edge"""
        self.assertTrue(
            Constraints.is_a_child(symbol, graph) == False,
            f"Constraints.is_a_child(symbol, graph) should return bool(False)",
        )

    def test_many_to_one_and_vice_versa(self):
        """`clu.phontools.alignment.parser.constraints.Constraints.many_to_one_and_vice_versa` should check the length of both queues to validate the discard action"""
        trans_queue = Queue(
            [
                Symbol(
                    original_index=-1,
                    index=0,
                    symbol="NULL",
                    source=TranscriptTypes.TRANSCRIPT,
                ),
                Symbol(
                    original_index=-1,
                    index=1,
                    symbol="NULL",
                    source=TranscriptTypes.TRANSCRIPT,
                ),
                Symbol(
                    original_index=0,
                    index=2,
                    symbol="a",
                    source=TranscriptTypes.TRANSCRIPT,
                ),
            ]
        )
        gold_queue = Queue(
            [
                Symbol(
                    original_index=-1,
                    index=0,
                    symbol="NULL",
                    source=TranscriptTypes.GOLD,
                ),
                Symbol(
                    original_index=0, index=1, symbol="a", source=TranscriptTypes.GOLD
                ),
            ]
        )

        self.assertTrue(
            Constraints.many_to_one_and_vice_versa(trans_queue, gold_queue) == True,
            f"Constraints.many_to_one_and_vice_versa(trans_queue, gold_queue) should return bool(True)",
        )
