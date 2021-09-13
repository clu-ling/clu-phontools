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
        res = [str(IntermediateSymbol())]
        for char in word:
            res.append(str(Symbol(char)))
            res.append(str(IntermediateSymbol()))
        return res

    @staticmethod
    def assign_index(symbols: List) -> List[Tuple[int, Symbol]]:
        indexes = [(indx, symbol) for indx, symbol in enumerate(symbols)]
        return indexes


class Actions(Enum):
    """
    The actions used by the parser.
    """

    DISCARD_T = "discard-t"
    DISCARD_G = "discard-g"
    SHIFT_T = "shift-t"
    SHIFT_G = "shift-g"
    STACK_SWAP = "stack-swap"
    INSERTION_PRESERVE_COPY_CHILD = "insertion-preserve-copy-child"
    INSERTION_PRESERVE_COPY_PARENT = "insertion-preserve-copy-parent"
    DELETION_PRESERVE_COPY_CHILD = "deletion-preserve-copy-child"
    DELETION_PRESERVE_COPY_PARENT = "deletion-preserve-copy-parent"
    ALIGN = "align"
    SUBSTITUTION = "substitution"
    DELETION = "deletion"

    def describe(self):
        return self.name, self.value


class State:
    def __init__(self, gold, transcribed):
        self.gold = gold
        self.transcribed = transcribed

    def gold_queue(self):
        """
        returns queue for gold with special symbol (NULL) and indexes
        [
        (0, "NULL"),
        (1, "c"),
        (2, "NULL"),
        (3, "a"),
        (4, "NULL"),
        (5, "t"),
        (6, "NULL"),
    ]
        """
        gold_symbols = Index.prepare_symbols(self.gold)
        return Index.assign_index(gold_symbols)

    def transcribed_queue(self):
        """
        returns queue for transcribed with special symbol (NULL) and indexes
        [
        (0, "NULL"),
        (1, "c"),
        (2, "NULL"),
        (3, "a"),
        (4, "NULL"),
        (5, "t"),
        (6, "NULL"),
        (7, "s"),
        (8, "NULL"),
    ]
        """
        transcribed_symbols = Index.prepare_symbols(self.transcribed)
        return Index.assign_index(transcribed_symbols)

    def realine_output(self):
        """
        returns alignments
        """
        aligner = ReAline()
        return aligner.align(self.gold, self.transcribed)

    def graph(self):
        """
        returns a toy graph
        [('c', 'align', 'c'), ('a', 'align', 'a'), ('t', 'align', 't'), ('s', 'deletion-preserve-copy-parent', '-')]

        This should be integrated with the special symbol (NULL)???!
        """
        res = []
        aligner = ReAline()
        alignments = aligner.align(self.gold, self.transcribed)
        for i in alignments:
            if i[0] == i[1]:
                res.append((i[0], Actions.ALIGN.value, i[1]))
            elif i[0] == "-":
                res.append((i[0], Actions.SUBSTITUTION.value, i[1]))
            elif i[1] == "-":
                res.append((i[0], Actions.DELETION.value, i[1]))
        return res

    def graph_2(self):
        stack = Stack()
        for i in self.gold_queue():
            stack.shift(i)
        return stack


class Edge:
    def __init__(self, value):
        self._value = value
        self._next = None


class Stack:
    def __init__(self):
        self._items = []

    def __str__(self):
        return str(self._items)

    def shift(self, item):
        """ shifts an item to the stack: works for shift-t and shift-g"""
        self._items.append(item)

    def discard(self, item):
        """ removes an item from the stack: works for discard-t and discard-g"""
        self._items.remove(item)

    def swap(self, item1, item2):
        """ swaps two items on the stack"""
        element1 = self._items.pop(item1)
        element2 = self._items.pop(item2 - 1)

        self._items.insert(item1, element2)
        self._items.insert(item2, element1)

