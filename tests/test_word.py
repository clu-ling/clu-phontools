# -*- coding: utf-8 -*-

import unittest
from clu.phontools.struct import *

"""
Test `clu.phontools.struct.Word` behaviors
"""


class WordTests(unittest.TestCase):
    def test_equality(self):
        """Comparisions of pairs of `clu.phontools.struct.Word` should account for differences in `clu.phontools.struct.Word.word` and `clu.phontools.struct.phonological_form`."""

        # change .word
        w1: Word = Word(
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
        )
        w2: Word = Word(
            word="permt",
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
        )
        self.assertNotEqual(w1, w2)

        # change .pf.phones
        w1: Word = Word(
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
        )
        w2: Word = Word(
            word="permt",
            phonological_form=PhonologicalWord(
                phones=("P", "ER0", "M", "IH1", "P"),
                stress_pattern=[
                    Stress.NON_VOWEL,
                    Stress.NO_STRESS,
                    Stress.NON_VOWEL,
                    Stress.PRIMARY,
                    Stress.NON_VOWEL,
                ],
            ),
        )
        self.assertNotEqual(w1, w2)

        # change .pf.stress_pattern
        w1: Word = Word(
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
        )
        w2: Word = Word(
            word="permt",
            phonological_form=PhonologicalWord(
                phones=("P", "ER0", "M", "IH1", "T"),
                stress_pattern=[
                    Stress.NON_VOWEL,
                    Stress.PRIMARY,
                    Stress.NO_STRESS,
                    Stress.NON_VOWEL,
                    Stress.NO_STRESS,
                    Stress.NON_VOWEL,
                ],
            ),
        )
        self.assertNotEqual(w1, w2)
