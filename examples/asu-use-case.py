# coding: utf-8
from clu.phontools.lang.en import EnglishUtils
from clu.phontools.struct import *
from clu.phontools.pronouncing import ConverterUtils
from clu.phontools.alignment.realine import *
from clu.phontools.alignment.lbe import *

# prompt/target is "balance clamp and bottle"
# get all pronunciations for the phrase
target_phrases = EnglishUtils.all_possible_phrases_for(
    ["balance", "clamp", "and", "bottle"]
)

# in this case, there should be 2:
assert len(target_phrases) == 2

# let's examine the stress patterns...
for phrase in target_phrases:
    print(phrase.coarse_stress)

# our stress pattern of interest
pattern = "SW S W SW"

# find the first Phrase that matches our pattern.
# we'll use the first entry (stress pattern = ["SW", "S", "W", "SW"])
# as our target.
match_stress = lambda phrase: phrase.match_coarse_stress_pattern(pattern)
target: Phrase = next(filter(match_stress, target_phrases))

# transcript says "bell is glad a bottle"
# get all pronunciations for the phrase
transcript_phrases = EnglishUtils.all_possible_phrases_for(
    ["bell", "is", "glad", "a", "bottle"]
)

# in this case, there should be 4:
assert len(transcript_phrases) == 4

# all of these phrases have 6 syllables with the structure "X X X X XX".
# If you're unfamiliar with regular expressions, keep in mind that ...
#   ^ in the pattern below means "starts with"
#   $ in the pattern below denotes the "end of sequence"
all(
    phrase.match_masked_syllables(pattern="^X X X X XX$", mask="X")
    for phrase in transcript_phrases
)

# for our comparisons, let's use the first one:
transcript: Phrase = transcript_phrases[0]

# let's calculate lexical boundary errors for the first one:
aligner = ReAline()

# by default, ReAline expects to align IPA,
# so we'll first want to convert our ARPABet-based representations to IPA
target_phones = [ConverterUtils.arpabet_to_ipa(phone) for phone in target.phones]
transcript_phones = [
    ConverterUtils.arpabet_to_ipa(phone) for phone in transcript.phones
]
alignment = aligner.align(target_phones, transcript_phones)
# alignment should be [('b', 'b'), ('æ', 'ɛ'), ('l', 'l'), ('ʌ', 'i'), ('n', '-'), ('s', 'z'), ('k', 'g'), ('l', 'l'), ('æ', 'æ'), ('m', '-'), ('p', '-'), ('ʌ', '-'), ('n', '-'), ('d', 'd'), ('-', 'ʌ'), ('b', 'b'), ('ɒ', 'ɒ'), ('t', 't'), ('ʌ', 'ʌ'), ('l', 'l')]

# Next, let's calculate phoneme errors:
phoneme_errors = aligner.phoneme_errors(alignment)

# Next, let's calculate lexical boundary errors:

target_stress = target.coarse_stress
# should produce ['SW', 'S', 'W', 'SW']

transcript_masked_stress = transcript.mask_syllables(mask="X")
# should produce ['X', 'X', 'X', 'X', 'XX']

lbe_errors = calculate_lbes_from_stress(target_stress, transcript_masked_stress)
# should produce [LexicalBoundaryError(error_type=LexicalBoundaryErrorType.INSERTION_WEAK, target_index=0, transcript_index=0)]
