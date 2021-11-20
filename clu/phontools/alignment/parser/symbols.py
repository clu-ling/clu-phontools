from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Text

__all__ = ["ParseSymbol", "TranscriptTypes"]


class TranscriptTypes(Enum):
    """"""

    GOLD: Text = "GOLD"
    TRANSCRIPT: Text = "TRANSCRIPT"


@dataclass
class ParseSymbol:
    """"""

    symbol: Text
    original_index: int
    index: int
    source: TranscriptTypes
