# Identify syllable boundaries using a CRF

# http://www.sfu.ca/person/dearmond/220/220.syllable.htm


# DUMP MEMM to decision tree?

# ('P', 'ER0', 'M', 'IH1', 'T')
# [('P', 'ER0'), ('M', 'IH1', 'T')]


# en_cmu_dict.get("pam")
# [('P', 'AE1', 'M')]

# en_cmu_dict.get("papa")
# [('P', 'AA1', 'P', 'AH2')]
# [('PAA1'), ('PAH2')]
# [B-SYLLABLE, I-SYLLABLE, B-SYLLABLE, O-SYLLABLE]


# en_cmu_dict.get("permIt")
# Out[3]: [('P', 'ER0', 'M', 'IH1', 'T'), ('P', 'ER1', 'M', 'IH2', 'T')]
