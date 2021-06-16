# -*- coding: utf-8 -*-

import unittest
from clu.phontools.struct import *
from .utils import phrase1

"""
Test `clu.phontools.struct.Phrase` behaviors
"""


class PhraseTests(unittest.TestCase):

    phrase1: Phrase = phrase1

    def test_equality(self):
        """Comparisions of pairs of `clu.phontools.struct.Phrase` should be sensitive to the order of `clu.phontools.struct.Phrase.words`."""

        phrase: Phrase = PhraseTests.phrase1
        # the order of words matters in a phrase
        phrase2 = Phrase(words=phrase1.words[-1::])
        self.assertNotEqual(phrase1, phrase2)

    def test_coarse_stress(self):
        """A `clu.phontools.struct.Phrase` should have a coarse_stress property and mask_stress method."""

        phrase: Phrase = PhraseTests.phrase1
        # syllable structure in terms of stress (weak or strong)
        # should return ['WS', 'S', 'S', 'S']
        self.assertEqual(phrase.coarse_stress, ["WS", "S", "S", "S"])

    def test_mask_syllables(self):
        """A `clu.phontools.struct.Phrase.mask_syllables` should mask strong (S) and weak (W) stress."""

        phrase: Phrase = PhraseTests.phrase1
        # num. syllables for each word represented using a mask.
        # should return ['XX', 'X', 'X', 'X']
        self.assertEqual(phrase.mask_syllables(mask="X"), ["XX", "X", "X", "X"])
