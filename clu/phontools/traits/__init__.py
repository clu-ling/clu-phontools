# from clu.phontools.traits.syllabification import *
# from clu.phontools.traits.syllable_properties import *
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple, Text

# from clu.phontools.struct import Pronunciation, Phone


Pronunciation = Tuple[Text, ...]
Phone = Text
Word = Text


class Syllabification(ABC):
    @staticmethod
    @abstractmethod
    def syllabify(pronunciation: Pronunciation) -> List[Pronunciation]:
        """Abstract static method to syllabify a sequence of phones constituting the pronunciation of a single lexical item.

        Example:
        A subclass that implements this method would ...
        ```python
        MyEnglishSyllabifier.syllabify(('P', 'ER0', 'M', 'IH1', 'T'))
        # should return [('P', 'ER0'), ('M', 'IH1', 'T')]
        ```
        """
        pass


class SyllableProperties(ABC):
    """Utilities related to manipulating syllables."""

    @abstractmethod
    def to_coarse_syllable_form(self) -> Text:
        """Converts a phonological word to a sequence of S (strong) or W (weak) symbols"""
        pass

    @abstractmethod
    def to_syllable_masked_form(self, mask: Text = "X") -> Text:
        """Converts a phonological word where each syllable is represented using the mask

        conceptual examples:
        "poo" -> "X" where mask is "X"
        "July" -> "XX" where mask is "X"
        """
        pass
