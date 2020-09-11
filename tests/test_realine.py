# -*- coding: utf-8 -*-

import unittest
from realine import *


'''
Test alignment of pairs
'''

class ReAlineTests(unittest.TestCase):
    
    def test_same_input(self):

        realiner = ReAline()

        seq = ["θ", "i", "n"]

        self.assertEqual(reliner.align(seq), [[('θ', 'θ'), ('i', 'i'), ('n', 'n')]], "Re-Aline failed to align a sequence with itself.")


    def test_align(self):
        realiner = ReAline()

        assert realiner.align(["θ", "i", "n"], ["θ", "i", "n"])
        assert realiner.align(["θ", "i", "n"], ["t", "e", "n", "w", "i", "s"]) == [[('θ', 't'), ('i', 'e'), ('n', 'n'), ('-', 'w'), ('-', 'i'), ('-', 's')]]

    def test_lexical_boundary(self):

        realiner = ReAline()
    
        # FIXME: decide how LB should be aligned
        assert realiner.align(["θ", "i", "n", "LB"], ["t", "e", "n", "w", "i", "s"]) == [[('θ', 't'), ('i', 'e'), ('n', 'n'), ('-', 'w'), ('LB', 'i'), ('-', 's')]]


    def test_default_class_features(self):

        realiner = ReAline()

        assert realiner.feature_matrix.keys() is not None
        assert len(realiner.feature_matrix.keys()) > 0
        assert realiner.similarity_matrix.keys() is not None
        assert len(realiner.similarity_matrix.keys()) > 0
        assert realiner.salience is not None
        # [c for c in features.consonants if c not in features.feature_matrix.keys()]
