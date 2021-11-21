from __future__ import annotations
from .symbols import Symbol, TranscriptTypes
from .graph import Graph


class Constraints:
    """
    Constraints used to validate Actions and guide our Oracle
    """

    @staticmethod
    def stack_top_two_different_sources(stack: Stack) -> bool:
        """
        True iff
        1) stack has >= 2 items AND
        2) top 2 items on the stack have different TranscriptTypes.
        """
        _stack = stack.copy()
        if len(stack) >= 2:
            s1 = _stack.pop()
            s2 = _stack.pop()
            # must have different TranscriptTypes
            # TODO: do we want to enforce an order here?
            return len(set([s1.source, s2.source])) > 1
        return False

    @staticmethod
    def participates_in_an_edge(symbol: Symbol, graph: Graph) -> bool:
        """
        Checks if the provided Symbol participates in some Edge
        """
        nodes = {node for edge in graph.edges for node in edge.nodes()}
        return symbol in nodes

    @staticmethod
    def is_a_parent(self, symbol: Symbol, graph: Graph) -> bool:
        """
        Checks if the provided Symbol is a parent (source) in some Edge
        """
        parents = {edge.source for edge in graph.edges}
        return symbol in parents

    @staticmethod
    def is_a_child(self, symbol: Symbol, graph: Graph) -> bool:
        """
        Checks if the provided Symbol is a child (destination) in some Edge
        """
        children = {edge.destination for edge in graph.edges}
        return symbol in children
