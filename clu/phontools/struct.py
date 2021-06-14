from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any, Text, Sequence
import re
import itertools
from autocorrect import Speller
from clu.phontools.lbe import LexicalBoundaryErrorReport
from pydantic.dataclasses import dataclass
import numpy as np


Pronunciation = Tuple[Text, ...]
Phone = Text
# type alias for a string of characters representing a word
SimpleWord = Text


spell = Speller(lang="en")

class Stress(Enum):
    """Enumeration of all possible stress values"""

    NON_VOWEL = "-"
    NO_STRESS = "0"
    PRIMARY = "1"
    SECONDARY = "2"

    def __repr__(self) -> Text:
        return f"Stress.{self.name}"


class CoarseStress(Enum):
    """A coarse representation of stress is categorized as being either strong of weak."""

    STRONG = "S"
    WEAK = "W"

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
@dataclass
class PhonologicalWord(SyllableProperties):
    """A [phonological word](https://en.wikipedia.org/wiki/Phonological_word) composed of one or more syllables"""

    phones: Sequence[Phone]
    """NOTE: For an EnglishSyllable, use en_cmu_dict as part of @staticmethod factory constructor"""
    stress_pattern: Sequence[Stress]

@dataclass
class Word:
    """The smallest sequence of phonemes that can be uttered in isolation with objective or practical meaning."""

    word: Text
    phonological_form: PhonologicalWord
    
    @property
    def pf(self) -> PhonologicalWord:
        """Alias for phonological_form"""
        return self.phonological_form

    def graphemes(self) -> List[Text]:
        return "".split(self.word)


@dataclass
class Phrase:
  """A sequence of `org.phontools.struct.Word` constitutes a Phrase"""
  words: Sequence[Word]

  @property
  def coarse_stress(self) -> Sequence[Text]:
    """Returns coarse stress form for each word in the Phrase"""
    return [word.pf.coarse_stress for word in self.words]

  def mask_syllables(self, mask: Text = "X") -> Sequence[Text]:
    """Returns coarse stress form for each word in the Phrase"""
    return [word.pf.mask_syllables(mask)for word in self.words]

  @property
  def coarse_stress_pattern(self) -> Sequence[CoarseStress]:
    """Returns coarse stress pattern for each word in the Phrase"""
    return [word.pf.coarse_stress_pattern for word in self.words]

  @property
  def stress_pattern(self) -> Sequence[Stress]:
    """Returns stress pattern for each word in the Phrase"""
    return [word.pf.stress_pattern for word in self.words]

class LangUtils(ABC):
  """Utilities to be implemented for each language.
  """

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
      """Generates a possible pronunciations from a sequence of words (as text). 
      """
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
