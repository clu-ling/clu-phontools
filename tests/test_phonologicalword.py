# -*- coding: utf-8 -*-

import unittest
from clu.phontools.struct import *

"""
Test `clu.phontools.struct.PhonologicalWord` behaviors
"""


class PhonologicalWordTests(unittest.TestCase):
    def test_equality(self):
        """Comparisions of pairs of `clu.phontools.struct.PhonologicalWord` should account for differences in `clu.phontools.struct.PhonologicalWord.phones` and `clu.phontools.struct.PhonologicalWord.stress_pattern`."""

        # change .phones
        pw1: PhonologicalWord = PhonologicalWord(
            phones=("P", "ER0", "M", "IH1", "T"),
            stress_pattern=[
                Stress.NON_VOWEL,
                Stress.NO_STRESS,
                Stress.NON_VOWEL,
                Stress.PRIMARY,
                Stress.NON_VOWEL,
            ],
        )
        pw2: PhonologicalWord = PhonologicalWord(
            phones=("P", "ER0", "M", "IH1", "P"),
            stress_pattern=[
                Stress.NON_VOWEL,
                Stress.NO_STRESS,
                Stress.NON_VOWEL,
                Stress.PRIMARY,
                Stress.NON_VOWEL,
            ],
        )
        self.assertNotEqual(pw1, pw2)

        # change .stress_pattern
        pw1: PhonologicalWord = PhonologicalWord(
            phones=("P", "ER0", "M", "IH1", "T"),
            stress_pattern=[
                Stress.NON_VOWEL,
                Stress.NO_STRESS,
                Stress.NON_VOWEL,
                Stress.PRIMARY,
                Stress.NON_VOWEL,
            ],
        )
        pw2: PhonologicalWord = PhonologicalWord(
            phones=("P", "ER0", "M", "IH1", "T"),
            stress_pattern=[
                Stress.NON_VOWEL,
                Stress.PRIMARY,
                Stress.NO_STRESS,
                Stress.NON_VOWEL,
                Stress.NO_STRESS,
                Stress.NON_VOWEL,
            ],
        )
        self.assertNotEqual(pw1, pw2)
