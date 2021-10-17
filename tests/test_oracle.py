# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch
from clu.phontools.alignment.realine import ReAline
from clu.phontools.alignment.parser import (
    Symbol,
    IntermediateSymbol,
    Index,
    State,
    Actions,
    Parser,
)


"""
Test `clu.phontools.alignment.parser.Index.prepare_symbols()` behaviors
Test `clu.phontools.alignment.parser.Index.assign_indexes()` behaviors
"""


class SymbolsTests(unittest.TestCase):
    def prepare_symbols_test(self):
        gold = "cat"
        symbols = Index.prepare_symbols(gold)
        res = ["NULL", "c", "NULL", "a", "NULL", "t", "NULL"]

        self.assertEqual(
            res,
            symbols,
            f"Index.prepare_symbols() should return an object where a special symbol 'NULL' is inserted between the characters of a given word",
        )

    def assign_index_test(self):
        text = "cat"
        symbols = Index.prepare_symbols(text)
        indexes = str(Index.assign_index(symbols))
        res = [
            (0, "NULL"),
            (1, "c"),
            (2, "NULL"),
            (3, "a"),
            (4, "NULL"),
            (5, "t"),
            (6, "NULL"),
        ]
        self.assertEqual(
            indexes,
            res,
            f"Index.prepare_index() should return a list of tuples with indexes and symbols.",
        )


class IndexTests(unittest.TestCase):
    """ Test `clu.phontools.paraser.Index` which assigns index to each
      character of a string, and returns both index and character
       in a list of tuples 
    """

    def test_prepare_symbols(self):
        print("mohammed")
        self.assertEqual(
            Index.prepare_symbols("cat"),
            ["NULL", "c", "NULL", "a", "NULL", "t", "NULL"],
        )

    def test_assign_index(self):
        self.assertEqual(
            Index.assign_index(Index.prepare_symbols("cat")),
            [
                (0, "NULL"),
                (1, "c"),
                (2, "NULL"),
                (3, "a"),
                (4, "NULL"),
                (5, "t"),
                (6, "NULL"),
            ],
        )


"""
Test `clu.phontools.alignment.parser.Edge` behaviors
"""


class SymbolsTests(unittest.TestCase):
    def edge_test(self):
        gold = "cat"
        transcript = "cats"

        res = [
            ("c", "align", "c"),
            ("a", "align", "a"),
            ("t", "align", "t"),
            ("-", "insertions", "s"),
        ]


"""
Test `clu.phontools.alignment.parser.State` behaviors
"""


class StateTests(unittest.TestCase):
    def test_gold_queue(self):
        state = State("cat", "cat")
        self.assertEqual(
            state.gold_queue(),
            [
                (0, "NULL"),
                (1, "c"),
                (2, "NULL"),
                (3, "a"),
                (4, "NULL"),
                (5, "t"),
                (6, "NULL"),
            ],
        )

    def test_transcribed_queue(self):
        state = State("cat", "cat")
        self.assertEqual(
            state.transcribed_queue(),
            [
                (0, "NULL"),
                (1, "c"),
                (2, "NULL"),
                (3, "a"),
                (4, "NULL"),
                (5, "t"),
                (6, "NULL"),
            ],
        )

    def test_realine_output(self):
        state = State("cat", "cat")
        self.assertEqual(state.realine_output(), [("c", "c"), ("a", "a"), ("t", "t")])

    def test_graph(self):
        state = State("cat", "cat")
        self.assertEqual(
            state.graph(),
            [("c", "align", "c"), ("a", "align", "a"), ("t", "align", "t")],
        )


"""
Test `clu.phontools.alignment.parser.Actions` behaviors
"""


class ActionsTests(unittest.TestCase):
    def test_actions(self):
        """`clu.phontools.alignment.parser.Actions.describe()` should return the correct enumerations of the actions used by the parser
        """
        assert len(Actions) == 11

        assert Actions.DISCARD_T.describe() == ("DISCARD_T", 1)
        assert Actions.DISCARD_G.describe() == ("DISCARD_G", 2)
        assert Actions.SHIFT_T.describe() == ("SHIFT_T", 3)
        assert Actions.SHIFT_G.describe() == ("SHIFT_G", 4)
        assert Actions.STACK_SWAP.describe() == ("STACK_SWAP", 5)
        assert Actions.INSERTION_PRESERVE_COPY_CHILD.describe() == (
            "INSERTION_PRESERVE_COPY_CHILD",
            6,
        )
        assert Actions.INSERTION_PRESERVE_COPY_PARENT.describe() == (
            "INSERTION_PRESERVE_COPY_PARENT",
            7,
        )
        assert Actions.DELETION_PRESERVE_COPY_CHILD.describe() == (
            "DELETION_PRESERVE_COPY_CHILD",
            8,
        )
        assert Actions.DELETION_PRESERVE_COPY_PARENT.describe() == (
            "DELETION_PRESERVE_COPY_PARENT",
            9,
        )
        assert Actions.ALIGN.describe() == ("ALIGN", 10)
        assert Actions.SUBSTITUTION.describe() == ("SUBSTITUTION", 11)


"""
Test `clu.phontools.alignment.parser.Parser` behaviors
"""


class ParserTests(unittest.TestCase):
    def test_check_edge(self):
        """
        `clu.phontools.alignment.parser.Parser.check_stack()` should return `True` or `False` to check if the two symbols on the
        stack are in the gold graph
        """
        gold_graph = [
            ("b", "b"),
            ("æ", "ɛ"),
            ("l", "l"),
        ]
        stack = ["b", "b"]
        stack_top = stack[-1]
        stack_bottom = stack[-2]
        self.assertEqual(
            Parser.check_edge(),
            (stack_top, stack_bottom) == gold_graph[0],
            f"Parser.check_edge() should return `True` or `False`",
        )

    def test_discard(self):
        stack = [1, 2]
        self.assertEqual(
            Parser.discard(stack), [], f"Parser.discard() returns a totally empty stack"
        )


# class ParserTests(unittest.TestCase):
#     def test_add_special_symbol(self):
#         """`clu.phontools.alignment.parser.Parser.add_special_symbol()` should return 'a string with a special character (-) between its letter/phones'
#         :INPUT: cat
#         :OUTPUT: -c-a-t-
#         """
#         text = "cat"
#         self.assertEqual(
#             Parser.add_special_symbol(text),
#             "-c-a-t-",
#             f"Parser.add_special_symbol() should return '-c-a-t-'",
#         )

