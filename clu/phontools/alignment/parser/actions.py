from __future__ import annotations
from enum import Enum

__all__ = ["Actions"]


class Actions(Enum):
    """
    The actions used by the parser.
    """

    DISCARD_T = "DISCARD-T"
    DISCARD_G = "DISCARD-G"
    SHIFT_T = "SHIFT-T"
    SHIFT_G = "SHIFT-G"
    STACK_SWAP = "STACK-SWAP"
    INSERTION_PRESERVE_COPY_CHILD = "INSERTION-PRESERVE-COPY-CHILD"
    INSERTION_PRESERVE_COPY_PARENT = "INSERTION-PRESERVE-COPY-PARENT"
    DELETION_PRESERVE_COPY_CHILD = "DELETION-PRESERVE-COPY-CHILD"
    DELETION_PRESERVE_COPY_PARENT = "DELETION-PRESERVE-COPY-PARENT"
    ALIGN = "ALIGN"
    SUBSTITUTION = "SUBSTITUTION"
    DELETION = "DELETION"

    def describe(self):
        return self.name, self.value
