#!/usr/bin/env python
import numpy as np
from pydantic.dataclasses import dataclass
from typing import Dict, List, Tuple, Text
from clu.phontools.realine import ReAline


@dataclass
class PhonemeErrors:
    """
    stores phoneme errors.
    """

    insertions: List[Tuple[Text, Text]]
    deletions: List[Tuple[Text, Text]]
    substitutions: List[Tuple[Text, Text]]

    @property
    def edit_distance(self) -> int:
        return len(self.insertions) + len(self.deletions) + len(self.substitutions)

    def to_dict(self) -> Dict[str, float]:
        return {
            "insertions": self.insertions,
            "deletions": self.deletions,
            "substitutions": self.substitutions,
        }


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

    @staticmethod
    def phoneme_errors(alignments: List[Tuple[str, str]]):
        """
        TODO: add docstring
        """
        insertions = []
        deletions = []
        substitutions = []
        for pair in alignments:
            (phone_1, phone_2) = pair
            if phone_1 == "-":
                insertions.append(pair)
            elif phone_2 == "-":
                deletions.append(pair)
            elif phone_1 != phone_2 and phone_1 != "-" and phone_2 != "-":
                substitutions.append(pair)
        return PhonemeErrors(
            insertions=insertions, deletions=deletions, substitutions=substitutions
        )


# alignments = [('æ', 'æ'), ('d', 'd'), ('v', 'v'), ('æ', 'æ'), ('n', 'n'), ('s', 's'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('-', 's'), ('æ', 'ɛ'), ('t', 't'), ('ə', 'ə'), ('p', '-'), ('i', 'i'), ('l', 'l')]
# print(Metrics.phone_similarity(alignments))
# print(Metrics.phoneme_errors(alignments))
