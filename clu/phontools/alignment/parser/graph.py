from __future__ import annotations
from .symbols import ParseSymbol
from .actions import Actions
from dataclasses import dataclass, field
from typing import List

__all__ = ["Graph", "Edge"]


@dataclass
class Graph:
    edges: List[Edge] = field(default_factory=list)

    # FIXME: implement me
    def has_children(self, ps: ParseSymbol) -> bool:
        # go over the edges and check which is the source and the destination
        pass

    def copy(self) -> Graph:
        """Creates a copy of the graph at this stage"""
        return Graph(edges=edges[:])


@dataclass
class Edge:
    """"""

    source: ParseSymbol
    destination: ParseSymbol
    label: Actions
