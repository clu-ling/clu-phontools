# -*- coding: utf-8 -*-

import unittest
from clu.phontools.alignment.realine import ReAline
from clu.phontools.alignment.parser import Oracle


"""
Test behavior of Oracle
"""


class OracleTests(unittest.TestCase):
    def test_hello(self):
        """`clu.phontools.alignment.parser.Oracle.greet()` should return 'hello'"""



        self.assertEqual(
            Oracle.greet(),
            'Hello',
            f"Oracle.greet() should return 'hello', but {Oracle.greet()} was returned",
        )

 
