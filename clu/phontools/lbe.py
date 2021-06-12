# coding: utf-8
from enum import Enum
from typing import Any, Dict, List, Text
from pydantic.dataclasses import dataclass
import json


class LexicalBoundaryErrorType(Enum):
    """
    An enumeration of all of the lexical boundary (LB) error types.
    """
    # insertion before weak syllable
    INSERTION_WEAK = "IW"
    # insertion before strong syllable
    INSERTION_STRONG = "IS"
    # deletion before weak syllable
    DELETION_WEAK = "DW"
    # deletion before strong syllable
    DELETION_STRONG = "DS"

@dataclass
class LexicalBoundaryError:
    """
    Encodes a single Lexical Boundary error
    """

    error_type: LexicalBoundaryErrorType
    target_index: int
    transcript_indices: List[int]

    def to_tuple(self):
        return (self.error_type, self.target_index, self.transcript_index)

    def to_dict(self):
        return {
            "target_index": self.target_index,
            "transcript_indices": self.transcript_indices,
            "error_type": self.error_type.name,
        }


@dataclass
class LexicalBoundaryErrorReport:
    # list attributes here
    target_stress: List[Text]
    transcript_stress: List[Text]
    lbes: List[LexicalBoundaryError]

    def to_dict(self) -> Dict[Text, Any]:
        # TODO: implement me by using class atributes

        # returns a json string (3 keys)
        return {
            "target_stress": self.target_stress,
            "transcript_stress": self.transcript_stress,
            "lbes": [lbe.to_dict() for lbe in self.lbes],  # list of dics
        }

# Example:
# take the first pron. for example word "permit"
# pron = en_cmu_dict.stress_for("permit")[0]
# @dataclass
# class StressSequence:
#  sequence: List[Stress]
#  def to_syllable_structure(self) -> List[Text]:
#     summary = []
#     for stress in self.sequence:
#       if stress == Stress.NO_STRESS:
#           summary.append("W")
#       elif if stress in { Stress.PRIMARY, Stress.SECONDARY }:
#           summary.append("S")
#     return "".join(summary)

# class CoarseStress(Enum):
#   """A coarse representation of stress is categorized as being either strong of weak."""
#   STRONG = "S"
#   WEAK   = "W"

# @dataclass 
# class PhonologicalWord:
#   """A [phonological word](https://en.wikipedia.org/wiki/Phonological_word) composed of one or more syllables"""
#   phones: List[Phone]  
#   """NOTE: For an EnglishSyllable, use en_cmu_dict as part of @staticmethod factory constructor"""
#   stress_pattern: List[Stress]
#
#   @property
#   def num_syllables(self):
#   """A syllable contains at most one stressed element (weak or strong)"""
#    return len(self.coarse_stress)
#  @property
#  def coarse_stress_pattern(self) -> List[CoarseStress]:
#     """Maps a detailed stress sequence to a sequence of strong and weak stressed syllabled"""
#     summary = []
#     for stress in self.sequence:
#       if stress == Stress.NO_STRESS:
#           summary.append(CoarseStress.WEAK)
#       elif if stress in { Stress.PRIMARY, Stress.SECONDARY }:
#           summary.append(CoarseStress.STRONG)
#     return summary

# class SyllableUtils:
#   @staticmethod
#   def to_coarse_syllable_word(pword: PhonologicalWord) -> Text:
#     """Converts a phonological word to a sequence of S (strong) or W (weak) symbols"""
#     return " ".join(cs.value for cs in pword.coarse_stress_pattern) 
#
#   @staticmethod
#   def to_syllable_masked_word(pword: PhonologicalWord, mask: Text = "X") -> Text:
#     """Converts a phonological word where each syllable is represented using the mask
#
#     conceptual examples:
#     "poo" -> "X" where mask is "X"
#     "July" -> "XX" where mask is "X"
#     """
#     return " ".join(cs.value for cs in pword.coarse_stress_pattern)  
#
# @dataclass
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

# FIXME: convert stress to 
def calculate_lbes(
    target: List[Text], transcript: List[Text]
) -> List[LexicalBoundaryError]:
    """Calculates lexical boundary errors using rules described in [(Jiao et al., 2019)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6808349/pdf/JSLHR-62-3359.pdf#page=4)"""
    target_remaining = [(tok, i) for (i, tok) in enumerate(target)]
    transcript_remaining = [(tok, i) for (i, tok) in enumerate(transcript)]

    errors = []
    while len(target_remaining) > 0 and len(transcript_remaining) > 0:
        target_term, target_idx = target_remaining[0]
        transcript_term, transcript_idx = transcript_remaining[0]

        # base case. no error
        if target_term == transcript_term:
            target_remaining = target_remaining[1:]
            transcript_remaining = transcript_remaining[1:]

        elif target_term.startswith(transcript_term):
            target_remaining[0] = (target_term[len(transcript_term) :], target_idx)
            transcript_remaining = transcript_remaining[1:]
            error = LexicalBoundaryError("insertion", target_idx, transcript_idx)
            errors.append(error)

        # FIXME: this is wrong
        else:
            transcript_term = transcript_term[1:]
            transcript_remaining[0] = (transcript_term, transcript_idx)
            error = LexicalBoundaryError("deletion", target_idx, transcript_idx)
            errors.append(error)

    # if we still have transcript tokens remaining, append them ...
    for (_, idx) in transcript_remaining:
        error = LexicalBoundaryError("new-tok", -1, idx)
        errors.append(error)

    return errors


# if __name__ == "__main__":

#   calculate_lbes(["01", "1", "01"], ["0", "01", "01"])

#   pairs = [
#     (["01", "1", "01"], ["01", "1", "01"]),
#     (["01", "1", "01"], ["0", "1", "1", "01"]),
#   ]

#   for target, transcript in pairs:
#     print(f"target:\t{target}")
#     print(f"transcript:\t{transcript}")
#     errors = calculate_lbes(target, transcript)
#     error_report = json.dumps([error.to_dict() for error in errors], indent=4)
#     print(f"errors: {error_report}")
#     print()
