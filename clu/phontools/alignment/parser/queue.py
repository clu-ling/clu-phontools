from __future__ import annotations
from .symbols import ParseSymbol
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

__all__ = ["Queue"]


class Queue:
    """"""

    def __init__(self, symbols: List[ParseSymbol] = []):
        self._symbols: List[ParseSymbol] = symbols

    def __len__(self) -> int:
        return len(self._symbols)

    def copy(self) -> Queue:
        """Creates a new Queue from the current state of this Queue"""
        # deep copy
        return Queue(symbols=self._symbols[:])

    def pop(self) -> Optional[ParseSymbol]:
        """pops off the first element in the queue
        and sets self._symbols to whatever remains"""
        # check if Queue is empty
        if self.is_empty():
            return None

        first = self._symbols[0]
        self._symbols = self._symbols[1:]
        return first

    def is_empty(self) -> bool:
        """returns true is Queue is empty otherwise false"""
        return True if len(self._symbols) == 0 else False
