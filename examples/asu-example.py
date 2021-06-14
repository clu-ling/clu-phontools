[[["I"], ["i"]], [["a"]]]
list(itertools.product(*test))

import itertools

from clu.phontools.lang.en import en_cmu_dict

phrase = ["permit", "for", "transport"]

pronunciations = [en_cmu_dict.get(w) for w in phrase]

possible_pronunciation_sequences = list(itertools.product(*pronunciations))

# pronounciation for first word of first sequence
pw1 = possible_pronunciation_sequences[0][0]
print(pw1)

# what's the stress pattern?
[p.name for p in en_cmu_dict.stress_for(pw1)]

[str(p.value) for p in en_cmu_dict.stress_for(pw1)]

# Two syllables (no specification of boundary):
# ['-', '0', '-', '1', '-'] -> "WS"


from clu.phontools.lang.en import Utils
import itertools

phrase = ["permit", "for", "transport"]

# all pronunciations of each word
res = [Utils.all_possible_forms(term) for term in phrase]

# cartesian prod.
possible_pronunciation_sequences = list(itertools.product(*res))

# syllables for first phrase
[word.to_coarse_syllable_form() for word in possible_pronunciation_sequences[0]]


# (['WS', 'S', 'WS'], ['WS', 'S', 'SW']) -> insertion strong?
# (['WS', 'S', 'WS'], ['WS', 'S']) -> deletion weak?


# [(['p', 'ER0', 'm', 'IH1', 't'], 'WS'), (['f', 'AO1', 'ɹ'], 'S'), (['t', 'ɹ', 'AE0', 'n', 's', 'p', 'AO1', 'ɹ', 't'], 'WS')]


# ["WS"] -> ["W", "S"] = (IS, seq1=0, seq2=1) # the second element of seq2 was placed as an "IS" at posiiton 0 for seq1
