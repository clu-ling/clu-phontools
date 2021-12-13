from __future__ import annotations
from .symbols import Symbol, TranscriptTypes
from .actions import Actions
from dataclasses import dataclass, field
from typing import List, Dict, List, Text, Tuple
from networkx.drawing.nx_pydot import to_pydot
from networkx.drawing.nx_agraph import to_agraph
import pygraphviz as pgv
import networkx as nx
import pydot

__all__ = ["Graph", "Edge"]


@dataclass
class Graph:
    """An alignment graph mapping transcribed phones to gold phones along with the relationship (deletion, substitution, alignment, etc.)"""

    edges: List[Edge] = field(default_factory=list)  # Graph(edges=[]) #

    def __post_init__(self):
        ps2children: Dict[Symbol, List[Symbol]] = dict()
        G = nx.DiGraph()
        for edge in self.edges:
            G.add_nodes_from(
                [self._nx_make_node(edge.source), self._nx_make_node(edge.destination)]
            )
            G.add_edge(
                self._nx_make_node_id(edge.source),
                self._nx_make_node_id(edge.destination),
                label=edge.label.simple(),
            )
            if edge.source != edge.destination:
                children = ps2children.get(edge.source, [])
                children.append(edge.destination)
                ps2children[edge.source] = children
        # mapping of node to its children
        self._children: Dict[Symbol, List[Symbol]] = ps2children
        # networkx DiGraph
        self.G = G

    def children_for(self, ps: Symbol) -> List[Symbol]:
        """Retrieves children for the provided Symbol ps."""
        return self._children.get(ps, [])

    def has_children(self, ps: Symbol) -> bool:
        """Checks whether provided Symbol ps has children."""
        return ps.source in self._children

    def copy(self) -> Graph:
        """Creates a copy of the graph at this stage"""
        return Graph(edges=edges[:])

    def _nx_make_node_id(self, ps: Symbol) -> Text:
        return f"{str(ps.source)}-{ps.symbol}-{ps.index}"

    def _nx_make_node(self, ps: Symbol) -> Tuple[Text, Dict[Text, Text]]:
        return (
            self._nx_make_node_id(ps),
            {
                "label": ps.symbol,
                "shape": "box" if ps.source == TranscriptTypes.GOLD else "circle",
            },
        )

    def _dot_with_tiered_view(self, G: nx.Graph) -> Text:
        """converts nx.Graph to pygraphviz.AGraph,
        add subgraphs for a tiered view,
        and returns dot"""
        AG = to_agraph(G)
        gold = set()
        transcribed = set()
        for edge in self.edges:
            for node in (edge.source, edge.destination):
                nx_id = self._nx_make_node_id(node)
                if node.source == TranscriptTypes.GOLD:
                    gold.add(nx_id)
                elif node.source == TranscriptTypes.TRANSCRIPT:
                    transcribed.add(nx_id)
        AG.add_subgraph(sorted(list(gold)), rank="min")
        AG.add_subgraph(sorted(list(transcribed)), rank="max")
        return AG.string()

    def to_dot(self) -> Text:
        """Dot-based representation of the alignment graph."""
        return self._dot_with_tiered_view(self.G)


@dataclass
class Edge:
    """
    this class returns an `Edge` object.
    Edge(
        source=Symbol(
            original_index=0, index=0, symbol="a", source=TranscriptTypes.TRANSCRIPT
            ), 
        destination=Symbol(
            original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD
            ), 
        label=Actions.ALIGN
        )
    """

    source: Symbol
    destination: Symbol
    label: Actions

    def nodes(self) -> List[Symbol]:
        """Distinct nodes (Symbols) in Edge"""
        return list(set([source, destination]))
