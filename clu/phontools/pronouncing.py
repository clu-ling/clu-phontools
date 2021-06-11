from typing import Dict, Text, Tuple, List, Optional
from clu.phontools.struct import Pronunciation, Word, Stress
import os


# FIXME: add APRAbetToIPA mappings
arpabet_to_ipa: Dict[str, str] = {}

ipa_to_arpabet = {v: k for k, v in arpabet_to_ipa.items()}


class PronouncingDict(dict):
    """
    Maps tuples of pronunciations -> lexical entries
    """

    def __init__(self, pairs: List[Tuple[Word, Pronunciation]] = []):
        self._dict: Dict[Word, List[Pronunciation]] = self._generate_dict(pairs)

    def stress_for(self, pronunciation: Pronunciation) -> List[int]:
        """
        Subclasses of PronunciationDict should implement stress_for
        """
        return []

    def _preprocess_key(self, key: Word) -> Word:
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

    def get(self, key: Text) -> Word:
        return self._dict.get(self._preprocess_key(key), [])

    def add(self, key: Pronunciation, value: Word) -> None:
        self._dict[self._preprocess_key(key)] = value

    def __getitem__(self, key: Word) -> List[Pronunciation]:
        return self._dict.__getitem__(key)

    def __setitem__(self, key: Word, value: List[Pronunciation]) -> None:
        self._dict.__setitem__(self, self._preprocess_key(key), value)

    def _generate_dict(
        self, pairs: List[Tuple[Word, Pronunciation]]
    ) -> Dict[Word, List[Pronunciation]]:
        pronounciation_dict = dict()
        for (k, v) in pairs:
            key = self._preprocess_key(k)
            pronunciations = pronounciation_dict.get(key, [])
            pronunciations.append(v)
            pronounciation_dict[key] = pronunciations
        return pronounciation_dict


class CMUPronouncingDict(PronouncingDict):
    def __init__(self, pairs: List[Tuple[Word, Pronunciation]] = []):
        super().__init__(pairs)

    def stress_for(self, pronunciation: Pronunciation) -> List[Stress]:
        """
        Subclasses of PronunciationDict should implement stress_for
        """
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
        filepath: Optional[str] = None, converter: Dict[str, str] = arpabet_to_ipa
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
