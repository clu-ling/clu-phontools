# coding: utf-8
from clu.phontools.lang.en import EnglishUtils
from clu.phontools.struct import Phrase

res = EnglishUtils.all_possible_phrases_for(["permit", "for", "transport"])

phrase: Phrase = res[0]

# syllable structure in terms of stress (weak or strong)
phrase.coarse_stress
# should return ['WS', 'S', 'S', 'S']

# num. syllables for each word represented using a mask.
phrase.mask_syllables(mask="X")
# should return ['XX', 'X', 'X', 'X']

# (['WS', 'S', 'WS'], ['WS', 'S', 'SW']) -> insertion strong?
# (['WS', 'S', 'WS'], ['WS', 'S']) -> deletion weak?


# [(['p', 'ER0', 'm', 'IH1', 't'], 'WS'), (['f', 'AO1', 'ɹ'], 'S'), (['t', 'ɹ', 'AE0', 'n', 's', 'p', 'AO1', 'ɹ', 't'], 'WS')]


# ["WS"] -> ["W", "S"] = (IS, seq1=0, seq2=1) # the second element of seq2 was placed as an "IS" at position 0 for seq1


# 1. is num. words different from target phrase?
# len(phrase1) == len(phrase2)

# 2.

# target "balance clamp and bottle"
target_coarse_stress = ["SW", "S", "W", "SW"]

# target "bell is glad a bottle"
transcript_coarse_stress = ["X", "X", "X", "X", "XX"]

target = ["SW", "S", "W", "SW"]
transcript = ["X", "X", "X", "X", "XX"]
