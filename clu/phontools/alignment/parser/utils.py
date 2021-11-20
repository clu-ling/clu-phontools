from __future__ import annotations
from .graph import *
from .symbols import *
from .stack import *
from .state import *
from .queue import *
from typing import List, Text, Tuple

__all__ = ["ReAlineOutputUtils"]


class ReAlineOutputUtils:
    """ """

    # TODO: @Sayed, implement this
    @staticmethod
    def to_symbols(text: Text, source: TranscriptTypes) -> List[ParseSymbol]:
        # "I like turtles" -> [
        # ParseSymbol(original_index=-1, index=0, symbol="NULL", source=source),
        # ParseSymbol(original_index=0, index=1, symbol="AI", source=source)
        # ...
        # ParseSymbol(original_index=-1, index=10, symbol="NULL", source=source)
        # ]
        symbols = []
        # insert NULL, create ParseSymbol instances, and append to symbols
        return symbols

    # TODO: @Sayed, implement this by "peeking into the future"
    @staticmethod
    def to_graph(
        symbols: List[ParseSymbol], realine_output: List[Tuple[Text, Text, Text]]
    ) -> Graph:
        """"""
        # 1. create Edges
        edges = []
        # for step in realine_output: create an edge and append
        return Graph(edges=edges)

    @staticmethod
    def get_states(gold: Text, transcribed: Text, realine_output) -> Graph:
        """"""
        # 1. get parse symbols
        gold_symbols = ReAlineOutputUtils.to_symbols(gold, source=TranscriptTypes.GOLD)
        transcript_symbols = ReAlineOutputUtils.to_symbols(
            gold, source=TranscriptTypes.TRANSCRIPT
        )
        states: List[State] = []
        # 2. create queues (initially full)
        gold_q = Queue(gold_symbols)
        trans_q = Queue(transcript_symbols)
        # 3. create stack (initially empty)
        stack = Stack()
        # 4a. create Graph (initially empty)
        gold_graph = ReAlineOutputUtils.to_graph()
        edges: List[Edge] = []
        graph = Graph(edges=[])
        # 4b. create Edges.
        # for each edge, create a new State (where we copy the graph, queues, and stack)
        states.append(
            State(
                gold_queue=gold_q.copy(),
                transcript_queue=trans_q.copy(),
                stack=stack.copy(),
                graph=Graph(edges=[]),
            )
        )

        # for step in realine_output: create an edge and append
        return Graph(edges=edges)
