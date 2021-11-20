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
            len(new_state.current_graph.edges) == 1,
            f"new_state should contain a single edge, but {len(new_state.current_graph.edges)} found.",
        )

        self.assertTrue(
            new_state.current_graph.edges[0].label == Actions.ALIGN,
            f"label of single edge in new_state.current_state should be {Actions.ALIGN}, but label was {new_state.current_graph.edges[0].label}",
        )
