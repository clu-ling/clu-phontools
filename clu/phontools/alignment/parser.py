# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum, auto
from clu.phontools.alignment.realine import ReAline
from typing import Dict, Text, Tuple, List, Optional, Sequence, Callable


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
        symbol = text[0]
        for item in text[1:]:
            symbol += '-' + item
        return '-' + symbol + '-'


class Oracle:
    pass






