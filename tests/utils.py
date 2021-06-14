from clu.phontools.struct import *

words1: Sequence[Word] = (
    Word(
        word="permit",
        phonological_form=PhonologicalWord(
            phones=("P", "ER0", "M", "IH1", "T"),
            stress_pattern=[
                Stress.NON_VOWEL,
                Stress.NO_STRESS,
                Stress.NON_VOWEL,
                Stress.PRIMARY,
                Stress.NON_VOWEL,
            ],
        ),
    ),
    Word(
        word="me",
        phonological_form=PhonologicalWord(
            phones=("M", "IY1"),
            stress_pattern=[Stress.NON_VOWEL, Stress.PRIMARY],
        ),
    ),
    Word(
        word="to",
        phonological_form=PhonologicalWord(
            phones=("T", "UW1"),
            stress_pattern=[Stress.NON_VOWEL, Stress.PRIMARY],
        ),
    ),
    Word(
        word="ask",
        phonological_form=PhonologicalWord(
            phones=("AE1", "S", "K"),
            stress_pattern=[Stress.PRIMARY, Stress.NON_VOWEL, Stress.NON_VOWEL],
        ),
    ),
)
phrase1: Phrase = Phrase(words=words1)
