# -*- coding: utf-8 -*-

import unittest
from typing import Sequence
from clu.phontools.struct import *
from clu.phontools.lang.en import EnglishUtils


"""
Test English-specific behaviors
"""


class EnglishTests(unittest.TestCase):
    def test_phrase_lookup(self):
        """"""
        res: Sequence[Phrase] = EnglishUtils.all_possible_phrases_for(
            ["permit", "for", "transport"]
        )
        assert len(res) == 6
