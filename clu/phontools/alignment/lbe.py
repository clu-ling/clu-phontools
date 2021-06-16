# coding: utf-8
from enum import Enum
from clu.phontools.struct import Phrase, CoarseStress, Stress
from typing import Any, Dict, List, Text, Sequence
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
import json


class LexicalBoundaryErrorType(Enum):
    """An enumeration of all of the lexical boundary (LB) error types."""

    INSERTION_WEAK = "IW"
    """insertion before weak syllable"""

    INSERTION_STRONG = "IS"
    """insertion before strong syllable"""

    DELETION_WEAK = "DW"
    """deletion before weak syllable"""

    DELETION_STRONG = "DS"
    """deletion before strong syllable"""

    UNKNOWN = "UNK"
    """unknown LBE error"""


class LexicalBoundaryError(BaseModel):
    """
    Encodes a single Lexical Boundary error
    """

    error_type: LexicalBoundaryErrorType
    target_index: int
    transcript_index: int

    def to_tuple(self):
        return (self.error_type, self.target_index, self.transcript_index)

    def to_dict(self):
        return {
            "target_index": self.target_index,
            "transcript_index": self.transcript_index,
            "error_type": self.error_type.name,
        }


class LexicalBoundaryErrorReport(BaseModel):
    # list attributes here
    target: Phrase
    transcript: Phrase
    lbes: Sequence[LexicalBoundaryError]

    def to_dict(self) -> Dict[Text, Any]:
        # TODO: implement me by using class atributes

        # returns a json string (3 keys)
        return {
            "target_stress": self.target_stress,
            "transcript_stress": self.transcript_stress,
            "lbes": [lbe.to_dict() for lbe in self.lbes],  # list of dicts
        }


def calculate_lbes_from_phrases(
    target_phrase: Phrase, transcript_phrase: Phrase
) -> LexicalBoundaryErrorReport:
    """Calculates lexical boundary errors from stress-based syllable structures via a pair of `clu.phontools.struct.Phrase` using rules described in [Jiao et al. (2019)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6808349/pdf/JSLHR-62-3359.pdf#page=4)"""
    target: Sequence[Text] = target_phrase.coarse_stress
    # FIXME: should these be masked?
    transcript: Sequence[Text] = target_phrase.mask_syllables(mask="X")
    errors: Sequence[LexicalBoundaryError] = calculate_lbes_from_stress(
        target, transcript
    )
    return LexicalBoundaryErrorReport(
        target=target_phrase, transcript=transcript_phrase, lbes=errors
    )


def calculate_lbes_from_stress(
    target: Sequence[Text], transcript: Sequence[Text]
) -> Sequence[LexicalBoundaryError]:
    """Calculates lexical boundary errors from stress-based syllable structures using rules described in [(Jiao et al., 2019)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6808349/pdf/JSLHR-62-3359.pdf#page=4)

    :param target: A sequence of syllables in terms of strong (S) or weak (W) stress (ex. ["SW", "S"]) representing the target to which we're comparing.
    :param transcript: A sequence of syllables in terms of strong (S) or weak (W) stress (ex. ["SW", "S"]) corresponding to some transcript.
    """
    target_remaining = [(tok, i) for (i, tok) in enumerate(target)]
    transcript_remaining = [(tok, i) for (i, tok) in enumerate(transcript)]

    errors = []
    while len(target_remaining) > 0 and len(transcript_remaining) > 0:
        target_term, target_idx = target_remaining[0]
        transcript_term, transcript_idx = transcript_remaining[0]

        # base case. no error
        if len(target_term) == len(transcript_term):
            # advance both sequences
            target_remaining = target_remaining[1:]
            transcript_remaining = transcript_remaining[1:]

        # length mismatch (insertion case)
        elif len(target_term) > len(transcript_term):
            # 1. remove the num. syllables from transcript from target
            target_remaining[0] = (target_term[len(transcript_term) :], target_idx)
            # 2. advance transcript by 1 word
            transcript_remaining = transcript_remaining[1:]
            # get new current symbols
            target_term, target_idx = target_remaining[0]
            # 3. categorize insertion error
            if target_term[0] == CoarseStress.WEAK.value:
                error = LexicalBoundaryError(
                    error_type=LexicalBoundaryErrorType.INSERTION_WEAK,
                    target_index=target_idx,
                    transcript_index=transcript_idx,
                )
            elif target_term[0] == CoarseStress.STRONG.value:
                error = LexicalBoundaryError(
                    error_type=LexicalBoundaryErrorType.INSERTION_STRONG,
                    target_index=target_idx,
                    transcript_index=transcript_idx,
                )
            errors.append(error)

        # length mismatch (deletion case)
        elif len(target_term) < len(transcript_term):
            # 1. remove the num. syllables from target from transcript
            transcript_remaining[0] = (
                transcript_term[len(target_term) :],
                transcript_idx,
            )
            # 2. advance target
            target_remaining = target_remaining[1:]
            # get new current symbols
            if len(target_remaining) > 0:
                target_term, target_idx = target_remaining[0]
            if len(transcript_remaining) > 0:
                transcript_term, transcript_idx = transcript_remaining[0]

            # 3. categorize deletion error
            if target_term[0] == CoarseStress.WEAK.value:
                error = LexicalBoundaryError(
                    error_type=LexicalBoundaryErrorType.DELETION_WEAK,
                    target_index=target_idx,
                    transcript_index=transcript_idx,
                )
            elif target_term[0] == CoarseStress.STRONG.value:
                error = LexicalBoundaryError(
                    error_type=LexicalBoundaryErrorType.DELETION_STRONG,
                    target_index=target_idx,
                    transcript_index=transcript_idx,
                )
            errors.append(error)
        # FIXME:
        # transcript_term = transcript_term[1:]
        # transcript_remaining[0] = (transcript_term, transcript_idx)
        # error = LexicalBoundaryError("deletion", target_idx, transcript_idx)
        # errors.append(error)

    # if we still have transcript tokens remaining, append them ...
    for (_, idx) in transcript_remaining:
        error = LexicalBoundaryError(
            error_type=LexicalBoundaryErrorType.UNKNOWN,
            target_index=-1,
            transcript_index=idx,
        )
        errors.append(error)
    # print(f"\ntarget:     {target}")
    # print(f"transcript: {transcript}")
    return errors
