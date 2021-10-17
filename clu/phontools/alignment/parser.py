# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum, auto
from collections import deque

from numpy import _FlatIterSelf
from clu.phontools.alignment.realine import ReAline
from typing import Dict, Text, Tuple, List, Optional, Sequence, Callable, Any

"""
The Symbol and Index classes are used to insert a NULL symbol between the symbols 
of the gold and transcript.
"""


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


"""
Graph class returns 
1) realine output ('b', 'align', 'b')
2) Gold: symbols
3) Transcript: symbols
4) Label: align 
"""


class Graph:
    def __init__(self, alignment):
        self.alignment = alignment
        self.edges = []
        self.add_edge()

    def realine_output(self):
        ll = []
        for alignment in self.alignment:
            s = []
            for pair in alignment:
                (phone_1, phone_2) = pair
                if phone_1 == "-":
                    s.append(
                        (phone_1, "inserion", phone_2)
                    )  # we can get these actions from the Enum class
                elif phone_2 == "-":
                    s.append((phone_1, "deletion", phone_2))
                elif phone_1 != phone_2 and phone_1 != "-" and phone_2 != "-":
                    s.append((phone_1, "substitution", phone_2))
                else:
                    s.append((phone_1, "align", phone_2))
            ll.append(s)
        return ll

    def add_edge(self):

        obj = Edge()
        for i in self.realine_output():
            # x = []
            for ii in i:
                obj.gold.append(ii[0])
                obj.transcribed.append(ii[2])
                obj.label.append(ii[1])

        self.edges.append(obj)
        obj = Edge()

        print("Gold", self.edges[0].gold)
        print("TRANScRIPT", self.edges[0].transcribed)
        print("LABEL", self.edges[0].label)


class Edge:
    def __init__(self):
        self.gold = []
        self.transcribed = []
        self.label = []


"""
State class
It includes the stack, two queues and the graph 
1) stack is empty
2) graph is empty
3

"""


class State:
    def __init__(self):
        self.stack = []
        self.resulted_graph = []
        self.gold = gold_graph.edges[0].gold
        self.transcribed = gold_graph.edges[0].transcribed

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

    def get_mappings(self):
        pass


"""
Parser class returns 

"""


class Parser:
    def __init__(self, state):
        self.gold = state.gold_queue()
        self.transcribed = state.transcribed_queue()
        self.stack = state.stack
        self.data = []

    def __repr__(self):
        return repr(self.stack)

    def oracle(self):
        train_data = []
        while self.gold and self.transcribed:
            if self.stack and self.stack_is_empty():
                stack_top = self.shift(self.gold)
                stack_bottom = self.shift(self.transcribed)

    def parse(self):
        pass

    """
    `check` methods:
    We define a number of check methods to test the stack and the stack
    """

    def stack_is_empty(self):
        """This methods checks whether the stack is empty or full"""
        result = False
        if len(self.stack) == 0:
            return True
        return result

    def shift(self, queue):
        """This method moves items form the queue to the stack"""
        return self.stack.insert(0, queue.pop(0))

    def check_edge(self):
        """This method checks whether the two symbols on the stack are in realine outpur or not."""
        result = False
        stack_top = self.stack[-1]
        stack_bottom = self.stack[-2]
        if (stack_top, stack_bottom) in gold_graph.realine_output():
            return True
        return result

    def check_len_stack(self):
        """This methods checks the length of the stack"""
        result = False
        if len(self.stack) == 2:
            return True
        return result

    def has_null(self):
        """This method checks whether there is a `Null` symbol on the stack or not."""
        pass

    """
    `Do` methods:
    We define a number of do methods to assign actions
    """

    def discard(self, stack):
        """This method is used to empty the stack completely"""
        stack.pop()
        stack.pop()

    def swap(self, item1, item2):
        """ swaps two items on the stack"""
        element1 = self.stack.pop(item1)
        element2 = self.stack.pop(item2 - 1)

        self.stack.insert(item1, element2)
        self.stack.insert(item2, element1)


if __name__ == "__main__":
    # this data is realine output
    data = [
        [
            ("b", "b"),
            ("æ", "ɛ"),
            ("l", "l"),
            ("ʌ", "i"),
            ("n", "-"),
            ("s", "z"),
            ("k", "g"),
            ("l", "l"),
            ("æ", "æ"),
            ("m", "-"),
            ("p", "-"),
            ("ʌ", "-"),
            ("n", "-"),
            ("d", "d"),
            ("-", "ʌ"),
            ("b", "b"),
            ("ɒ", "ɒ"),
            ("t", "t"),
            ("ʌ", "ʌ"),
            ("l", "l"),
        ]
    ]

    # 1) Graph class
    gold_graph = Graph(data)
    print(gold_graph.edges[0].gold)
    print("Realine output", gold_graph.realine_output())

    # 2) State class
    # stack = []
    state = State()
    print(state.gold_queue())

    # 3) parser class
    parser = Parser(state)
    print(parser.gold)

