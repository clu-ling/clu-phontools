# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum
import random
from re import S
from typing import Text, Tuple, List, Sequence, Any, Literal, Union, Optional
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

[[('k', 'align', 'k'), ('æ', 'align', 'æ'), ('t', 'deletion', '-'), ('-', 'inserion', 'n'), 
('-', 'inserion', 'j'), ('i', 'substitution', 'ʌ'), ('n', 'align', 'n'), ('ð', 'deletion', '-'), 
('-', 'inserion', 'k'), ('I', 'substitution', 'æ'), ('h', 'deletion', '-'), ('æ', 'deletion', '-'), 
('t', 'align', 't')], [('f', 'align', 'f'), ('æ', 'substitution', 'ɒ'), ('-', 'inserion', 'ɹ'), 
('t', 'substitution', 'k'), ('i', 'substitution', 'æ'), ('n', 'deletion', '-'), ('ð', 'deletion', '-'), 
('ʌ', 'deletion', '-'), ('h', 'deletion', '-'), ('æ', 'deletion', '-'), ('t', 'align', 't')]]
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
    def get_gold_and_transcript(self):
        alignments = []
        for item in ReadData().get_pairs:
            gold = GetPhones(item[0]).to_ipa
            tran = GetPhones(item[1]).to_ipa
            alignments.append((gold, tran))
        return alignments

    @property
    def alignments(self):
        # [[('c','c')]]
        realiner = ReAline()
        al = []
        for item in self.get_gold_and_transcript:
            gold, transcript = item
            output = realiner.align(gold, transcript)
            al.append(output)
        return al

    # 1. create a list of ParseSymbol instances

    def to_parsesymbols(self, gold, transcript) -> List[ParseSymbol]:
        # ParseSymbol(symbol="NULL", original_index=-1, index=0, source, TranscriptTypes.GOLD)
        some_class.to_parsesymbols("I like turtles", "I like purple tools")

    def realine_graph(self) -> Graph:
        gold_graph = []
        for alignment in self.alignments:
            edge = []
            for pair in alignment:
                (phone_1, phone_2) = pair
                if phone_1 == "-":
                    edge.append((phone_1, "inserion", phone_2))
                elif phone_2 == "-":
                    edge.append((phone_1, "deletion", phone_2))
                elif phone_1 != phone_2 and phone_1 != "-" and phone_2 != "-":
                    edge.append((phone_1, "substitution", phone_2))
                else:
                    edge.append((phone_1, "align", phone_2))
            gold_graph.append(edge)
        return gold_graph


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


"""
Two Enum classes:
Actions
TranscriptTypes
"""


class TranscriptTypes(Enum):
    GOLD: Text = "Gold"
    TRANSCRIPT: Text = "TRANSCRIPT"


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
The following function reads the data from the csv file, utilizes the Index class and returns a list of each GOLD or TRANSCRIPT with indexes. 

NOTE: the reason for this function is to determine which queue is GOLD and which is TRANSCRIPT
"""


def prepare_data_for_parse_symbol_class() -> List[List[List[Tuple[int, Text]]]]:
    """
    returns:
    [[[(0, 'NULL'), (1, 'c'), (2, 'NULL'), (3, 'a'), (4, 'NULL'), (5, 't'), (6, 'NULL'), (7, 'NULL'), (8, 'i'), (9, 'NULL'), (10, 'n'), (11, 'NULL'), (12, 'NULL'), (13, 't'), (14, 'NULL'), (15, 'h'), (16, 'NULL'), (17, 'e'), (18, 'NULL'), (19, 'NULL'), (20, 'h'), (21, 'NULL'), (22, 'a'), (23, 'NULL'), (24, 't'), (25, 'NULL')], 
      [(0, 'NULL'), (1, 'c'), (2, 'NULL'), (3, 'a'), (4, 'NULL'), (5, 'n'), (6, 'NULL'), (7, 'y'), (8, 'NULL'), (9, 'o'), (10, 'NULL'), (11, 'n'), (12, 'NULL'), (13, 'NULL'), (14, 'c'), (15, 'NULL'), (16, 'a'), (17, 'NULL'), (18, 't'), (19, 'NULL')]], 
     [[(0, 'NULL'), (1, 'f'), (2, 'NULL'), (3, 'a'), (4, 'NULL'), (5, 't'), (6, 'NULL'), (7, 'NULL'), (8, 'i'), (9, 'NULL'), (10, 'n'), (11, 'NULL'), (12, 'NULL'), (13, 't'), (14, 'NULL'), (15, 'h'), (16, 'NULL'), (17, 'e'), (18, 'NULL'), (19, 'NULL'), (20, 'h'), (21, 'NULL'), (22, 'a'), (23, 'NULL'), (24, 't'), (25, 'NULL')], 
      [(0, 'NULL'), (1, 'f'), (2, 'NULL'), (3, 'a'), (4, 'NULL'), (5, 'r'), (6, 'NULL'), (7, 'NULL'), (8, 'c'), (9, 'NULL'), (10, 'a'), (11, 'NULL'), (12, 't'), (13, 'NULL')]]]
    """
    data = ReadData()
    pairs = data.get_pairs
    prepared_data = []
    for element in pairs:
        items = []
        gold, transcript = element
        index_gold = Index(gold)
        gold_null = index_gold.prepare_symbols(gold)
        gold_null = [i for i in gold_null if i != " "]
        gold_null = index_gold.assign_index(gold_null)
        items.append(gold_null)
        index_transcript = Index(transcript)
        transcript_null = index_transcript.prepare_symbols(transcript)
        transcript_null = [i for i in transcript_null if i != " "]
        transcript_null = index_transcript.assign_index(transcript_null)
        items.append(transcript_null)
        prepared_data.append(items)
    return prepared_data


"""
ParseSymbol is a dataclass that take GOLD with indexes and TRANSCRIPT with indexes and returns a GOLD QUEUE and a TRANSCRIPT QUEUE

Output Example:

GOLD_QUEUE = [
    ParseSymbol(symbol="NULL", original_index=-1, index=0, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="c", original_index=0, index=1, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="NULL", original_index=-1, index=2, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="a", original_index=1, index=3, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="NULL", original_index=-1, index=4, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="t", original_index=2, index=5, source=TranscriptTypes.GOLD),
    ParseSymbol(symbol="NULL", original_index=-1, index=6, source=TranscriptTypes.GOLD),
    ]
"""

# EXAMPLE: a GOLD QUEUE from the output of `prepare_data_for_parse_symbol_class()`

example = prepare_data_for_parse_symbol_class()
example = example[0][0]

# GOLD, TRANSCRIPT = example


@dataclass
class ParseSymbol:
    symbol: Text
    original_index: int
    index: int
    source: Text

    def parse(queue):
        parsed_symbols = []
        for item in queue:
            if item[1] == "NULL":
                symbol = item[1]
                original_index = -1
                index = item[0]
                source = "GOLD"
                parsed_symbols.append(
                    ParseSymbol(
                        symbol=symbol,
                        original_index=original_index,
                        index=index,
                        source=source,  # TranscriptTypes.GOLD if item[0] else TranscriptTypes.TRANSCRIPT
                    )
                )
            elif item[1] != "NULL":
                symbol = item[1]
                original_index = (item[0] - 1) / 2
                index = item[0]
                source = "GOLD"
                parsed_symbols.append(
                    ParseSymbol(
                        symbol=symbol,
                        original_index=original_index,
                        index=index,
                        source=source,
                    )
                )
        return parsed_symbols


# parse_symbol = ParseSymbol
# print(parse_symbol.parse(example))


@dataclass()
class Graph:
    edges: List[Edge]

    def has_children(self, ps: ParseSymbol) -> bool:
        # go over the edges and check which is the source and the destination
        pass


@dataclass
class Edge:
    source: ParseSymbol  # is an instance
    destination: ParseSymbol
    label: Actions


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


class State:
    def __init__(self):
        self.stack = []
        self.gold_graph: Optional[Graph]
        self.current_graph: Graph
        self.gold_q: ParseSymbol
        self.transcribed_q: ParseSymbol


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
    # (1) realine gold graph
    realine_output = RealineOutput()
    gold_graph = realine_output.realine_graph()
    print(gold_graph)

    # (2) indexes
    print(prepare_data_for_parse_symbol_class())

    # (3) ParseSymbol
    q = [
        (0, "NULL"),
        (1, "c"),
        (2, "NULL"),
        (3, "a"),
        (4, "NULL"),
        (5, "t"),
        (6, "NULL"),
    ]

    parse_symbol = ParseSymbol
    parsed = parse_symbol.parse(q)
    # print(parsed)

