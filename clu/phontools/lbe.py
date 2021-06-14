# coding: utf-8
from enum import Enum
from clu.phontools.struct import Phrase
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
            "lbes": [lbe.to_dict() for lbe in self.lbes],  # list of dicts
        }


# FIXME: WIP
def calculate_lbes_from_phrases(
    target_phrase: Phrase, transcript_phrase: Phrase
) -> List[LexicalBoundaryError]:
    """Calculates lexical boundary errors from stress-based syllable structures via a pair of `clu.phontools.struct.Phrase` using rules described in [(Jiao et al., 2019)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6808349/pdf/JSLHR-62-3359.pdf#page=4)"""
    target: Sequence[Text] = target_phrase.coarse_stress
    # FIXME: should these be masked?
    transcript: Sequence[Text] = target_phrase.mask_syllables(mask="X")
    errors: Sequence[LexicalBoundaryError] = calculate_lbes_from_stress(
        target, transcript
    )
    # TODO: return an error report
    return errors


def calculate_lbes_from_stress(
    target: Sequence[Text], transcript: Sequence[Text]
) -> Sequence[LexicalBoundaryError]:
    """Calculates lexical boundary errors from stress-based syllable structures using rules described in [(Jiao et al., 2019)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6808349/pdf/JSLHR-62-3359.pdf#page=4)"""
    target_remaining = [(tok, i) for (i, tok) in enumerate(target)]
    transcript_remaining = [(tok, i) for (i, tok) in enumerate(transcript)]

    errors = []
    while len(target_remaining) > 0 and len(transcript_remaining) > 0:
        target_term, target_idx = target_remaining[0]
        transcript_term, transcript_idx = transcript_remaining[0]

        # base case. no error
        # FIXME: if masked, only length matters, if not equivalence works.
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

#         target = 'address'
#         transcript = 'add is'
#         ReAline.align(target, transcript)


# for this small job of deletion before weak:
#     WS (01) + W (0) > WSW (010)
# firs loop for stress pattern in target for WS 01 followed by W 0
# print True if found in target
# loop in transcribed to find the 010


# for key in a_dict:
# ...     print(key, '->', a_dict[key])

# indtance of deletion before strong
# divide across retreat = ['01', '01', '01']
# 'the body cross returned' = ['0', '10', '1', '01']
# IS 01 > 0 and 1 added to next syllable divide > the body
#  DW 01 > 0 accross > cross

# index[0]01 index[1]01 index[2] 01
# idex[0]0 index[1]0 index[2]1 index[3] 01


# if there is a space after 0 and before 1, this I
# if there is a

# Q1 Is there one index in target mapped to multiple indecies in transcribed?
#     YES, Example 01 > 0 1  or 10 > 1 0
#     example: address  her ['01', '0'] in  'address her meeting time' address ['01']
#         is mapped to 0
# Q2 Is there one index in transcribed mapped to multiple indecies in trarget?
#     example: address  her ['01', '0'] in  'address her meeting time' address ['01']
#         is mapped to index[0]  in 'adjusted reading time' adjusted = WSW 010


# [49]: for i in transcript:
#     ...: for k, v in d.items():
#     ...: if i == k:
#     ...: print(i, v)
