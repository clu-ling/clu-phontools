# -*- coding: utf-8 -*-

import unittest
import typing
from typing import Sequence
# import clu.phontools.parser 
from clu.phontools.parser import *


"""
Test parser process behaviors
"""

# class SymbolTests(unittest.TestCase): 
# #     pass
#     """ Test `clu.phontools.paraser.Symbol` which converts a string  as a symbol"""
    



# class IntermediateSymbolTest(unittest.TestCase): 
#     pass
#     """ Test `clu.phontools.paraser.IntermediateSymbol` which inserts 
#     'NULL' between every character of a string
#     """
#     # self.assertEqual()

class IndexTests(unittest.TestCase):
    """ Test `clu.phontools.paraser.Index` which assigns index to each
      character of a string, and returns both index and character
       in a list of tuples 
    """
    def test_prepare_symbols(self):
        print('mohammed')
        self.assertEqual(Index.prepare_symbols('cat'), ['NULL', 'c', 'NULL', 'a', 'NULL', 't', 'NULL'])
    def test_assign_index(self):
        self.assertEqual(Index.assign_index(Index.prepare_symbols('cat')),
         [(0, 'NULL'), (1, 'c'), (2, 'NULL'),(3, 'a'), (4, 'NULL'),
         (5, 't'), (6, 'NULL')])

# class ActionsTests(unittest.TestCase): pass

class StateTests(unittest.TestCase): 
    def test_gold_queue(self):
        state = State('cat', 'cat')
        self.assertEqual(state.gold_queue(), [(0, 'NULL'),(1, 'c'),(2, 'NULL'),
        (3, 'a'),(4, 'NULL'),(5, 't'),(6, 'NULL')])
    def test_transcribed_queue(self):
        state = State('cat', 'cat')
        self.assertEqual(state.transcribed_queue(), [(0, 'NULL'),(1, 'c'),(2, 'NULL'),
        (3, 'a'),(4, 'NULL'),(5, 't'),(6, 'NULL')])

    def test_realine_output(self):
        state = State('cat', 'cat')
        self.assertEqual(state.realine_output(), [('c', 'c'), ('a', 'a'), ('t', 't')])
    def test_graph(self):
        state = State('cat', 'cat')
        self.assertEqual(state.graph(), [('c', 'align', 'c'), ('a', 'align', 'a'), ('t', 'align', 't')])


# class EdgeTests(unittest.TestCase): pass


# class StackTests(unittest.TestCase): pass
