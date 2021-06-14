# -*- coding: utf-8 -*-

import unittest
from clu.phontools.struct import *


"""
Test `clu.phontools.struct.Phrase` behaviors
"""


class PhraseTests(unittest.TestCase):

    phrase1: Phrase = Phrase(
        words=(
            Word(
                word="permit",
                phonological_form=PhonologicalWord(
                    phones=("P", "ER0", "M", "IH1", "T"),
                    stress_pattern=[
                        Stress.NON_VOWEL,
                        Stress.NO_STRESS,
                        Stress.NON_VOWEL,
                        Stress.PRIMARY,
                        Stress.NON_VOWEL,
                    ],
                ),
            ),
            Word(
                word="me",
                phonological_form=PhonologicalWord(
                    phones=("M", "IY1"),
                    stress_pattern=[Stress.NON_VOWEL, Stress.PRIMARY],
                ),
            ),
            Word(
                word="to",
                phonological_form=PhonologicalWord(
                    phones=("T", "UW1"),
                    stress_pattern=[Stress.NON_VOWEL, Stress.PRIMARY],
                ),
            ),
            Word(
                word="ask",
                phonological_form=PhonologicalWord(
                    phones=("AE1", "S", "K"),
                    stress_pattern=[Stress.PRIMARY, Stress.NON_VOWEL, Stress.NON_VOWEL],
                ),
            ),
        )
    )

    def test_phrase(self):
        """A `clu.phontools.struct.Phrase` should have a coarse_stress property and mask_stress method."""

        phrase: Phrase = Phrase.Tests.phrase1
        # syllable structure in terms of stress (weak or strong)
        # should return ['WS', 'S', 'S', 'S']
        assert phrase.coarse_stress == ["WS", "S", "S", "S"]

        # num. syllables for each word represented using a mask.
        # should return ['XX', 'X', 'X', 'X']
        assert phrase.mask_syllables(mask="X") == ["XX", "X", "X", "X"]
