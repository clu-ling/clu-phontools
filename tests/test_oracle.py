# -*- coding: utf-8 -*-

import unittest
from clu.phontools.alignment.realine import ReAline
from clu.phontools.alignment.parser import (
    Oracle,
    Parser,
    Actions,
    Symbol,
    IntermediateSymbol,
    prepare_symbols,
    assign_index,
)


"""
Test `clu.phontools.alignment.parser.prepare_symbols` behaviors
Test `clu.phontools.alignment.parser.assign_index` behaviors
"""


class SymbolsTests(unittest.TestCase):
    def prepare_symbols_test(self):
        """`clu.phontools.alignment.parser.prepare_symbols()` should return the correct enumerations of the actions used by the parser
        """
        text = "cat"
        self.assertEqual(
            Symbol(text),
            "cat",
            f"Symbol() should return 'cat'",
        )
        # symbol = Symbol()
        # text = "cat"
        # self.assertEqual(
        #     prepare_symbols(text),
        #     [NULL, c, NULL, a, NULL, t, NULL],
        #     f"prepare_symbols() should return [NULL, c, NULL, a, NULL, t, NULL]",
        # )

    # def assign_index_test(self):
    #     """`clu.phontools.alignment.parser.assign_index()` should return the correct enumerations of the actions used by the parser
    #     """
    #     # list = [NULL, c, NULL, a, NULL, t, NULL]
    #     # self.assertEqual(
    #     #     Parser.assign_indexs(list),
    #     #     "[(0,NULL), (1,c), NULL, a, NULL, t, NULL]",
    #     #     f"Parser.prepare_symbols() should return [NULL, c, NULL, a, NULL, t, NULL]",
    #     # )
    #     pass


"""
Test `clu.phontools.alignment.parser.Actions` behaviors
"""


# class ActionsTests(unittest.TestCase):
#     def test_actions(self):
#         """`clu.phontools.alignment.parser.Actions.describe()` should return the correct enumerations of the actions used by the parser
#         """
#         assert len(Actions) == 11

#         assert Actions.DISCARD_T.describe() == ("DISCARD_T", 1)
#         assert Actions.DISCARD_G.describe() == ("DISCARD_G", 2)
#         assert Actions.SHIFT_T.describe() == ("SHIFT_T", 3)
#         assert Actions.SHIFT_G.describe() == ("SHIFT_G", 4)
#         assert Actions.STACK_SWAP.describe() == ("STACK_SWAP", 5)
#         assert Actions.INSERTION_PRESERVE_COPY_CHILD.describe() == (
#             "INSERTION_PRESERVE_COPY_CHILD",
#             6,
#         )
#         assert Actions.INSERTION_PRESERVE_COPY_PARENT.describe() == (
#             "INSERTION_PRESERVE_COPY_PARENT",
#             7,
#         )
#         assert Actions.DELETION_PRESERVE_COPY_CHILD.describe() == (
#             "DELETION_PRESERVE_COPY_CHILD",
#             8,
#         )
#         assert Actions.DELETION_PRESERVE_COPY_PARENT.describe() == (
#             "DELETION_PRESERVE_COPY_PARENT",
#             9,
#         )
#         assert Actions.ALIGN.describe() == ("ALIGN", 10)
#         assert Actions.SUBSTITUTION.describe() == ("SUBSTITUTION", 11)


"""
Test `clu.phontools.alignment.parser.Parser` behaviors
"""


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

