from __future__ import annotations
from .symbols import Symbol
from typing import List, Optional

__all__ = ["Queue"]


class Queue:
    """this class constrcuts a `Queue` based on the `Symbol` class where the following
    methods are used to deal with these symbols.
    1) copy()
    2) push()
    3) pop()
    4) is_empty()
    #
    
    The class should return a `Queue` object that contains a list of `Symbol`:
    Queue(
        [Symbol(original_index=0, index=0, symbol="a", source=TranscriptTypes.GOLD)]
        )
    """

    def __init__(self, symbols: Optional[List[Symbol]] = None):
        self._symbols: List[Symbol] = symbols or []

    def __len__(self) -> int:
        return len(self._symbols)

    def copy(self) -> Queue:
        """Creates a new Queue from the current state of this Queue"""
        # deep copy
        return Queue(symbols=self._symbols[:])

    def push(self, ps: Symbol) -> None:
        """pushes an element into the first position of the queue"""
        self._symbols = [ps] + self._symbols

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
