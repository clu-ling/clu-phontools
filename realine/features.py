from __future__ import unicode_literals
# === Constants ===

inf = float('inf')

# Default values for maximum similarity scores (Kondrak 2002: 54)
C_skip = 10  # Indels
C_sub = 35  # Substitutions
C_exp = 45  # Expansions/compressions
C_vwl = 5  # Vowel/consonant relative weight (decreased from 10)

consonants = ['B', 'N', 'R', 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
              'n', 'p', 'q', 'r', 's', 't', 'v', 'x', 'z', 'ç', 'ð', 'ħ',
              'ŋ', 'ɖ', 'ɟ', 'ɢ', 'ɣ', 'ɦ', 'ɬ', 'ɮ', 'ɰ', 'ɱ', 'ɲ', 'ɳ', 'ɴ',
              'ɸ', 'ɹ', 'ɻ', 'ɽ', 'ɾ', 'ʀ', 'ʁ', 'ʂ', 'ʃ', 'ʈ', 'ʋ', 'ʐ ', 'ʒ',
              'ʔ', 'ʕ', 'ʙ', 'ʝ', 'β', 'θ', 'χ', 'ʐ', 'w', '4', '5', 'ɜ', 'L', 'B']

# Relevant features for comparing consonants and vowels
R_c = ['aspirated', 'lateral', 'manner', 'nasal', 'place', 'retroflex',
       'syllabic', 'voice']
# 'high' taken out of R_v because same as manner
R_v = ['back', 'lateral', 'long', 'manner', 'nasal', 'place',
       'retroflex', 'round', 'syllabic', 'voice']

# Flattened feature matrix (Kondrak 2002: 56)
similarity_matrix = {
    #place
    'bilabial': 1.0, 'labiodental': 0.95, 'dental': 0.9,
    'alveolar': 0.85, 'retroflex': 0.8, 'palato-alveolar': 0.75,
    'palatal': 0.7, 'velar': 0.6, 'uvular': 0.5, 'pharyngeal': 0.3,
    'glottal': 0.1, 'labiovelar': 1.0, 'vowel': -1.0,  # added 'vowel'
    #manner
    'stop': 1.0, 'affricate': 0.9, 'fricative': 0.85,  # increased fricative from 0.8
    'trill': 0.7, 'tap': 0.65, 'approximant': 0.6, 'high vowel': 0.4,
    'mid vowel': 0.2, 'low vowel': 0.0, 'vowel2': 0.5,  # added vowel
    #high
    'high': 1.0, 'mid': 0.5, 'low': 0.0,
    #back
    'front': 1.0, 'central': 0.5, 'back': 0.0,
    #binary features
    'plus': 1.0, 'minus': 0.0,
    # lexical boundary
    'lexical': 1.0,


}

# Relative weights of phonetic features (Kondrak 2002: 55)
salience = {
    'syllabic': 5,
    'place': 40,
    'manner': 50,
    'voice': 5,  # decreased from 10
    'nasal': 20,  # increased from 10
    'retroflex': 10,
    'lateral': 10,
    'aspirated': 5,
    'long': 0,  # decreased from 1
    'high': 3,  # decreased from 5
    'back': 2,  # decreased from 5
    'round': 2,  # decreased from 5
    'boundary': 1,
}

# (Kondrak 2002: 59-60)
feature_matrix = {
    # Consonants
    'tʃ': {'place': 'palato-alveolar', 'manner': 'affricate', 'syllabic': 'minus', 'voice': 'minus',
           'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'dʒ': {'place': 'palato-alveolar', 'manner': 'affricate', 'syllabic': 'minus', 'voice': 'plus',
           'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'p': {'place': 'bilabial', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'b': {'place': 'bilabial', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    't': {'place': 'alveolar', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'd': {'place': 'alveolar', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ʈ': {'place': 'retroflex', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'plus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ɖ': {'place': 'retroflex', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'plus', 'lateral': 'minus', 'aspirated': 'minus'},

    'c': {'place': 'palatal', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ɟ': {'place': 'palatal', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'k': {'place': 'velar', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'g': {'place': 'velar', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'q': {'place': 'uvular', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ɢ': {'place': 'uvular', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ʔ': {'place': 'glottal', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'm': {'place': 'bilabial', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'plus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ɱ': {'place': 'labiodental', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'plus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'n': {'place': 'alveolar', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'plus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ɳ': {'place': 'retroflex', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'plus', 'retroflex': 'plus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ɲ': {'place': 'palatal', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'plus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ŋ': {'place': 'velar', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'plus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ɴ': {'place': 'uvular', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'plus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'N': {'place': 'uvular', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'plus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ʙ': {'place': 'bilabial', 'manner': 'trill', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'B': {'place': 'bilabial', 'manner': 'trill', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'r': {'place': 'alveolar', 'manner': 'trill', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'plus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ʀ': {'place': 'uvular', 'manner': 'trill', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'R': {'place': 'uvular', 'manner': 'trill', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ɾ': {'place': 'alveolar', 'manner': 'tap', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ɽ': {'place': 'retroflex', 'manner': 'tap', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'plus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ɸ': {'place': 'bilabial', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'β': {'place': 'bilabial', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'f': {'place': 'labiodental', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'v': {'place': 'labiodental', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'θ': {'place': 'dental', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ð': {'place': 'dental', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    's': {'place': 'alveolar', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'z': {'place': 'alveolar', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ʃ': {'place': 'palato-alveolar', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ʒ': {'place': 'palato-alveolar', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ʂ': {'place': 'retroflex', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'plus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ʐ': {'place': 'retroflex', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'plus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ç': {'place': 'palatal', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ʝ': {'place': 'palatal', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'x': {'place': 'velar', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ɣ': {'place': 'velar', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'χ': {'place': 'uvular', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ʁ': {'place': 'uvular', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ħ': {'place': 'pharyngeal', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ʕ': {'place': 'pharyngeal', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'h': {'place': 'glottal', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ɦ': {'place': 'glottal', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ɬ': {'place': 'alveolar', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'minus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'plus', 'aspirated': 'minus'},

    'ɮ': {'place': 'alveolar', 'manner': 'fricative', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'plus', 'aspirated': 'minus'},

    'ʋ': {'place': 'labiodental', 'manner': 'approximant', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ɹ': {'place': 'alveolar', 'manner': 'approximant', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ɻ': {'place': 'retroflex', 'manner': 'approximant', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'plus', 'lateral': 'minus', 'aspirated': 'minus'},

    'j': {'place': 'palatal', 'manner': 'approximant', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'ɰ': {'place': 'velar', 'manner': 'approximant', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    'l': {'place': 'alveolar', 'manner': 'approximant', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'plus', 'aspirated': 'minus'},

    'w': {'place': 'labiovelar', 'manner': 'approximant', 'syllabic': 'minus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'aspirated': 'minus'},

    # Vowels
    'ɑ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'back', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},

    'ɪ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},

    'i': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},

    'y': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},

    'e': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},

    'E': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},

    'ø': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},

    'ɛ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},

    'œ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},

    'æ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},

    'a': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'front', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},

    'A': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},

    'ɨ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'central', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},

    'ʉ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'central', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},

    'ə': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'central', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},

    'u': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},

    'U': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},

    'o': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},

    'O': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},

    'ɔ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},

    'ɒ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'back', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},

    'I': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},

    'ʌ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},

    'ʊ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},

    'ɜ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},

    'L': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},

    'B': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},

}
