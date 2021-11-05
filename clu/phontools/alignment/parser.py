# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum
import random
from typing import (
    Text,
    Tuple,
    List,
    Sequence,
    Any,
    Literal,
    Union,
)
from clu.phontools.lang.en import EnglishUtils
from clu.phontools.struct import *
from clu.phontools.pronouncing import ConverterUtils
from clu.phontools.alignment.realine import *
from clu.phontools.alignment.lbe import *


# Type aliases
Phone = Text
NullSymbol = Literal["NULL"]
ParserInput = Union[Phone, NullSymbol]

"""
The Three classes (ReadData - GetPhones - RealineOutput) take a tab delimited file that contains GOLD and TRANS and returns
a realine graph as follows:
[[('k', 'align', 'k'), ('æ', 'align', 'æ'), ('t', 'deletion', '-'), ('-', 'inserion', 'n'), ('-', 'inserion', 'j'), ('i', 'substitution', 'ʌ'), ('n', 'align', 'n'), ('ð', 'deletion', '-'), ('-', 'inserion', 'k'), ('I', 'substitution', 'æ'), ('h', 'deletion', '-'), ('æ', 'deletion', '-'), ('t', 'align', 't')], [('f', 'align', 'f'), ('æ', 'substitution', 'ɒ'), ('-', 'inserion', 'ɹ'), ('t', 'substitution', 'k'), ('i', 'substitution', 'æ'), ('n', 'deletion', '-'), ('ð', 'deletion', '-'), ('ʌ', 'deletion', '-'), ('h', 'deletion', '-'), ('æ', 'deletion', '-'), ('t', 'align', 't')]]
"""


class ReadData:
    def __init__(self):
        self.path = "./data.txt"

    @property
    def get_pairs(self) -> List[List[Text]]:
        file = open(self.path).readlines()
        return [item.strip().split("\t") for item in file]


class GetPhones:
    def __init__(self, phrase: Text) -> List[List[Text]]:
        self.phrase = phrase

    @property
    def raw_phrase_to_phone_sets(self) -> List[List[Text]]:
        return [
            list(phrase.phones)
            for phrase in EnglishUtils.all_possible_phrases_for(self.phrase.split())
        ]

    @property
    def random_member_of_the_phone_set(self) -> List[Text]:
        return random.choice(self.raw_phrase_to_phone_sets)

    @property
    def to_ipa(self):
        return [
            ConverterUtils.arpabet_to_ipa(phone)
            for phone in self.random_member_of_the_phone_set
        ]


class RealineOutput:
    @property
    def get_gold_transcript(self):
        alignments = []
        for item in ReadData().get_pairs:
            gold = GetPhones(item[0]).to_ipa
            tran = GetPhones(item[1]).to_ipa
            alignments.append((gold, tran))
        return alignments

    @property
    def alignments(self):
        realiner = ReAline()
        al = []
        for item in self.get_gold_transcript:
            gold, transcript = item
            output = realiner.align(gold, transcript)
            al.append(output)
        return al

    def realine_graph(self):
        ll = []
        for alignment in self.alignments:
            s = []
            for pair in alignment:
                (phone_1, phone_2) = pair
                if phone_1 == "-":
                    s.append((phone_1, "inserion", phone_2))
                elif phone_2 == "-":
                    s.append((phone_1, "deletion", phone_2))
                elif phone_1 != phone_2 and phone_1 != "-" and phone_2 != "-":
                    s.append((phone_1, "substitution", phone_2))
                else:
                    s.append((phone_1, "align", phone_2))
            ll.append(s)
        return ll


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
        """
        Gold -> "cat in the hat" -> Seq[PhonologicalWord] -> Phones
        Transcribed -> "canyon hat"  -> Seq[PhonologicalWord] -> Phones
        (all pairs as a generator)
        Example:
        cat:
        [Null, c, NULL, a, NULL, t, NULL]

        G: stimulus
        T: response
        """
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


gold = "cat"
tran = "cat"


class TranscriptTypes(Enum):
    GOLD: Text = "Gold"
    TRANSCRIPT: Text = "TRANSCRIPT"


@dataclass()
class ParseSymbol:
    symbol: Text
    original_index: int
    index: int
    # gold or transcript
    source: TranscriptTypes


g_queue = [
    ParseSymbol(symbol="NULL", original_index=-1, index=0, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="c", original_index=0, index=1, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="NULL", original_index=-1, index=2, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="a", original_index=1, index=3, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="NULL", original_index=-1, index=4, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="t", original_index=2, index=5, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="NULL", original_index=-1, index=6, source=TranscriptTypes.GOLD),
]

t_queue = [
    ParseSymbol(
        symbol="NULL", original_index=-1, index=0, source=TranscriptTypes.TRANSCRIPT
    ),
    ParseSymbol(
        symbol="c", original_index=0, index=1, source=TranscriptTypes.TRANSCRIPT
    ),
    ParseSymbol(
        symbol="NULL", original_index=-1, index=2, source=TranscriptTypes.TRANSCRIPT
    ),
    ParseSymbol(
        symbol="a", original_index=1, index=3, source=TranscriptTypes.TRANSCRIPT
    ),
    ParseSymbol(
        symbol="NULL", original_index=-1, index=4, source=TranscriptTypes.TRANSCRIPT
    ),
    ParseSymbol(
        symbol="t", original_index=2, index=5, source=TranscriptTypes.TRANSCRIPT
    ),
    ParseSymbol(
        symbol="NULL", original_index=-1, index=6, source=TranscriptTypes.TRANSCRIPT
    ),
]


@dataclass()
class Graph:
    edge_order: List[Edge]

    def has_children(self, ps: ParseSymbol) -> bool:
        # go over the edges and check which is the source and the destination
        pass


class Edge:
    source: ParseSymbol
    destination: ParseSymbol
    label: Actions


gold_parse = Graph(
    edge_order=[
        Edge(
            source=ParseSymbol(
                symbol="NULL",
                original_index=-1,
                index=0,
                source=TranscriptTypes.TRANSCRIPT,
            ),
            destination=ParseSymbol(
                symbol="NULL",
                original_index=-1,
                index=0,
                source=TranscriptTypes.TRANSCRIPT,
            ),
            label=Actions.DISCARD_T,
        ),
        # gold_queue = [null c null a null t null]
        # trans_queue = [c null a null t null]
        # stack = []
        Edge(
            source=ParseSymbol(
                symbol="NULL", original_index=-1, index=0, source=TranscriptTypes.GOLD
            ),
            destination=ParseSymbol(
                symbol="NULL", original_index=-1, index=0, source=TranscriptTypes.GOLD
            ),
            label=Actions.DISCARD_G,
        ),
        # gold_queue = [c null a null t null]
        # trans_queue = [c null a null t null]
        # stack = []
        Edge(
            source=ParseSymbol(
                symbol="c", original_index=0, index=1, source=TranscriptTypes.TRANSCRIPT
            ),
            destination=ParseSymbol(
                symbol="c", original_index=0, index=1, source=TranscriptTypes.GOLD
            ),
            label=Actions.ALIGN,
        ),
        # gold_queue = [null a null t null]
        # trans_queue = [null a null t null]
        # stack = []
        Edge(
            source=ParseSymbol(
                symbol="NULL",
                original_index=-1,
                index=2,
                source=TranscriptTypes.TRANSCRIPT,
            ),
            destination=ParseSymbol(
                symbol="NULL",
                original_index=-1,
                index=2,
                source=TranscriptTypes.TRANSCRIPT,
            ),
            label=Actions.DISCARD_T,
        ),
        # gold_queue = [null a null t null]
        # trans_queue = [a null t null]
        # stack = []
        Edge(
            source=ParseSymbol(
                symbol="NULL", original_index=-1, index=3, source="Gold"
            ),
            destination=ParseSymbol(
                symbol="NULL", original_index=-1, index=3, source="Gold"
            ),
            label=Actions.DISCARD_G,
        ),
        # gold_queue = [a null t null]
        # trans_queue = [a null t null]
        # stack = []
        Edge(
            source=ParseSymbol(
                symbol="a", original_index=1, index=4, source=TranscriptTypes.TRANSCRIPT
            ),
            destination=ParseSymbol(
                symbol="a", original_index=1, index=4, source=TranscriptTypes.GOLD
            ),
            label=Actions.ALIGN,
        ),
        # gold_queue = [null t null]
        # trans_queue = [null t null]
        # stack = []
    ]
)

# utility method to tell us

# function that converts the realine output to parse symbols and edges.
# stack operation (del - insertion)


class ParsersUtils:
    @staticmethod
    def convert_realine_output(realine_output: List[Tuple[Text, Text]]) -> Graph:
        """converts realine output to a gold parse represented like a graph.
        Each symbol is converted to a ParseSymbol.
        """
        pass


class IndexTracker:
    def __init__(self):
        # ['c','a','t']
        self.original_phones: Sequence[Phones] = ["c", "a", "t"]
        # ['NULL','c','NULL','a','NULL','t','NULL']
        self.original_with_null: Sequence[Phones, Symbol] = [
            "NULL",
            "c",
            "NULL",
            "a",
            "NULL",
            "t",
            "NULL",
        ]

    @property
    def original_phones_indexes(self):
        """[(0, 'c'), (1, 'a'), (2, 't')]"""
        return [(indx, phone) for indx, phone in enumerate(self.original_phones)]

    @property
    def original_with_null_indexes(self):
        """[(0, 'NULL'), (1, 'c'), (2, 'NULL'), (3, 'a'), (4, 'NULL'), (5, 't'), (6, 'NULL')]"""
        return [(indx, phone) for indx, phone in enumerate(self.original_with_null)]

    @property
    def original_and_null(self):
        """[(-1, 'NULL'), (0, 'c'), (-1, 'NULL'), (1, 'a'), (-1, 'NULL'), (2, 't'), (-1, 'NULL')]"""
        indexes_1 = []
        for i in self.original_phones_indexes:
            for item in self.original_with_null:
                if item in i[1]:
                    indexes_1.append((i[0], item))
        indexes_2 = []
        for item in self.original_with_null:
            if item == "NULL":
                indexes_2.append((-1, item))

        result = [None] * (len(indexes_1) + len(indexes_2))
        result[::2] = indexes_2
        result[1::2] = indexes_1
        return result


@dataclass
class ParseSymbol:
    """
    g_queue = [
    ParseSymbol(symbol="NULL", original_index=-1, index=0, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="c", original_index=0, index=1, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="NULL", original_index=-1, index=2, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="a", original_index=1, index=3, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="NULL", original_index=-1, index=4, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="t", original_index=2, index=5, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="NULL", original_index=-1, index=6, source=TranscriptTypes.GOLD),
    ]
    """

    symbol: Text
    original_index: int
    index: int
    source: Text

    @classmethod
    def parse(cls):
        s = []
        for item in IndexTracker().original_with_null:
            if item in IndexTracker().original_and_null:
                s.append(symbol=item)
        return s


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
    # state = State()
    # print(state.gold_queue())

    # # 3) parser class
    # parser = Parser(state)
    # print(parser.gold)

