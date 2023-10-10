from __future__ import unicode_literals

"""
The description of the Modern Standard Arabic (MSA) sounds is based on:
1. Karin Ryding. (2014). Arabic: A Linguistic Introduction. Cambrdige University Press.
2. Gairdner, W. (1925). The Phonetics of Arabic. The American University in Cairo.
"""

inf = float("inf")

# Default values for maximum similarity scores (Kondrak 2002: 54)
C_skip = 10  # Indels
C_sub = 35  # Substitutions
C_exp = 45  # Expansions/compressions
C_vwl = 5  # Vowel/consonant relative weight (decreased from 10)

# consonants for Mondern Standard Arabic (msa)
consonants = [
    "b",
    "t",
    "θ",
    "ʒ",
    "ħ",
    "x",
    "d",
    "ð",
    "r",
    "z",
    "s",
    "ʃ",
    "sˤ",
    "dˤ",
    "tˤ",
    "ðˤ",
    "ʕ",
    "ɣ",
    "f",
    "q",
    "k",
    "l",
    "m",
    "n",
    "h",
    "w",
    "j",
    "ʔ",
    "h",
]

# vowels for Mondern Standard Arabic (msa)
vowels = ["a", "i", "u", "aː", "iː", "uː"]

# Relevant features for comparing consonants and vowels
R_c = [
    "aspirated",
    "lateral",
    "manner",
    "nasal",
    "place",
    "retroflex",
    "syllabic",
    "voice",
]
# 'high' taken out of R_v because same as manner
R_v = [
    "back",
    "lateral",
    "long",
    "manner",
    "nasal",
    "place",
    "retroflex",
    "round",
    "syllabic",
    "voice",
]

# Flattened feature matrix (Kondrak 2002: 56)
similarity_matrix = {
    # place
    "bilabial": 1.0,
    "labiodental": 0.95,
    "dental": 0.9,
    "alveolar": 0.85,
    "retroflex": 0.8,
    "palato-alveolar": 0.75,
    "palatal": 0.7,
    "velar": 0.6,
    "uvular": 0.5,
    "pharyngeal": 0.3,
    "glottal": 0.1,
    "labiovelar": 1.0,
    "vowel": -1.0,  # added 'vowel'
    # manner
    "stop": 1.0,
    "affricate": 0.9,
    "fricative": 0.85,  # increased fricative from 0.8
    "trill": 0.7,
    "tap": 0.65,
    "approximant": 0.6,
    # high
    #'high': 0.4, 'mid': 0.2,
    "high": 1.0,
    "mid": 0.5,
    "low": 0.0,
    "vowel2": 0.5,  # added vowel
    # back
    "front": 1.0,
    "central": 0.5,
    "back": 0.0,
    # binary features
    "plus": 1.0,
    "minus": 0.0,
    # lexical boundary
    "lexical": 0.0,
}

# Relative weights of phonetic features (Kondrak 2002: 55)
# TODO: convert to defaultdict with 0 as default value?
salience = {
    "syllabic": 5,
    "place": 40,
    "manner": 50,
    "voice": 5,  # decreased from 10
    "nasal": 20,  # increased from 10
    "retroflex": 10,
    "lateral": 10,
    "aspirated": 5,
    "long": 0,  # decreased from 1
    "high": 3,  # decreased from 5
    "back": 2,  # decreased from 5
    "round": 2,  # decreased from 5
    "boundary": 0,
}


# (Kondrak 2002: 59-60)
feature_matrix = {
    # Consonants
    "ʔ": {
        "place": "glottal",
        "manner": "stop",
        "syllabic": "minus",
        "voice": "minus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "b": {
        "place": "bilabial",
        "manner": "stop",
        "syllabic": "minus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "t": {
        "place": "alveolar",
        "manner": "stop",
        "syllabic": "minus",
        "voice": "minus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "θ": {
        "place": "dental",  # FIXME: interdental: find the values
        "manner": "fricative",
        "syllabic": "minus",
        "voice": "minus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "ʒ": {
        "place": "palato-alveolar",  # FIXME: there are 3 variants at least
        "manner": "fricative",
        "syllabic": "minus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "ħ": {
        "place": "pharyngeal",
        "manner": "fricative",
        "syllabic": "minus",
        "voice": "minus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "x": {
        "place": "velar",  # FIXME: it can be uvular also. we can add another description
        "manner": "fricative",
        "syllabic": "minus",
        "voice": "minus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "d": {
        "place": "alveolar",
        "manner": "stop",
        "syllabic": "minus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "ð": {
        "place": "dental",  # FIXME: inter-dental?
        "manner": "fricative",
        "syllabic": "minus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "r": {
        "place": "alveolar",  # FIXME: singelton r is tap while geminated is trill
        "manner": "trill",
        "syllabic": "minus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "ɾ": {
        "place": "alveolar",
        "manner": "tap",
        "syllabic": "minus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "z": {
        "place": "alveolar",
        "manner": "fricative",
        "syllabic": "minus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "s": {
        "place": "alveolar",
        "manner": "fricative",
        "syllabic": "minus",
        "voice": "minus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "ʃ": {
        "place": "palatal",
        "manner": "fricative",
        "syllabic": "minus",
        "voice": "minus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "sˤ": {
        "place": "alveolar",  # FIXME: these are emphatics?!
        "manner": "fricative",
        "syllabic": "minus",
        "voice": "minus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "dˤ": {
        "place": "alveolar",
        "manner": "stop",
        "syllabic": "minus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "tˤ": {
        "place": "alveolar",
        "manner": "stop",
        "syllabic": "minus",
        "voice": "minus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "ðˤ": {
        "place": "dental",  # FIXME: there might be two variants.
        "manner": "fricative",
        "syllabic": "minus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "ʕ": {
        "place": "pharyngeal",
        "manner": "fricative",
        "syllabic": "minus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "ɣ": {
        "place": "velar",  # FIXME: it can be uvular as well
        "manner": "fricative",
        "syllabic": "minus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "f": {
        "place": "labiodental",
        "manner": "fricative",
        "syllabic": "minus",
        "voice": "minus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "q": {
        "place": "uvular",
        "manner": "stop",
        "syllabic": "minus",
        "voice": "minus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "k": {
        "place": "velar",
        "manner": "stop",
        "syllabic": "minus",
        "voice": "minus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "l": {
        "place": "alveolar",  # FIXME: might consider clear /l/ and dark /l/
        "manner": "approximant",
        "syllabic": "minus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "m": {
        "place": "bilabial",
        "manner": "stop",
        "syllabic": "minus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "n": {
        "place": "alveolar",
        "manner": "stop",
        "syllabic": "minus",
        "voice": "plus",
        "nasal": "plus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "h": {
        "place": "glottal",
        "manner": "fricative",
        "syllabic": "minus",
        "voice": "minus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "w": {
        "place": "labiovelar",
        "manner": "approximant",
        "syllabic": "minus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    "j": {
        "place": "palatal",
        "manner": "approximant",
        "syllabic": "minus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "aspirated": "minus",
    },
    # VOWELS
    "a": {
        "place": "vowel",
        "manner": "vowel2",
        "syllabic": "plus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "high": "low",
        "back": "central",  # FIXME: it can be front as well (check).
        "round": "minus",
        "long": "minus",
        "aspirated": "minus",
    },
    "i": {
        "place": "vowel",
        "manner": "vowel2",
        "syllabic": "plus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "high": "high",
        "back": "front",
        "round": "minus",
        "long": "minus",
        "aspirated": "minus",
    },
    "u": {
        "place": "vowel",
        "manner": "vowel2",
        "syllabic": "plus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "high": "high",
        "back": "back",
        "round": "plus",
        "long": "minus",
        "aspirated": "minus",
    },
    "aː": {
        "place": "vowel",
        "manner": "vowel2",
        "syllabic": "plus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "high": "low",
        "back": "central",
        "round": "minus",
        "long": "plus",
        "aspirated": "minus",
    },
    "iː": {
        "place": "vowel",
        "manner": "vowel2",
        "syllabic": "plus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "high": "high",
        "back": "front",
        "round": "minus",
        "long": "plus",
        "aspirated": "minus",
    },
    "uː": {
        "place": "vowel",
        "manner": "vowel2",
        "syllabic": "plus",
        "voice": "plus",
        "nasal": "minus",
        "retroflex": "minus",
        "lateral": "minus",
        "high": "high",
        "back": "back",
        "round": "plus",
        "long": "plus",
        "aspirated": "minus",
    },
}
