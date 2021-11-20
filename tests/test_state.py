# -*- coding: utf-8 -*-

import unittest
from clu.phontools.alignment.parser import *


"""
Test behavior of State
"""


class StateTests(unittest.TestCase):
    def test_ALIGN(self):
        """`clu.phontools.alignment.parser.state.State` should support Actions.ALIGN."""

        state = State(
            stack=Stack(
                [
                    ParseSymbol(
                        symbol="a",
                        original_index=0,
                        index=0,
                        source=TranscriptTypes.GOLD,
                    ),
                    # top of stack
                    ParseSymbol(
                        symbol="a",
                        original_index=0,
                        index=0,
                        source=TranscriptTypes.TRANSCRIPT,
                    ),
                ]
            ),
            gold_queue=Queue([]),
            transcribed_queue=Queue([]),
            gold_graph=None,
            current_graph=Graph(edges=[]),
        )

        valid_actions = state.valid_actions()
        new_state = state.perform_action(Actions.ALIGN)
        self.assertTrue(
            Actions.ALIGN in valid_actions,
            f"state should support Actions.ALIGN, but only the following were present: {valid_actions}.",
        )

        self.assertTrue(
            state.is_valid_ALIGN(),
            f"configured state should allow ALIGN action when top two items on stack are from GOLD and TRANSCRIPT",
        )

        self.assertTrue(
            len(new_state.current_graph.edges) == 1,
            f"new_state should contain a single edge, but {len(new_state.current_graph.edges)} found.",
        )

        self.assertTrue(
            new_state.current_graph.edges[0].label == Actions.ALIGN,
            f"label of single edge in new_state.current_state should be {Actions.ALIGN}, but label was {new_state.current_graph.edges[0].label}",
        )

        edge = new_state.current_graph.edges[0]
        self.assertEqual(
            edge.destination.source,
            TranscriptTypes.GOLD,
            f"ALIGN must point from TRANSCRIPT -> GOLD",
        )

        problem_stack = Stack(
            [
                ParseSymbol(
                    symbol="a",
                    original_index=0,
                    index=0,
                    source=TranscriptTypes.GOLD,
                ),
                ParseSymbol(
                    symbol="b",
                    original_index=1,
                    index=1,
                    source=TranscriptTypes.GOLD,
                ),
            ]
        )
        bad_state = state.copy(stack=problem_stack)
        self.assertFalse(
            bad_state.is_valid_ALIGN(),
            f"state should NOT allow ALIGN action when top two items on stack are both from GOLD",
        )
