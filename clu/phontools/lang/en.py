from clu.phontools.struct import *
from clu.phontools.pronouncing import CMUPronouncingDict
from clu.phontools.struct import Word, PhonologicalWord, Phrase

class EnglishUtils(LangUtils):
    """English-specific implementation of `org.phontools.struct.LangTools`.
    """

    pronouncing_dict: CMUPronouncingDict = CMUPronouncingDict.from_cmu_dict()

    @staticmethod
    def phonological_word_for(phones: Pronunciation) -> PhonologicalWord:
        return PhonologicalWord(
            phones=phones, stress_pattern=EnglishUtils.pronouncing_dict.stress_for(phones)
        )

    # FIXME: consider having this return a generator
    @staticmethod
    def all_possible_forms_for(word: Text) -> Sequence[Word]:
        possible = []
        for pron in EnglishUtils.pronouncing_dict.get(word):
            possible.append(
                Word(word=word, phonological_form=EnglishUtils.phonological_word_for(pron))
            )
        return possible

    # FIXME: consider having this return a generator
    @staticmethod
    def all_possible_phrases_for(words: Sequence[Text]) -> Sequence[Phrase]:
        pronunciations = [EnglishUtils.all_possible_forms_for(w) for w in words]
        return [Phrase(words) for words in itertools.product(*pronunciations)]

    @staticmethod
    def syllabify(pronunciation: Pronunciation) -> Sequence[Pronunciation]:
        # FIXME: implement me
        return []