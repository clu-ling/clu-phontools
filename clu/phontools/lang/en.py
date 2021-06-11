from clu.phontools.traits import *
from clu.phontools.pronouncing import CMUPronouncingDict


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


en_cmu_dict = CMUPronouncingDict.from_cmu_dict()
