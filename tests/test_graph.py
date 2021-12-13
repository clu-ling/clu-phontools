# -*- coding: utf-8 -*-

import unittest
from clu.phontools.alignment.parser import *


"""
Test behavior of clu.phontools.alignment.parser.graph.Edge
"""


class EdgeTests(unittest.TestCase):
    def test_nodes(self):
        """`clu.phontools.alignment.parser.graph.Edge.nodes` should return a list of source and destination symbols."""
        source = Symbol(
            original_index=0, index=0, symbol="a", source=TranscriptTypes.TRANSCRIPT
        )
        destination = Symbol(
            original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD
        )
        label = Actions.ALIGN
        edge = Edge(source, destination, label)
        nodes = edge.nodes()

        self.assertTrue(len(nodes) == 2, f"len(Queue()) should be 2")


"""
Test behavior of clu.phontools.alignment.parser.graph.Graph
"""


class GraphTests(unittest.TestCase):
    pass
