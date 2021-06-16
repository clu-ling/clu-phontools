from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any, Text, Sequence
import re
import itertools
from autocorrect import Speller
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
import numpy as np


Pronunciation = Tuple[Text, ...]
Phone = Text
# type alias for a string of characters representing a word
SimpleWord = Text


spell = Speller(lang="en")


class Hashable(ABC):
    """Ensures subclasses are hashable"""

    @abstractmethod
    def __hash__(self) -> int:
        pass


class Stress(Enum):
    """Enumeration of all possible stress values"""

    NON_VOWEL = "-"
    """The phone is not a vowel (i.e., it cannot have a stress assignment)"""
    NO_STRESS = "0"
    """The phone (vowel) is unstressed."""
    PRIMARY = "1"
    """The phone (vowel) receives primary stress"""
    SECONDARY = "2"
    """The phone (vowel) receives secondary stress."""

    def __repr__(self) -> Text:
        return f"Stress.{self.name}"


class CoarseStress(Enum):
    """A coarse representation of stress is categorized as being either strong (S) of weak (W)."""

    STRONG = "S"
    """Strong stress.  Corresponds to `clu.phontools.struct.Stress.PRIMARY` and `clu.phontools.struct.Stress.SECONDARY`"""
    WEAK = "W"
    """Weak stress.  Corresponds to `clu.phontools.struct.Stress.NO_STRESS`"""

    def __repr__(self) -> Text:
        return f"CoarseStress.{self.name}"


class SyllableProperties(ABC):
    """Propertie and manipulations of syllables."""

    """A sequence of `clu.phontools.struct.Stress` assignments"""

    def __init__(self):
        self.stress_pattern: Sequence[Stress] = []

    @property
    def coarse_stress_pattern(self) -> Sequence[CoarseStress]:
        """Maps a detailed stress sequence to a sequence of strong and weak stressed syllabled"""
        summary = []
        for stress in self.stress_pattern:
            if stress == Stress.NO_STRESS:
                summary.append(CoarseStress.WEAK)
            elif stress in {Stress.PRIMARY, Stress.SECONDARY}:
                summary.append(CoarseStress.STRONG)
        return summary

    @property
    def coarse_stress(self) -> Text:
        """Converts a phonological word to a sequence of S (strong) or W (weak) symbols"""
        return "".join(cs.value for cs in self.coarse_stress_pattern)

    def mask_syllables(self, mask: Text = "X") -> Text:
        """Converts a phonological word where each syllable is represented using the mask

        conceptual examples:
        "poo" -> "X" where mask is "X"
        "July" -> "XX" where mask is "X"
        """
        return "".join(mask for cs in self.coarse_stress_pattern)

    @property
    def num_syllables(self):
        """A syllable contains at most one stressed element (weak or strong)"""
        return len(self.coarse_stress_pattern)


# FIXME: consider adding PhonologicalSystem(Enum) -> ARPABET, IPA, XAMPA, etc.
class PhonologicalWord(BaseModel, SyllableProperties, Hashable):
    """A [phonological word](https://en.wikipedia.org/wiki/Phonological_word) composed of one or more syllables

    :param phones: a sequences of phonological symbols (character, kana, etc.)
    :param stress_pattern: a sequence of `clu.phontools.struct.Stress` assignments (one for each of the `phones`)
    """

    phones: Sequence[Phone]
    """NOTE: For an EnglishSyllable, use `clu.phontools.lang.en.EnglishUtils.pronouncing_dict` as part of @staticmethod factory constructor"""
    stress_pattern: Sequence[Stress]

    def __iter__(self) -> Phone:
        for phone in self.phones:
            yield phone

    def __getitem__(self, i: int) -> Phone:
        return self.phones[i]

    def __reversed__(self) -> "Phrase":
        return PhonologicalWord(phones=self.phones[::-1])

    def __contains__(self, item) -> bool:
        return True if item in self.phones else False

    def __len__(self) -> int:
        return len(self.phones)

    def __hash__(self) -> int:
        return hash(tuple(list(self.phones) + list(self.stress_pattern)))


class Word(BaseModel, Hashable):
    r"""The smallest sequence of phonemes that can be uttered in isolation with objective or practical meaning.

    :param word: orthographic representation of this Word
    :param phonological_form: the phonological form of this Word
    """

    word: Text
    phonological_form: PhonologicalWord

    @property
    def pf(self) -> PhonologicalWord:
        """Alias for phonological_form"""
        return self.phonological_form

    def graphemes(self) -> Sequence[Text]:
        """Individual characters/symbols that comprise the orthographic representation of the `clu.phontools.struct.Word`"""
        return "".split(self.word)

    def __hash__(self) -> int:
        return hash((("word", self.word), ("pf", hash(self.phonological_form))))


class Phrase(BaseModel, Hashable):
    """A sequence of `clu.phontools.struct.Word` constitutes a Phrase.

    :param words: The sequence of `clu.phontools.struct.Word` that constitutes this Phrase.
    """

    words: Sequence[Word]

    @property
    def coarse_stress(self) -> Sequence[Text]:
        """Returns coarse stress form for each word in the Phrase"""
        return [word.pf.coarse_stress for word in self.words]

    def mask_syllables(self, mask: Text = "X") -> Sequence[Text]:
        """Returns coarse stress form for each word in the Phrase"""
        return [word.pf.mask_syllables(mask) for word in self.words]

    def words_as_phones(self) -> Sequence[Text]:
        """Represent `clu.phontools.struct.Phrase` using a sequence of symbols denoting the phones of each word

        Example:
        ```python
        from clu.phontools.struct import *
        # define a phrase
        phrase = Phrase(
          words=[
            Word(
              word='hello',
              phonological_form=PhonologicalWord(
                phones=('HH', 'EH0', 'L', 'OW1'),
                stress_pattern=[
                  Stress.NON_VOWEL,
                  Stress.NO_STRESS,
                  Stress.NON_VOWEL,
                  Stress.PRIMARY
                ]
              )
            ),
            Word(
              word='world',
              phonological_form=PhonologicalWord(
                phones=('W', 'ER1', 'L', 'D'),
                stress_pattern=[
                  Stress.NON_VOWEL,
                  Stress.PRIMARY,
                  Stress.NON_VOWEL,
                  Stress.NON_VOWEL
                ]
              )
            )
          ]
        )

        phrase.to_phones()
        # should return ['HH EH0 L OW1', 'W ER1 L D']
        ```
        """
        return [" ".join(word.pf.phones) for word in self.words]

    @property
    def phones(self) -> Sequence[Text]:
        """Represent `clu.phontools.struct.Phrase` using a flat sequence of symbols denoting the phones of each word

        Example:
        ```python
        from clu.phontools.struct import *
        # define a phrase
        phrase = Phrase(
          words=[
            Word(
              word='hello',
              phonological_form=PhonologicalWord(
                phones=('HH', 'EH0', 'L', 'OW1'),
                stress_pattern=[
                  Stress.NON_VOWEL,
                  Stress.NO_STRESS,
                  Stress.NON_VOWEL,
                  Stress.PRIMARY
                ]
              )
            ),
            Word(
              word='world',
              phonological_form=PhonologicalWord(
                phones=('W', 'ER1', 'L', 'D'),
                stress_pattern=[
                  Stress.NON_VOWEL,
                  Stress.PRIMARY,
                  Stress.NON_VOWEL,
                  Stress.NON_VOWEL
                ]
              )
            )
          ]
        )

        phrase.to_phones()
        # should return ["HH", "EH0", "L", "OW1", "W", "ER1", "L", "D"]
        ```
        """
        return [phone for word in self.words for phone in word.pf.phones]

    @property
    def coarse_stress_pattern(self) -> Sequence[CoarseStress]:
        """Returns coarse stress pattern for each word in the Phrase"""
        return [word.pf.coarse_stress_pattern for word in self.words]

    @property
    def stress_pattern(self) -> Sequence[Stress]:
        """Returns stress pattern for each word in the Phrase"""
        return [word.pf.stress_pattern for word in self.words]

    def match_coarse_stress_pattern(self, pattern: Text) -> bool:
        """Checks if `clu.phontools.struct.Phrase matches` the specified coarse stress pattern (a regular expression).

        Example:
        ```python
        from clu.phontools.struct import *
        # define a phrase
        phrase = Phrase(
          words=[
            Word(
              word='hello',
              phonological_form=PhonologicalWord(
                phones=('HH', 'EH0', 'L', 'OW1'),
                stress_pattern=[
                  Stress.NON_VOWEL,
                  Stress.NO_STRESS,
                  Stress.NON_VOWEL,
                  Stress.PRIMARY
                ]
              )
            )
          ]
        )

        phrase.match_coarse_stress_pattern("WS")
        # should return True
        ```
        """
        return True if re.match(pattern, " ".join(self.coarse_stress)) else False

    def match_masked_syllables(self, pattern: Text, mask: Text = "X") -> bool:
        """Checks if `clu.phontools.struct.Phrase matches` the specified masked stress pattern (a regular expression).

        Example:
        ```python
        from clu.phontools.struct import *
        # define a phrase
        phrase = Phrase(
          words=[
            Word(
              word='hello',
              phonological_form=PhonologicalWord(
                phones=('HH', 'EH0', 'L', 'OW1'),
                stress_pattern=[
                  Stress.NON_VOWEL,
                  Stress.NO_STRESS,
                  Stress.NON_VOWEL,
                  Stress.PRIMARY
                ]
              )
            )
          ]
        )

        phrase.match_masked_syllables("^XX", mask="X")
        # should return True
        ```
        """
        return (
            True
            if re.match(pattern, " ".join(self.mask_syllables(mask=mask)))
            else False
        )

    def __iter__(self) -> Word:
        for word in self.words:
            yield word

    def __getitem__(self, i: int) -> Word:
        return self.words[i]

    def __reversed__(self) -> "Phrase":
        return Phrase(words=self.words[::-1])

    def __contains__(self, item) -> bool:
        return True if item in self.words else False

    def __len__(self) -> int:
        return len(self.words)

    def __hash__(self) -> int:
        return hash(tuple(hash(w) for w in self.words))


class LangUtils(ABC):
    """Utilities to be implemented for each language."""

    @staticmethod
    @abstractmethod
    def phonological_word_for(phones: Pronunciation) -> PhonologicalWord:
        """Produces a `clu.phontools.struct.PhonologicalWord` for a sequence of phones"""
        pass

    @staticmethod
    @abstractmethod
    def all_possible_forms_for(word: Text) -> Sequence[Word]:
        """Generates a list of `clu.phontools.struct.Word` from an orthographic form."""
        pass

    @staticmethod
    @abstractmethod
    def all_possible_phrases_for(words: Sequence[Text]) -> Sequence[Phrase]:
        """Generates a possible pronunciations from a sequence of words (as text)."""
        pass

    @staticmethod
    @abstractmethod
    def syllabify(pronunciation: Pronunciation) -> Sequence[Pronunciation]:
        """Abstract static method to syllabify a sequence of phones that constitute the pronunciation of a single lexical item.

        Example:
        A subclass that implements this method would ...
        ```python
        MyEnglishSyllabifier.syllabify(('P', 'ER0', 'M', 'IH1', 'T'))
        # should return [('P', 'ER0'), ('M', 'IH1', 'T')]
        ```
        """
        pass


# class StressSequence:
#     """A sequence of stress assignments.
#     """
#     sequence: List[Stress]
#
# class SimpleStressSequence:
#    sequence:
# stress = [str(p.value) for p in pron]
# ['-', '0', '-', '1', '-']
# syllable_structure =
# pron -> stress -> syllable counts
# ['-', '0', '-', '1', '-'] -> "WS"
# First token has two syllables: Strong Weak
# ["SW", "S", "W", "SW"]
# Each X represents a syllable
# ["X" ,"X" ,"X", "X", "XX"]
# mask_syllable_stress(["SW", "S", "W", "SW"]) -> ["XX", "X", "X", "XX"]
# Output:
# second token of transcript (1) inserts before weak syllable
# [(1, "IW")]
