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
                    # top of stack
                    Symbol(
                        symbol="a",
                        original_index=0,
                        index=0,
                        source=TranscriptTypes.TRANSCRIPT,
                    ),
                    Symbol(
                        symbol="a",
                        original_index=0,
                        index=0,
                        source=TranscriptTypes.GOLD,
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
                Symbol(
                    symbol="a",
                    original_index=0,
                    index=0,
                    source=TranscriptTypes.GOLD,
                ),
                Symbol(
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

    def test_STACK_SWAP(self):
        """`clu.phontools.alignment.parser.state.State` should support Actions.STACK_SWAP."""

        first_ps = Symbol(
            symbol="b",
            original_index=1,
            index=1,
            source=TranscriptTypes.TRANSCRIPT,
        )
        second_ps = Symbol(
            symbol="a",
            original_index=0,
            index=0,
            source=TranscriptTypes.GOLD,
        )
        state = State(
            stack=Stack(
                [
                    # top of stack
                    first_ps,
                    second_ps,
                ]
            ),
            gold_queue=Queue(),
            transcribed_queue=Queue(),
            gold_graph=None,
            current_graph=Graph(edges=[]),
        )

        valid_actions = state.valid_actions()
        new_state = state.perform_action(Actions.STACK_SWAP)
        self.assertTrue(
            Actions.STACK_SWAP in valid_actions,
            f"state should support Actions.STACK_SWAP, but only the following were present: {valid_actions}.",
        )

        self.assertTrue(
            state.is_valid_STACK_SWAP(),
            f"configured state should allow STACK_SWAP action when there are >= 2 items on stack",
        )

        self.assertTrue(
            len(new_state.current_graph.edges) == 0,
            f"new_state should not contain any edges, but {len(new_state.current_graph.edges)} found.",
        )

        top = new_state.stack.pop()
        self.assertEqual(
            top,
            second_ps,
            f"first item in stack of new_stack should now be 'a', but {top.symbol} found.",
        )

        problem_stack = Stack(
            [
                Symbol(
                    symbol="a",
                    original_index=0,
                    index=0,
                    source=TranscriptTypes.GOLD,
                )
            ]
        )
        bad_state = state.copy(stack=problem_stack)
        self.assertFalse(
            bad_state.is_valid_STACK_SWAP(),
            f"state should NOT allow STACK_SWAP action when < 2 items on stack",
        )

    def test_SHIFT_G(self):
        """`clu.phontools.alignment.parser.state.State` should support Actions.SHIFT_G."""

        ps = Symbol(
            symbol="a",
            original_index=0,
            index=0,
            source=TranscriptTypes.GOLD,
        )

        state = State(
            stack=Stack(),
            gold_queue=Queue([ps]),
            transcribed_queue=Queue(),
            gold_graph=None,
            current_graph=Graph(edges=[]),
        )

        valid_actions = state.valid_actions()
        ACTION = Actions.SHIFT_G
        new_state = state.perform_action(ACTION)
        self.assertTrue(
            ACTION in valid_actions,
            f"state should support Actions.SHIFT_G, but only the following were present: {valid_actions}.",
        )

        self.assertTrue(
            state.is_valid_SHIFT_G(),
            f"configured state should allow SHIFT_G action when there are > 0 items on gold_queue",
        )

        self.assertTrue(
            len(new_state.current_graph.edges) == 0,
            f"new_state should not contain any edges, but {len(new_state.current_graph.edges)} found.",
        )

        top = new_state.stack.pop()
        self.assertEqual(
            top,
            ps,
            f"first item in stack of new_stack should now be 'a', but {top.symbol} found.",
        )

        problem_queue = Queue()
        bad_state = state.copy(gold_queue=problem_queue)
        self.assertFalse(
            bad_state.is_valid_SHIFT_G(),
            f"state should NOT allow SHIFT_G action when < 1 items on gold_queue",
        )

    def test_SHIFT_T(self):
        """`clu.phontools.alignment.parser.state.State` should support Actions.SHIFT_T."""

        ps = Symbol(
            symbol="a",
            original_index=0,
            index=0,
            source=TranscriptTypes.TRANSCRIPT,
        )

        state = State(
            stack=Stack(),
            gold_queue=Queue(),
            transcribed_queue=Queue([ps]),
            gold_graph=None,
            current_graph=Graph(edges=[]),
        )

        valid_actions = state.valid_actions()
        ACTION = Actions.SHIFT_T
        new_state = state.perform_action(ACTION)
        self.assertTrue(
            ACTION in valid_actions,
            f"state should support Actions.SHIFT_T, but only the following were present: {valid_actions}.",
        )

        self.assertTrue(
            state.is_valid_SHIFT_T(),
            f"configured state should allow SHIFT_T action when there are > 0 items on transcribed_queue",
        )

        self.assertTrue(
            len(new_state.current_graph.edges) == 0,
            f"new_state should not contain any edges, but {len(new_state.current_graph.edges)} found.",
        )

        top = new_state.stack.pop()
        self.assertEqual(
            top,
            ps,
            f"first item in stack of new_stack should now be 'a', but {top.symbol} found.",
        )

        problem_queue = Queue()
        bad_state = state.copy(transcribed_queue=problem_queue)
        self.assertFalse(
            bad_state.is_valid_SHIFT_T(),
            f"state should NOT allow SHIFT_T action when < 1 items on transcribed_queue",
        )
