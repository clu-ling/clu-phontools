from enum import Enum
from typing import List, Dict, Tuple, Any, Text
import re
import itertools
from autocorrect import Speller
from clu.phontools.lbe import LexicalBoundaryErrorReport
from clu.phontools.traits import Pronunciation, Phone, Word, SyllableProperties
from pydantic.dataclasses import dataclass
import numpy as np

#Pronunciation, Phone, Word
# Pronunciation = Tuple[Text, ...]
# Phone = Text
# Word = Text


spell = Speller(lang="en")


class Stress(Enum):
    """Enumeration of all possible stress values
    """
    NON_VOWEL = '-'
    NO_STRESS = "0"
    PRIMARY = "1"
    SECONDARY = "2"

    def __repr__(self) -> Text:
      return f"Stress.{self.name}"

class CoarseStress(Enum):
  """A coarse representation of stress is categorized as being either strong of weak."""
  STRONG = "S"
  WEAK   = "W"

  def __repr__(self) -> Text:
    return f"CoarseStress.{self.name}"

@dataclass 
class PhonologicalWord(SyllableProperties):
  """A [phonological word](https://en.wikipedia.org/wiki/Phonological_word) composed of one or more syllables"""
  phones: List[Phone]
  """NOTE: For an EnglishSyllable, use en_cmu_dict as part of @staticmethod factory constructor"""
  stress_pattern: List[Stress]

  @property
  def coarse_stress_pattern(self) -> List[CoarseStress]:
    """Maps a detailed stress sequence to a sequence of strong and weak stressed syllabled"""
    summary = []
    for stress in self.stress_pattern:
      if stress == Stress.NO_STRESS:
          summary.append(CoarseStress.WEAK)
      elif stress in { Stress.PRIMARY, Stress.SECONDARY }:
          summary.append(CoarseStress.STRONG)
    return summary

  @property
  def num_syllables(self):
    """A syllable contains at most one stressed element (weak or strong)"""
    return len(self.coarse_stress_pattern)

  def to_coarse_syllable_form(self) -> Text:
    return " ".join(cs.value for cs in self.coarse_stress_pattern) 

  def to_syllable_masked_form(self, mask: Text = "X") -> Text:
    return " ".join(cs.value for cs in self.coarse_stress_pattern)  

@dataclass 
class Word(SyllableProperties):
  """The smallest sequence of phonemes that can be uttered in isolation with objective or practical meaning.
  """
  phonological_form: PhonologicalWord
  word: Text

  def graphemes(self) -> List[Text]:
    return "".split(self.word)

  def to_coarse_syllable_form(self) -> Text:
    return self.phonological_form.to_coarse_syllable_word()

  def to_syllable_masked_form(self, mask: Text = "X") -> Text:
    return self.phonological_form.to_syllable_masked_word(mask)

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