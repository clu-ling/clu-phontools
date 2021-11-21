# -*- coding: utf-8 -*-

import unittest
from clu.phontools.alignment.parser import *


"""
Test behavior of State
"""


class StateTests(unittest.TestCase):

    # for test purposes
    gold_a = Symbol(
        symbol="a",
        original_index=0,
        index=0,
        source=TranscriptTypes.GOLD,
    )
    gold_b = Symbol(
        symbol="b",
        original_index=1,
        index=1,
        source=TranscriptTypes.GOLD,
    )
    trans_a = Symbol(
        symbol="a",
        original_index=0,
        index=0,
        source=TranscriptTypes.TRANSCRIPT,
    )
    trans_b = Symbol(
        symbol="b",
        original_index=1,
        index=1,
        source=TranscriptTypes.TRANSCRIPT,
    )

    # Actions
    def test_ALIGN(self):
        """`clu.phontools.alignment.parser.state.State` should support Actions.ALIGN."""

        state = State(
            stack=Stack(
                [
                    # top of stack
                    StateTests.trans_a,
                    StateTests.gold_a,
                ]
            ),
            gold_queue=Queue([]),
            transcribed_queue=Queue([]),
            gold_graph=None,
            current_graph=Graph(edges=[]),
        )

        valid_actions = state.valid_actions()
        ACTION = Actions.ALIGN
        new_state = state.perform_action(ACTION)
        self.assertTrue(
            Actions.ALIGN in valid_actions,
            f"state should support Actions.ALIGN, but only the following were present: {valid_actions}.",
        )

        self.assertTrue(
            state.is_valid(ACTION),
            f"configured state should allow ALIGN action when top two items on stack are from GOLD and TRANSCRIPT",
        )

        self.assertTrue(
            len(new_state.current_graph.edges) == 1,
            f"new_state should contain a single edge, but {len(new_state.current_graph.edges)} found.",
        )

        self.assertEqual(
            new_state.last_action(),
            ACTION,
            f"new_state.last_action() should be {ACTION}, but was {new_state.last_action()}",
        )

        self.assertTrue(
            new_state.current_graph.edges[0].label == ACTION,
            f"label of single edge in new_state.current_state should be {ACTION}, but label was {new_state.current_graph.edges[0].label}",
        )

        edge = new_state.current_graph.edges[0]
        self.assertEqual(
            edge.destination.source,
            TranscriptTypes.GOLD,
            f"ALIGN must point from TRANSCRIPT -> GOLD",
        )

        problem_stack = Stack([StateTests.gold_a, StateTests.gold_b])
        bad_state = state.copy(stack=problem_stack)
        self.assertFalse(
            bad_state.is_valid(ACTION),
            f"state should NOT allow ALIGN action when top two items on stack are both from GOLD",
        )

    def test_STACK_SWAP(self):
        """`clu.phontools.alignment.parser.state.State` should support Actions.STACK_SWAP."""

        first_ps = StateTests.trans_b
        second_ps = StateTests.trans_a
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
        ACTION = Actions.STACK_SWAP
        new_state = state.perform_action(Actions.STACK_SWAP)
        self.assertTrue(
            ACTION in valid_actions,
            f"state should support {ACTION}, but only the following were present: {valid_actions}.",
        )

        self.assertTrue(
            state.is_valid(ACTION),
            f"configured state should allow STACK_SWAP action when there are >= 2 items on stack",
        )

        self.assertTrue(
            len(new_state.current_graph.edges) == 0,
            f"new_state should not contain any edges, but {len(new_state.current_graph.edges)} found.",
        )

        self.assertEqual(
            new_state.last_action(),
            ACTION,
            f"new_state.last_action() should be {ACTION}, but was {new_state.last_action()}",
        )

        top = new_state.stack.pop()
        self.assertEqual(
            top,
            second_ps,
            f"first item in stack of new_stack should now be 'a', but {top.symbol} found.",
        )

        problem_stack = Stack([StateTests.gold_a])
        bad_state = state.copy(stack=problem_stack)
        self.assertFalse(
            bad_state.is_valid(ACTION),
            f"state should NOT allow STACK_SWAP action when < 2 items on stack",
        )

    def test_SHIFT_G(self):
        """`clu.phontools.alignment.parser.state.State` should support Actions.SHIFT_G."""

        state = State(
            stack=Stack(),
            gold_queue=Queue([StateTests.gold_a]),
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
            state.is_valid(ACTION),
            f"configured state should allow SHIFT_G action when there are > 0 items on gold_queue",
        )

        self.assertTrue(
            len(new_state.current_graph.edges) == 0,
            f"new_state should not contain any edges, but {len(new_state.current_graph.edges)} found.",
        )
        self.assertEqual(
            new_state.last_action(),
            ACTION,
            f"new_state.last_action() should be {ACTION}, but was {new_state.last_action()}",
        )

        top = new_state.stack.pop()
        self.assertEqual(
            top,
            StateTests.gold_a,
            f"first item in stack of new_stack should now be 'a', but {top.symbol} found.",
        )

        problem_queue = Queue()
        bad_state = state.copy(gold_queue=problem_queue)
        self.assertFalse(
            bad_state.is_valid(ACTION),
            f"state should NOT allow SHIFT_G action when < 1 items on gold_queue",
        )

    def test_SHIFT_T(self):
        """`clu.phontools.alignment.parser.state.State` should support Actions.SHIFT_T."""

        state = State(
            stack=Stack(),
            gold_queue=Queue(),
            transcribed_queue=Queue([StateTests.trans_a]),
            gold_graph=None,
            current_graph=Graph(edges=[]),
        )

        valid_actions = state.valid_actions()
        ACTION = Actions.SHIFT_T
        new_state = state.perform_action(ACTION)
        self.assertTrue(
            ACTION in valid_actions,
            f"state should support {ACTION}, but only the following were present: {valid_actions}.",
        )

        self.assertTrue(
            state.is_valid(ACTION),
            f"configured state should allow {ACTION} action when there are > 0 items on transcribed_queue",
        )

        self.assertTrue(
            len(new_state.current_graph.edges) == 0,
            f"new_state should not contain any edges, but {len(new_state.current_graph.edges)} found.",
        )

        self.assertEqual(
            new_state.last_action(),
            ACTION,
            f"new_state.last_action() should be {ACTION}, but was {new_state.last_action()}",
        )

        top = new_state.stack.pop()
        self.assertEqual(
            top,
            StateTests.trans_a,
            f"first item in stack of new_stack should now be 'a', but {top.symbol} found.",
        )

        problem_queue = Queue()
        bad_state = state.copy(transcribed_queue=problem_queue)
        self.assertFalse(
            bad_state.is_valid(ACTION),
            f"state should NOT allow {ACTION} action when < 1 items on transcribed_queue",
        )

    # def test_INSERTION_PRESERVE_CHILD(self):
    #     """`clu.phontools.alignment.parser.state.State` should support Actions.INSERTION_PRESERVE_CHILD."""

    #     ACTION = Actions.INSERTION_PRESERVE_CHILD
    #     stack = Stack()
    #     stack.push(StateTests.trans_b)
    #     stack.push(StateTests.gold_a)
    #     state = State(
    #         stack=stack,
    #         gold_queue=Queue(),
    #         transcribed_queue=Queue(),
    #         gold_graph=None,
    #         current_graph=Graph(edges=[]),
    #     )

    #     valid_actions = state.valid_actions()
    #     new_state = state.perform_action(ACTION)
    #     self.assertTrue(
    #         ACTION in valid_actions,
    #         f"state should support {ACTION}, but only the following were present: {valid_actions}.",
    #     )

    #     self.assertTrue(
    #         state.is_valid(ACTION),
    #         f"configured state should allow {ACTION} action when there are > 0 items on Stack and both are from gold and transcribed",
    #     )

    #     self.assertTrue(
    #         len(new_state.current_graph.edges) == 1,
    #         f"new_state should contain 1 edge, but {len(new_state.current_graph.edges)} found.",
    #     )

    #     self.assertEqual(
    #         new_state.last_action(),
    #         ACTION,
    #         f"new_state.last_action() should be {ACTION}, but was {new_state.last_action()}",
    #     )

    #     top = new_state.stack.pop()
    #     self.assertEqual(
    #         top,
    #         StateTests.gold_a,
    #         f"first item in stack of new_stack should now be 'a', but {top.symbol} found.",
    #     )

    #     problem_stack = Stack([StateTests.gold_a, StateTests.gold_b])
    #     bad_state = state.copy(stack=problem_stack)
    #     self.assertFalse(
    #         bad_state.is_valid(ACTION),
    #         f"state should NOT allow {ACTION} action when stack is {problem_stack._symbols}",
    #     )
