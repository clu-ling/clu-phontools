# coding: utf-8
from enum import Enum
from typing import Any, Dict, List, Text
from pydantic.dataclasses import dataclass
import json


class LexicalBoundaryErrorType(Enum):
    """
    An enumeration of all of the LB error types.
    """

    IW = "IW"
    IS = "IS"
    DW = "DW"
    DS = "DS"
    # TODO: add more


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
            "error_type": self.error_type.value,
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


def calculate_lbes(
    target: List[Text], transcript: List[Text]
) -> List[LexicalBoundaryError]:
    """ """
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
