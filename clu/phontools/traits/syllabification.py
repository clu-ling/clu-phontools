from abc import ABC, abstractmethod
from typing import List, Tuple
from clu.phontools.struct import Pronunciation, Phone


class Syllabification(ABC):
    @staticmethod
    @abstractmethod
    def syllabify(pronunciation: Pronunciation) -> List[Tuple[Phone]]:
        """Abstract static method to syllabify a sequence of phones constituting the pronunciation of a single lexical item.

        Example:
        A subclass that implements this method would ...
        ```python
        MyEnglishSyllabifier.syllabify(('P', 'ER0', 'M', 'IH1', 'T'))
        # should return [('P', 'ER0'), ('M', 'IH1', 'T')]
        ```
        """
        pass
