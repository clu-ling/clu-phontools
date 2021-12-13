from __future__ import annotations
from .symbols import Symbol, TranscriptTypes
from .graph import Graph
from .stack import Stack
from .queue import Queue

__all__ = ["Constraints"]


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
            s1 = _stack.pop()  # gold
            s2 = _stack.pop()  # trans
            # must have different TranscriptTypes
            # TODO: do we want to enforce an order here?
            # NOTE: in the test case, we push trans then the gold. when we apply this constraint
            # s1 will be gold and s2 will be trans. I do not think order matters?!
            return len(set([s1.source, s2.source])) > 1
            # return len(set([s2.source, s1.source])) > 1
        return False

    @staticmethod
    def participates_in_an_edge(symbol: Symbol, graph: Graph) -> bool:
        """
        Checks if the provided Symbol participates in some Edge
        """
        nodes = {node for edge in graph.edges for node in edge.nodes()}
        return symbol in nodes

    @staticmethod
    def is_a_parent(symbol: Symbol, graph: Graph) -> bool:
        """
        Checks if the provided Symbol is a parent (source) in some Edge
        """
        parents = {edge.source for edge in graph.edges}
        return symbol in parents

    @staticmethod
    def is_a_child(symbol: Symbol, graph: Graph) -> bool:
        """
        Checks if the provided Symbol is a child (destination) in some Edge
        """
        children = {edge.destination for edge in graph.edges}
        return symbol in children

    @staticmethod
    def many_to_one_and_vice_versa(trans_queue: Queue, gold_queue: Queue) -> bool:
        """checks the length of both queues to validate the discard action"""
        # the logic is to check the length of QUEUES
        # If the TRANS is Longer, then it is many-to-one
        # Otherwise, it is one-to-many
        # based on that, Discard is applied to get rid of the NULL symbol from the transcript.
        # push trans (NULL) - push gold (NULL) we have to do another two pushes here
        # if both are NULL, then we discard them
        return True if trans_queue != gold_queue else False
