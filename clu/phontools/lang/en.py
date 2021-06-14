from clu.phontools.traits import *
from clu.phontools.pronouncing import CMUPronouncingDict
from clu.phontools.traits import Pronunciation
from clu.phontools.struct import Word, PhonologicalWord

en_cmu_dict = CMUPronouncingDict.from_cmu_dict()


class RuleBasedSyllabification(Syllabification):
    @staticmethod
    def syllabify(pronunciation: Pronunciation) -> List[Tuple[Phone]]:
        """Rule-based syllabification for English

        Example:
        ```python
        RuleBasedSyllabification.syllabify(('P', 'ER0', 'M', 'IH1', 'T'))
        # should return [('P', 'ER0'), ('M', 'IH1', 'T')]
        ```
        """
        # FIXME: implement me!
        return []


class Utils(object):
    @staticmethod
    def to_phonological_word(phones: Pronunciation) -> PhonologicalWord:
        """ """
        return PhonologicalWord(
            phones=phones, stress_pattern=en_cmu_dict.stress_for(phones)
        )

    @staticmethod
    def all_possible_forms(word: Text) -> List[Word]:
        """Generates a list of `clu.phontools.struct.Word` from an orthographic form."""
        possible = []
        for pron in en_cmu_dict.get(word):
            possible.append(
                Word(word=word, phonological_form=Utils.to_phonological_word(pron))
            )
        return possible
