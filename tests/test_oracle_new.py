# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch
from collections import deque
from clu.phontools.alignment.realine import ReAline
from clu.phontools.alignment.parser import (
    Symbol,
    IntermediateSymbol,
    Index,
    State,
    Actions,
    Parser,
    RealineOutput,
    GetPhones,
    ParseSymbol,
    stack_is_empty,
    check_len_stack,
    TranscriptTypes,
)
from clu.phontools.lang.en import EnglishUtils
from clu.phontools.struct import *
from clu.phontools.pronouncing import ConverterUtils
from clu.phontools.alignment.realine import *
from clu.phontools.alignment.lbe import *

"""
Test `clu.phontools.alignment.GetPhones` behaviors
"""


class TestGetPhones(unittest.TestCase):
    def test_raw_phrase_to_phone_sets(self):
        """`clu.phontools.alignment.GetPhones.raw_phrase_to_phone_sets` outputs List[List[Phones]]."""

        gold = "cat in the hat"
        transcript = "canyon cat"

        gold_phones = GetPhones(gold).raw_phrase_to_phone_sets
        transcript_phones = GetPhones(transcript).raw_phrase_to_phone_sets

        gold_result = [
            ["K", "AE1", "T", "IH0", "N", "DH", "AH0", "HH", "AE1", "T"],
            ["K", "AE1", "T", "IH0", "N", "DH", "AH1", "HH", "AE1", "T"],
            ["K", "AE1", "T", "IH0", "N", "DH", "IY0", "HH", "AE1", "T"],
            ["K", "AE1", "T", "IH1", "N", "DH", "AH0", "HH", "AE1", "T"],
            ["K", "AE1", "T", "IH1", "N", "DH", "AH1", "HH", "AE1", "T"],
            ["K", "AE1", "T", "IH1", "N", "DH", "IY0", "HH", "AE1", "T"],
        ]
        transcript_result = [["K", "AE1", "N", "Y", "AH0", "N", "K", "AE1", "T"]]
        self.assertEqual(
            gold_phones,
            gold_result,
            f"clu.phontools.alignment.GetPhones(gold={gold}).raw_phrase_to_phone_set produced {gold_result}",
        )
        self.assertEqual(
            transcript_phones,
            transcript_result,
            f"clu.phontools.alignment.GetPhones(gold={transcript}).raw_phrase_to_phone_set produced {transcript_result}",
        )

    def test_random_member_of_the_phone_set(self):
        """`clu.phontools.alignment.GetPhones.random_member_of_the_phone_set` randomly chooses a list of phones."""
        gold = "cat in the hat"
        transcript = "canyon cat"
        chosen_gold = GetPhones(gold).random_member_of_the_phone_set
        chosen_transcript = GetPhones(transcript).random_member_of_the_phone_set
        assert chosen_gold == 1
        assert chosen_transcript == 1

    def test_to_ipa(self):
        """`clu.phontools.alignment.GetPhones.to_ipa` takes the chosen gold and transcript Arpabet and converts them to ipa symbols."""
        gold = "cat in the hat"
        transcript = "canyon cat"

        gold_ipa = GetPhones(gold).to_ipa
        transcript_ipa = GetPhones(transcript).to_ipa

        gold_res = ["k", "æ", "t", "i", "n", "ð", "ʌ", "h", "æ", "t"]
        transcript_res = ["k", "æ", "n", "j", "ʌ", "n", "k", "æ", "t"]

        self.assertEqual(
            gold_ipa,
            gold_res,
            f"clu.phontools.alignment.GetPhones(gold={gold}).to_ipa produced {gold_res}",
        )
        self.assertEqual(
            transcript_ipa,
            transcript_res,
            f"clu.phontools.alignment.GetPhones(gold={transcript}).to_ipa produced {transcript_res}",
        )


"""
Test `clu.phontools.alignment.RealineOutput` behaviors
"""


class TestRealineOutput(unittest.TestCase):
    def test_alignments(self):
        """`clu.phontools.alignment.RealineOutput.alignments` outpust List[Tuples[Phones, ...]]"""

        gold = "cat in the hat"
        transcript = "canyon cat"

        output = ReAline.alignments

        res = [
            ("k", "k"),
            ("æ", "æ"),
            ("t", "-"),
            ("-", "n"),
            ("-", "j"),
            ("i", "ʌ"),
            ("n", "n"),
            ("ð", "-"),
            ("-", "k"),
            ("ʌ", "æ"),
            ("h", "-"),
            ("æ", "-"),
            ("t", "t"),
        ]
        self.assertEqual(
            output,
            res,
            f"clu.phontools.alignment.RealineOutput.alignments produced {res}",
        )

    def test_realine_graph(self):
        """`clu.phontools.alignment.RealineOutput.realine_graph()` outputs List[List[Tuples]].
        Each tuple represents a state. In other words, each tuple contains: the gold symbol, the lable and the transcript symbol.
        
        :Input: 2 strings (Gold: cat in the hat) and (transcript: canyon cat)
        :Output: Graph (i.e. List[State])
        """
        alignments = [
            ("k", "k"),
            ("æ", "æ"),
            ("t", "-"),
            ("-", "n"),
            ("-", "j"),
            ("i", "ʌ"),
            ("n", "n"),
            ("ð", "-"),
            ("-", "k"),
            ("ʌ", "æ"),
            ("h", "-"),
            ("æ", "-"),
            ("t", "t"),
        ]

        output = RealineOutput.realine_graph(alignments)

        res = [
            ("k", "align", "k"),
            ("æ", "align", "æ"),
            ("t", "deletion", "-"),
            ("-", "inserion", "n"),
            ("-", "inserion", "j"),
            ("i", "substitution", "ʌ"),
            ("n", "align", "n"),
            ("ð", "deletion", "-"),
            ("-", "inserion", "k"),
            ("ʌ", "substitution", "æ"),
            ("h", "deletion", "-"),
            ("æ", "deletion", "-"),
            ("t", "align", "t"),
        ]
        self.assertEqual(
            output,
            res,
            f"clu.phontools.alignment.RealineOutput.realine_graph({alignments}) produced {res}",
        )


"""
Test `clu.phontools.alignment` behaviors
Testing some actions
"""


class TestSomeMethodsNecessaryForOracle(unittest.TestCase):
    def test_stack_is_empty(self):
        """`clu.phontools.alignment.stack_is_empty` returns a bool value"""
        stack = deque()
        res = stack_is_empty(stack)
        assert res == True

    def test_check_len_stack(self):
        """`clu.phontools.alignment.check_len_stack` returns a bool value"""
        stack = deque(["æ", "æ"])
        res = check_len_stack(stack)
        assert res == 2

    def test_pop_for_queue(self):
        """`clu.phontools.alignment.pop_for_queue` returns the queue and deletes the item on the left end of the queue """
        queue = deque(["NULL", "æ"])
        res = pop_for_queue(queue)

        desired_res = deque(["æ"])  # or stack

        self.assertEqual(
            res,
            desired_res,
            f"clu.phontools.alignment.pop_for_stack({queue}) produced {desired_res}",
        )

    def test_pop_for_stack(self):
        """`clu.phontools.alignment.pop_for_stack` returns the stack and deletes the item on the right end of the queue"""
        stack = deque(["æ", "æ"])
        res = pop_for_stack(stack)

        desired_res = deque(["æ"])  # or stack

        self.assertEqual(
            res,
            desired_res,
            f"clu.phontools.alignment.pop_for_stack({stack}) produced {desired_res}",
        )

    def test_shift(self):
        """`clu.phontools.alignment.shift` performs two functions: 1) takes the item on the left end  and inserts it on the left end (index 0) in the stack"""
        stack = deque()
        queue = deque(["NULL", "æ"])

        res = shift(stack, queue)

        desired_stack = stack
        desired_queue = queue
        assert len(stack) != len(desired_stack)
        assert len(queue) != len(desired_queue)

    def test_discard(self):
        pass

    def test_swap_stack(self):
        pass

    def test_check_edge(self):
        pass


"""
Test `clu.phontools.alignment.ParseSymbol` behaviors
"""


class TestParseSymbol(unittest.TestCase):
    def test_generate_queues(self):
        """`clu.phontools.alignment.ParseSymbol.generate_queues` returns a ParseSymbol object"""

        queue = [
            (0, "NULL"),
            (1, "c"),
            (2, "NULL"),
            (3, "a"),
            (4, "NULL"),
            (5, "t"),
            (6, "NULL"),
        ]

        output = ParseSymbol.parse(queue)

        gold_queue = [
            ParseSymbol(
                symbol="NULL", original_index=-1, index=0, source=TranscriptTypes.GOLD
            ),
            ParseSymbol(
                symbol="c", original_index=0, index=1, source=TranscriptTypes.GOLD
            ),
            ParseSymbol(
                symbol="NULL", original_index=-1, index=2, source=TranscriptTypes.GOLD
            ),
            ParseSymbol(
                symbol="a", original_index=1, index=3, source=TranscriptTypes.GOLD
            ),
            ParseSymbol(
                symbol="NULL", original_index=-1, index=4, source=TranscriptTypes.GOLD
            ),
            ParseSymbol(
                symbol="t", original_index=2, index=5, source=TranscriptTypes.GOLD
            ),
            ParseSymbol(
                symbol="NULL", original_index=-1, index=6, source=TranscriptTypes.GOLD
            ),
        ]
        self.assertEqual(
            output,
            gold_queue,
            f"clu.phontools.alignment.ParseSymbol.generate_queues({queue}) produced {gold_queue}",
        )

