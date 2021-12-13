from __future__ import annotations

# from dataclasses import dataclass
from enum import Enum
from typing import Literal, Text

__all__ = ["Symbol", "TranscriptTypes"]


class TranscriptTypes(Enum):
    """the types of the two inputs to the parser"""

    GOLD: Text = "GOLD"
    TRANSCRIPT: Text = "TRANSCRIPT"


class Symbol:
    """this class creates a `Symbol` object where it adds the NULL symbol to the symbols of both the GOLD and TRANSCRIPT """

    NULL: Literal["NULL"] = "NULL"

    def __init__(
        self, symbol: Text, original_index: int, index: int, source: TranscriptTypes
    ):
        self.symbol: Text = symbol
        self.original_index: int = original_index
        self.index: int = index
        self.source: TranscriptTypes = source

    def is_null(self) -> bool:
        """Checks whether the symbol is NULL"""
        return self.symbol == Symbol.NULL

    @staticmethod
    def create_null(index: int, source: TranscriptTypes) -> Symbol:
        """Easily create a Symbol for NULL"""
        return Symbol(original_index=-1, index=index, symbol=Symbol.NULL, source=source)


