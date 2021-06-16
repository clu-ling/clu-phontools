#!/usr/bin/env python
import numpy as np
from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from typing import Dict, List, Tuple, Text
from clu.phontools.alignment.realine import ReAline


class Metrics(object):
    """
    Metrics take the output of ReAline and
    calculates edit distance, phoneme errors and phone similarity.
    """

    realine = ReAline()

    @staticmethod
    def similarity(pair: Tuple[Text, Text]) -> float:
        """
        Calculates similarity of an aligned pair of symbols (phones) using 1 - ReAline.delta.
        See Kondrak (2002, p54).
        """
        (a, b) = pair
        missing = (
            True
            if any(symbol not in Metrics.realine.feature_matrix for symbol in pair)
            else False
        )
        return 0.0 if missing else 1 - Metrics.realine.delta(a, b)

    @staticmethod
    def phone_similarity(alignments: List[Tuple[str, str]]) -> List[int]:
        """
        TODO: add docstring
        """
        return [Metrics.similarity(i) for i in alignments]


# alignments = [('æ', 'æ'), ('d', 'd'), ('v', 'v'), ('æ', 'æ'), ('n', 'n'), ('s', 's'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('-', 's'), ('æ', 'ɛ'), ('t', 't'), ('ə', 'ə'), ('p', '-'), ('i', 'i'), ('l', 'l')]
# print(Metrics.phone_similarity(alignments))
# print(Metrics.phoneme_errors(alignments))
