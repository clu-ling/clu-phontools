from __future__ import annotations
from enum import Enum
from typing import Text, Tuple

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
    INSERTION_PRESERVE_CHILD = "INSERTION-PRESERVE-CHILD"
    INSERTION_PRESERVE_PARENT = "INSERTION-PRESERVE-PARENT"
    DELETION_PRESERVE_CHILD = "DELETION-PRESERVE-CHILD"
    DELETION_PRESERVE_PARENT = "DELETION-PRESERVE-PARENT"
    ALIGN = "ALIGN"
    SUBSTITUTION = "SUBSTITUTION"
    DELETION = "DELETION"

    def describe(self) -> Tuple[Text, Text]:
        return (self.name, self.value)

    def simple(self) -> Text:
        """A simplified/more coarse-grained version of the label."""
        label = self.value
        for prefix in [
            "INSERT",
            "ALIGN",
            "DELETION",
            "SUBSTITUTION",
            "SHIFT",
            "DISCARD",
        ]:
            if label.startswith(prefix):
                return prefix
        return label
