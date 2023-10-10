from clu.phontools.struct import *
from clu.phontools.pronouncing import CMUPronouncingDict
from clu.phontools.struct import Word, PhonologicalWord, Phrase


class ArabicUtils(LangUtils):

    pronouncing_dict: CMUPronouncingDict = CMUPronouncingDict.from_arabic_dict()

    @staticmethod
    def phonological_word_for(phones: Pronunciation) -> PhonologicalWord:
        return PhonologicalWord(
            phones=phones,
            stress_pattern=ArabicUtils.pronouncing_dict.stress_for(phones),
        )

    # FIXME: consider having this return a generator
    @staticmethod
    def all_possible_forms_for(word: Text) -> Sequence[Word]:
        possible = []
        for pron in ArabicUtils.pronouncing_dict.get(word):
            possible.append(
                Word(
                    word=word,
                    phonological_form=ArabicUtils.phonological_word_for(pron),
                )
            )
        return possible

    # FIXME: consider having this return a generator
    @staticmethod
    def all_possible_phrases_for(words: Sequence[Text]) -> Sequence[Phrase]:
        pronunciations = [ArabicUtils.all_possible_forms_for(w) for w in words]
        return [Phrase(words=words) for words in itertools.product(*pronunciations)]

    @staticmethod
    def syllabify(pronunciation: Pronunciation) -> Sequence[Pronunciation]:
        # FIXME: implement me
        return []
