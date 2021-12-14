# -*- coding: utf-8 -*-

import unittest
from clu.phontools.alignment.parser import *


"""
Test behavior of clu.phontools.alignment.parser.utils.ReAlineOutputUtils
"""


class UtilsTests(unittest.TestCase):
    def test_to_symbol(self):
        """`clu.phontools.alignment.parser.utils.ReAlineOutputUtils.to_symbol` should convert a text into a list of `Symbol` object."""
        transcript = "cat"  # this can be gold
        list_of_symbol_object = [
            Symbol(symbol="NULL", original_index=-1, index=0, source="TRANSCRIPT"),
            Symbol(symbol="k", original_index=0, index=1, source="TRANSCRIPT"),
            Symbol(symbol="NULL", original_index=-1, index=2, source="TRANSCRIPT"),
            Symbol(symbol="æ", original_index=1, index=3, source="TRANSCRIPT"),
            Symbol(symbol="NULL", original_index=-1, index=4, source="TRANSCRIPT"),
            Symbol(symbol="t", original_index=2, index=5, source="TRANSCRIPT"),
            Symbol(symbol="NULL", original_index=-1, index=6, source="TRANSCRIPT"),
        ]
        res = utils.ReAlineOutputUtils.to_symbol(
            text=transcript, source=TranscriptTypes.TRANSCRIPT.value
        )
        self.assertEqual(
            res,
            list_of_symbol_object,
            f"`clu.phontools.alignment.parser.utils.ReAlineOutputUtils.to_symbol({transcript})` should return {list_of_symbol_object} ",
        )

    def test_realine_output(self):
        """`clu.phontools.alignment.parser.utils.ReAlineOutputUtils.realine_output` should a list of tuples of transcript and gold symbols as well as their label"""
        transcript = "cat"
        gold = "cat"

        mappings = [
            ("c", "align", "c"),
            ("a", "align", "a"),
            ("t", "align", "t"),
            ("-", "inserion", "s"),
        ]
        res = utils.ReAlineOutputUtils.realine_output(transcript, gold)

        self.assertEqual(
            res,
            mappings,
            f"`clu.phontools.alignment.parser.utils.ReAlineOutputUtils.realine_output({transcript, gold})` should return {mappings} ",
        )

    def test_to_graph(self):
        """`clu.phontools.alignment.parser.utils.ReAlineOutputUtils.to_graph` should construct edges based on realine output and return the Graph object"""
        # realine_output = [
        #     ("c", "align", "c"),
        #     ("a", "align", "a"),
        #     ("t", "align", "t"),
        #     ("-", "insertion", "s"),
        # ]
        transcript = "cat" # ---> source
        gold = "cats"      # ---> destination
        graph = Graph(
            Edge(source=Symbol(symbol='NULL', original_index=-1, index=0, source='TRANSCRIPT'), destination=Symbol(symbol='NULL', original_index=-1, index=0, source='GOLD'), label='ALIGN'),
            Edge(source=Symbol(symbol='k', original_index=0, index=1, source='TRANSCRIPT'), destination=Symbol(symbol='k', original_index=0, index=1, source='GOLD'), label='ALIGN'),
            Edge(source=Symbol(symbol='NULL', original_index=-1, index=2, source='TRANSCRIPT'), destination=Symbol(symbol='NULL', original_index=-1, index=2, source='GOLD'), label='ALIGN'),
            Edge(source=Symbol(symbol='æ', original_index=1, index=3, source='TRANSCRIPT'), destination=Symbol(symbol='æ', original_index=1, index=3, source='GOLD'), label='ALIGN'),
            Edge(source=Symbol(symbol='NULL', original_index=-1, index=4, source='TRANSCRIPT'), destination=Symbol(symbol='NULL', original_index=-1, index=4, source='GOLD'), label='ALIGN'),
            Edge(source=Symbol(symbol='t', original_index=2, index=5, source='TRANSCRIPT'), destination=Symbol(symbol='t', original_index=2, index=5, source='GOLD'), label='ALIGN'),
            Edge(source=Symbol(symbol='NULL', original_index=-1, index=6, source='TRANSCRIPT'), destination=Symbol(symbol='NULL', original_index=-1, index=6, source='GOLD'), label='ALIGN'),
            Edge(source=Symbol(symbol='-', original_index=3, index=7, source='TRANSCRIPT'), destination=Symbol(symbol='s', original_index=3, index=7, source='GOLD'), label='INSERTION_PRESERVE_PARENT'),
            Edge(source=Symbol(symbol='-', original_index=-1, index=8, source='TRANSCRIPT'), destination=Symbol(symbol='NULL', original_index=-1, index=8, source='GOLD'), label='INSERTION_PRESERVE_CHILD')
        )
        res = utils.ReAlineOutputUtils.to_graph(transcript, gold)

        self.assertEqual(
            res,
            graph,
            f"`clu.phontools.alignment.parser.utils.ReAlineOutputUtils.realine_output({transcript, gold})` should return {graph} ",
        )
