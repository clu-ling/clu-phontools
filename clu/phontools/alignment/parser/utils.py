from __future__ import annotations
import random
from .actions import *
from .graph import *
from .state import ActionFunc
from .symbols import *
from .stack import *
from .state import *
from .queue import *
from typing import List, Text, Tuple
from clu.phontools.lang.en import EnglishUtils
from clu.phontools.struct import *
from clu.phontools.pronouncing import ConverterUtils
from clu.phontools.alignment.realine import *
from clu.phontools.alignment.lbe import *

__all__ = ["ReAlineOutputUtils"]


class ReAlineOutputUtils:
    """`ReAlineOutputUtils` class returns:
    1) a list of `Symbol` instances through `to_symbols` method.
    2) 
    """

    # TODO: @Sayed, implement this -------> DONE
    # NOTE: I did notuse the methods is_null and create_null in Symbol class. Is that okay?!
    @staticmethod
    def to_symbols(text: Text, source: TranscriptTypes) -> List[Symbol]:
        """takes a raw text and returns a list of `Symbol` instances"""
        symbols = []
        phones = [
            list(text.phones)
            for text in EnglishUtils.all_possible_phrases_for(text.split())
        ]
        random_phrase = random.choice(phones)
        to_ipa = [ConverterUtils.arpabet_to_ipa(phone) for phone in random_phrase]
        indx = Index(to_ipa)
        add_null = indx.prepare_symbols(to_ipa)
        with_indexes = indx.assign_index(add_null)
        for item in with_indexes:
            if item[1] == "NULL":
                symbol = item[1]
                original_index = -1
                index = item[0]
                source = source
                symbols.append(
                    Symbol(
                        symbol=symbol,
                        original_index=original_index,
                        index=index,
                        source=source,
                    )
                )
            elif item[1] != "NULL":
                symbol = item[1]
                original_index = int((item[0] - 1) / 2)
                index = item[0]
                source = source
                symbols.append(
                    Symbol(
                        symbol=symbol,
                        original_index=original_index,
                        index=index,
                        source=source,
                    )
                )
        return symbols

    @staticmethod
    def realine_output(gold: Text, transcribed: Text) -> List[Tuple[Text, Text, Text]]:
        """returns ReAline output as a gold graph"""
        realiner = ReAline()
        alignment = realiner.align(gold, transcribed)
        gold_graph = []
        for pair in alignment:
            (phone_1, phone_2) = pair
            if phone_1 == "-":
                gold_graph.append((phone_1, "insertion", phone_2))
            elif phone_2 == "-":
                gold_graph.append((phone_1, "deletion", phone_2))
            elif phone_1 != phone_2 and phone_1 != "-" and phone_2 != "-":
                gold_graph.append((phone_1, "substitution", phone_2))
            else:
                gold_graph.append((phone_1, "align", phone_2))
        return gold_graph

    # TODO: @Sayed, implement this by "peeking into the future"
    # NOTE: to_graph method had (symbols: List[Symbol]) as an argument. I added two source and destination.
    @staticmethod
    def to_graph(
        source: Text, destination: Text, realine_output: List[Tuple[Text, Text, Text]]
    ) -> Graph:
        """returns a Graph object which is a list of Edges"""
        # STEP 1: get source list of Symbols and destination list of Symbols and map them togther (BORING WAY!!)
        source_symbols = ReAlineOutputUtils.to_symbols(
            source, TranscriptTypes.TRANSCRIPT.value
        )
        destination_symbols = ReAlineOutputUtils.to_symbols(
            destination, TranscriptTypes.TRANSCRIPT.value
        )
        
        pairs = []
        source_len = len(source_symbols)
        dest_len = len(destination_symbols)
        i = 1
        for item in range(min(source_len, dest_len)):
            t = []
            t.insert(i, source_symbols[item])
            t.insert(i, destination_symbols[item])
            pairs.append(t)
            i += 2
        pairs.extend(destination_symbols[item + 1 :])
        pairs.extend(source_symbols[item + 1 :])

        pairs = [[i] if type(i) != list else i for i in pairs]

        # STEP 2: iterate over pairs to construct edges (ANOTHER BORING WAY!!!)
        edges = []
        for pair in pairs:
            if len(pair) == 2:
                if pair[0].symbol == pair[1].symbol:
                    edges.append(Edge(source=pair[0], destination=pair[1], label=Actions.ALIGN.value))
                else:
                    # other possibilities here but this example is for the test case
                    pass
            elif len(pair) != 2:
                if pair[0].source == "GOLD":
                    edges.append(Edge(source=Symbol(symbol='-', original_index=pair[0].original_index, index=pair[0].index, source=TranscriptTypes.TRANSCRIPT.value), destination=i[0], label=Actions.INSERTION_PRESERVE_PARENT.value))
                elif pair[0].source == "TRANSCRIPT":
                    edges.append(Edge(source=pair[0], destination=Symbol(symbol='-', original_index=pair[0].original_index, index=pair[0].index, source=TranscriptTypes.GOLD.value), label=Actions.INSERTION_PRESERVE_CHILD.value))
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


class AddSymbol:
    def __init__(self, char: Text):
        self._symbol = char

    def __repr__(self):
        return self._symbol


class IntermediateSymbol(AddSymbol):
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
    def prepare_symbols(word: Text) -> Sequence[AddSymbol]:
        """
        """
        res = [str(IntermediateSymbol())]
        for char in word:
            res.append(str(AddSymbol(char)))
            res.append(str(IntermediateSymbol()))
        return res

    @staticmethod
    def assign_index(symbols: List) -> List[Tuple[int, AddSymbol]]:
        indexes = [(indx, symbol) for indx, symbol in enumerate(symbols)]
        return indexes
