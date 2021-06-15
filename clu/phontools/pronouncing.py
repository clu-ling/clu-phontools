from abc import ABC, abstractmethod
from typing import Dict, Text, Tuple, List, Optional, Sequence
from clu.phontools.struct import Pronunciation, SimpleWord, Stress
import os


# FIXME: add more symbols
# TODO: test cases
arpabet_to_ipa: Dict[Text, Text] = {
    "AA": "ɒ",
    "AE": "æ",
    "AH": "ʌ",
    "AO": "ɔ",
    "AW": "aʊ",
    "AY": "ai",
    "B": "b",
    "CH": "tʃ",
    "D": "d",
    "DH": "ð",
    "EH": "ɛ",
    "ER": "ə",
    "EY": "ei",
    "F": "f",
    "G": "g",
    "HH": "h",
    "IH": "i",
    "IY": "I",
    "JH": "dʒ",
    "K": "k",
    "L": "l",
    "M": "m",
    "N": "n",
    "NG": "ŋ",
    "OW": "oʊ",
    "OY": "ɔi",
    "P": "p",
    "R": "ɹ",
    "S": "s",
    "SH": "ʃ",
    "T": "t",
    "TH": "θ",
    "UH": "ʊ",
    "UW": "U",
    "V": "v",
    "W": "w",
    "Y": "j",
    "Z": "z",
    "ZH": "ʒ",
}

ipa_to_arpabet = {v: k for k, v in arpabet_to_ipa.items()}


class PronouncingDict(dict, ABC):
    """
    Maps tuples of pronunciations -> lexical entries
    """

    def __init__(self, pairs: List[Tuple[SimpleWord, Pronunciation]] = []):
        self._dict: Dict[Word, List[Pronunciation]] = self._generate_dict(pairs)

    @abstractmethod
    def stress_for(self, pronunciation: Pronunciation) -> Sequence[Stress]:
        """Returns the stress assignment for each phone in the pronunciation

        Subclasses of `clu.phontools.pronouncing.PronouncingDict` should implement `clu.phontools.pronouncing.PronouncingDict.stress_for`
        """
        pass

    def _preprocess_key(self, key: SimpleWord) -> SimpleWord:
        return key.lower()

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def items(self):
        return self._dict.items()

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def get(self, key: Text) -> SimpleWord:
        return self._dict.get(self._preprocess_key(key), [])

    def add(self, key: Pronunciation, value: SimpleWord) -> None:
        self._dict[self._preprocess_key(key)] = value

    def __getitem__(self, key: SimpleWord) -> List[Pronunciation]:
        return self._dict.__getitem__(key)

    def __setitem__(self, key: SimpleWord, value: List[Pronunciation]) -> None:
        self._dict.__setitem__(self, self._preprocess_key(key), value)

    def _generate_dict(
        self, pairs: List[Tuple[SimpleWord, Pronunciation]]
    ) -> Dict[SimpleWord, List[Pronunciation]]:
        pronounciation_dict = dict()
        for (k, v) in pairs:
            key = self._preprocess_key(k)
            pronunciations = pronounciation_dict.get(key, [])
            pronunciations.append(v)
            pronounciation_dict[key] = pronunciations
        return pronounciation_dict


class CMUPronouncingDict(PronouncingDict):
    def __init__(self, pairs: List[Tuple[SimpleWord, Pronunciation]] = []):
        super().__init__(pairs)

    def stress_for(self, pronunciation: Pronunciation) -> Sequence[Stress]:
        """Returns the stress assignment for each phone in the pronunciation"""
        stress_pattern = []
        for phone in pronunciation:
            assignment = Stress.NON_VOWEL
            for symbol in phone:
                if symbol == "0":
                    assignment = Stress.NO_STRESS
                    break
                elif symbol == "1":
                    assignment = Stress.PRIMARY
                    break
                elif symbol == "2":
                    assignment = Stress.SECONDARY
                    break
            stress_pattern.append(assignment)
        assert len(stress_pattern) == len(
            pronunciation
        ), "each phone must have a stress assignment (non-vowels should be assigned Stress.NON_VOWEL)"
        return stress_pattern

    @staticmethod
    def from_cmu_dict(
        filepath: Optional[str] = None, converter: Dict[str, str] = dict()
    ) -> "CMUPronouncingDict":
        cmudict_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "resources", "cmudict"
        )
        filepath = filepath or cmudict_file
        pairs = []
        with open(filepath, "r", encoding="ISO-8859-1") as infile:
            for row in infile:
                # ignore comments
                if not row.startswith(";;"):
                    res = row.strip().split("  ")
                    # discard (x) for any entries with multiple pronunciations
                    key = res[0].lower()
                    # permit(1) -> permit
                    # permit -> permit
                    key = key.split("(", -1)[0] if key.endswith(")") else key
                    # "{LEFT-BRACE" -> "{"
                    key = key if key[0].isalnum() else key[0]
                    pronunciation = "".join(res[1:]).split(" ")
                    # ARPAbet pronunciation.
                    # optionally convert to provided format
                    value = tuple(converter.get(phon, phon) for phon in pronunciation)
                    pairs.append((key, value))
        return CMUPronouncingDict(pairs)
