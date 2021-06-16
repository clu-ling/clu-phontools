# -*- coding: utf-8 -*-

import unittest
from clu.phontools.alignment.realine import ReAline, PhonemeErrors


"""
Test alignment of pairs
"""


class ReAlineTests(unittest.TestCase):
    def test_same_input(self):
        """`clu.phontools.alignment.realine.ReAline.align()` should align the same sequence with itself."""

        aligner = ReAline()

        seq = ["θ", "i", "n"]

        self.assertEqual(
            aligner.align(seq, seq),
            [("θ", "θ"), ("i", "i"), ("n", "n")],
            "Re-Aline failed to align a sequence with itself.",
        )

    def test_align(self):
        """`clu.phontools.alignment.realine.ReAline.align()` should be able to align different sequences of phones."""
        aligner = ReAline()

        seq1 = ["θ", "i", "n"]
        seq2 = ["t", "e", "n", "w", "i", "s"]
        expected = [
            ("θ", "t"),
            ("i", "e"),
            ("n", "n"),
            ("-", "w"),
            ("-", "i"),
            ("-", "s"),
        ]
        res = aligner.align(seq1, seq2)
        self.assertEqual(
            res,
            expected,
            f"`clu.phontools.alignment.realine.ReAline.align({seq1}, {seq2})` should produce {expected}, but instead generated {res}",
        )

    # def test_lexical_boundary(self):

    #     aligner = ReAline()

    #     # FIXME: decide how LB should be aligned
    #     assert aligner.align(
    #         ["θ", "i", "n", "LB"], ["t", "e", "n", "w", "i", "s"]
    #     ) == [[("θ", "t"), ("i", "e"), ("n", "n"), ("-", "w"), ("LB", "i"), ("-", "s")]]

    def test_default_class_features(self):
        """Instances of `clu.phontools.alignment.realine.ReAline` should have class attributes set."""

        aligner = ReAline()

        assert aligner.feature_matrix.keys() is not None
        assert len(aligner.feature_matrix.keys()) > 0
        assert aligner.similarity_matrix.keys() is not None
        assert len(aligner.similarity_matrix.keys()) > 0
        assert aligner.salience is not None
        # [c for c in features.consonants if c not in features.feature_matrix.keys()]

    def test_phoneme_errors(self):
        """`clu.phontools.alignment.realine.ReAline.phoneme_errors()` should accurately count insertions, deletions, and substitutions for aligned pairs."""
        alignments = [("æ", "-"), ("-", "d"), ("v", "v"), ("æ", "ɛ")]
        predicted = ReAline.phoneme_errors(alignments)
        expected = PhonemeErrors(
            insertions=[("-", "d")], deletions=[("æ", "-")], substitutions=[("æ", "ɛ")]
        )
        self.assertEqual(
            predicted,
            expected,
            f"Testing phoneme errors failed. Expected {expected}, but received {predicted}",
        )
