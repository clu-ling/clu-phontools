# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum, auto
from clu.phontools.alignment.realine import ReAline
from typing import Dict, Text, Tuple, List, Optional, Sequence, Callable, Any


class Symbol:
    # FIXME: need to track index of symbol
    def __init__(self, char: Text):
        self._symbol = char

    def __repr__(self):
        return self._symbol


class IntermediateSymbol(Symbol):
    def __init__(self):
        super().__init__(char="NULL")


class Index:
    # FIXME: we use Any and we will fix it later so that the code accepts any seq.
    def __init__(self, word: Sequence[Any], start=0):
        self.word = word
        self.satrt = start

    def __repr__(self):
        return str(self.word)

    @staticmethod
    def prepare_symbols(word: Text) -> Sequence[Symbol]:
        res = [IntermediateSymbol()]
        for char in word:
            res.append(Symbol(char))
            res.append(IntermediateSymbol())
        return res

    @staticmethod
    def assign_index(symbols: List) -> List[Tuple[int, Symbol]]:
        indexes = [(indx, symbol) for indx, symbol in enumerate(symbols)]
        return indexes


class Actions(Enum):
    """
    The actions used by the parser.
    """

    DISCARD_T = auto()
    DISCARD_G = auto()
    SHIFT_T = auto()
    SHIFT_G = auto()
    STACK_SWAP = auto()
    INSERTION_PRESERVE_COPY_CHILD = auto()
    INSERTION_PRESERVE_COPY_PARENT = auto()
    DELETION_PRESERVE_COPY_CHILD = auto()
    DELETION_PRESERVE_COPY_PARENT = auto()
    ALIGN = auto()
    SUBSTITUTION = auto()

    def describe(self):
        return self.name, self.value


@dataclass()
class Graph:
    """
    This dataclass encodes all the aligment output (edges, vertics, and nodes)
    wether these are transcript or gold. Based on this graph, we constrcut the oracle
    """

    pass


class Parser:
    def __init__(self):
        pass

    @staticmethod
    def add_special_symbol(text: Text) -> Text:
        """
        class means intermediate symbols:
            wrap each letter is a symbol class
        """
        symbol = text[0]
        for item in text[1:]:
            symbol += "-" + item
        return "-" + symbol + "-"


# class Oracle:
#     pass


# class State:
#     transcribed_queue: Sequence[Symbol]
#     gold_queue: Sequence[Symbol]
#     # NOTE: this might need to be a Sequence[Graph]
#     stack: Sequence[Symbol]
#     # the graph you've constructed so far
#     graph: Graph


# class Graph:
#     edges: Sequence[Edge]


# class Edge:
#     source: Symbol
#     destination: Symbol
#     label: Text

