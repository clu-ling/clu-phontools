from clu.phontools.lang.en import EnglishUtils

res = EnglishUtils.all_possible_phrases_for(["permit", "for", "transport"])

phrase = res[0]

# syllable structure in terms of stress (weak or strong)
phrase.coarse_stress
# should return ['WS', 'S', 'S', 'S']

# num. syllables for each word represented using a mask.
phrase.mask_syllables(mask="X")
# should return ['XX', 'X', 'X', 'X']

# (['WS', 'S', 'WS'], ['WS', 'S', 'SW']) -> insertion strong?
# (['WS', 'S', 'WS'], ['WS', 'S']) -> deletion weak?


# [(['p', 'ER0', 'm', 'IH1', 't'], 'WS'), (['f', 'AO1', 'ɹ'], 'S'), (['t', 'ɹ', 'AE0', 'n', 's', 'p', 'AO1', 'ɹ', 't'], 'WS')]


# ["WS"] -> ["W", "S"] = (IS, seq1=0, seq2=1) # the second element of seq2 was placed as an "IS" at posiiton 0 for seq1
