from __future__ import annotations
from .symbols import Symbol
from typing import List, Optional

__all__ = ["Stack"]


class Stack:
    """
    this class constrcuts a `Stack` based on the `Symbol` class where the following
    methods are used to deal with these symbols.
    1) copy()
    2) push()
    3) pop()
    4) is_empty()
    #
    
    The class should return a `Stack` object that contains a list of `Symbol`:
    Stack(
        [Symbol(original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD)]
        )
    """

    def __init__(self, symbols: Optional[List[Symbol]] = None):
        self._symbols: List[Symbol] = symbols or []

    def __len__(self) -> int:
        return len(self._symbols)

    def push(self, ps: Symbol) -> None:
        """Pushes a symbol onto the Stack"""
        self._symbols.append(ps)

    def copy(self) -> Stack:
        """Creates a new Stack from the current state of this Stack"""
        # deep copy
        return Stack(symbols=self._symbols[:])

    def pop(self) -> Optional[Symbol]:
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
