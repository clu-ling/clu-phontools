# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch
from clu.phontools.alignment.realine import ReAline
from clu.phontools.alignment.parser import Symbol, Index, Actions, Parser


"""
Test `clu.phontools.alignment.parser.Symbol()` behaviors
Test `clu.phontools.alignment.parser.Index.prepare_symbols()` behaviors
Test `clu.phontools.alignment.parser.Index.assign_indexes()` behaviors
"""


class SymbolsTests(unittest.TestCase):
    def symbol_test(self):
        """`clu.phontools.alignment.parser.Symbol()` should return the correct enumerations of the actions used by the parser
        """
        text = "cat"
        symbols = Symbol(text)
        self.assertEqual(
            text,
            str(symbols),
            f"Symbol() should return an object which is equal to the given string",
        )

    def prepare_symbols_test(self):
        text = "cat"
        symbols = Index.prepare_symbols(text)
        res = "[NULL, c, NULL, a, NULL, t, NULL]"
        self.assertEqual(
            symbols,
            res,
            f"Index.prepare_symbols() should return an object where a special symbol 'NULL' is inserted between the characters of a given word",
        )

    def assign_index_test(self):
        text = "cat"
        indexes_symbols = (
            "[(0, NULL), (1, c), (2, NULL), (3, a), (4, NULL), (5, t), (6, NULL)]"
        )
        symbols = Index.prepare_symbols(text)
        indexes = Index.assign_index(symbols)
        self.assertEqual(
            indexes_symbols,
            indexes,
            f"Index.prepare_index() should return a list of tuples with indexes and symbols.",
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
    def test_add_special_symbol(self):
        """`clu.phontools.alignment.parser.Parser.add_special_symbol()` should return 'a string with a special character (-) between its letter/phones'
        :INPUT: cat
        :OUTPUT: -c-a-t-
        """
        text = "cat"
        self.assertEqual(
            Parser.add_special_symbol(text),
            "-c-a-t-",
            f"Parser.add_special_symbol() should return '-c-a-t-'",
        )


"""
Test behavior of Oracle
"""


# class OracleTests(unittest.TestCase):
#     def test_hello(self):
#         """`clu.phontools.alignment.parser.Oracle.greet()` should return 'hello'"""

#         self.assertEqual(
#             Oracle.greet(),
#             'Hello',
#             f"Oracle.greet() should return 'hello', but {Oracle.greet()} was returned",
#         )

