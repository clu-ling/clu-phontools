# -*- coding: utf-8 -*-

import unittest
from clu.phontools.pronouncing import *

"""
Test `clu.phontools.pronouncing.ConverterUtils` behaviors
"""


class ConverterUtilsTests(unittest.TestCase):
    def test_arpabet_to_ipa(self):
        """`clu.phontools.pronouncing.ConverterUtils.arpabet_to_ipa()` should convert arpabet symbols to IPA."""

        arpa2ipa_tests = {
            "AE": "æ",
            "AE0": "æ",
            "AE1": "æ",
            "AH": "ʌ",
            "AO": "ɔ",
            "AW": "aʊ",
            "AY": "ai",
            "B": "b",
            "CH": "tʃ",
        }.items()
        for (input_symbol, expected) in arpa2ipa_tests:
            res = ConverterUtils.arpabet_to_ipa(input_symbol)
            self.assertEqual(
                res,
                expected,
                f"`clu.phontools.pronouncing.ConverterUtils.arpabet_to_ipa({input_symbol})` should return {expected}, but instead produced {res}",
            )

    def test_ipa_to_arpabet(self):
        """`clu.phontools.pronouncing.ConverterUtils.ipa_to_arpabet()` should convert IPA symbols to arpabet."""

        ipa2arpa_tests = {
            "æ": "AE",
            "ʌ": "AH",
            "ɔ": "AO",
            "aʊ": "AW",
            "ai": "AY",
            "b": "B",
            "tʃ": "CH",
        }.items()
        for (input_symbol, expected) in ipa2arpa_tests:
            res = ConverterUtils.ipa_to_arpabet(input_symbol)
            self.assertEqual(
                res,
                expected,
                f"`clu.phontools.pronouncing.ConverterUtils.ipa_to_arpabet({input_symbol})` should return {expected}, but instead produced {res}",
            )
