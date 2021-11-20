from __future__ import annotations
from .symbols import ParseSymbol
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

__all__ = ["Stack"]


class Stack:
    """"""

    def __init__(self, symbols: List[ParseSymbol] = []):
        self._symbols: List[ParseSymbol] = symbols

    def __len__(self) -> int:
        return len(self._symbols)

    # TODO: implement me
    def push(self) -> None:
        """Pushes a symbol onto the Stack"""
        pass

    def copy(self) -> Stack:
        """Creates a new Stack from the current state of this Stack"""
        # deep copy
        return Stack(symbols=self._symbols[:])

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
