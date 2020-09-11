from __future__ import unicode_literals
class LanguageFeatures(object):
      def __init__(self, consonant_matrix, vowel_matrix, salience, C_skip, C_sub, C_exp, C_vwl):
            self.consonant_matrix = consonant_matrix
            self.vowel_matrix = vowel_matrix
            self.salience = salience
            self.C_skip = C_skip
            self.C_sub = C_sub
            self.C_exp = C_exp
            self.C_vwl = C_vwl
            #Combine both feature matrices
            self.feature_matrix = consonant_matrix + vowel_matrix
            #Ensure features are valid
            self.sanity_check()

      def sanity_check(self):
            #ensure C_* take values in an acceptable range
            #ensure all feature values are accounted for in salience dict
            pass

      
# class EnglishFeatures(LanguageFeatures):
#       def __init__(self, C_skip, C_sub, C_exp, C_vwl):
#             # Default values for maximum similarity scores (Kondrak 2002: 54)
#             self.C_skip = 10  # Indels
#             self.C_sub = 35  # Substitutions
#             self.C_exp = 45  # Expansions/compressions
#             self.C_vwl = 5  # Vowel/consonant relative weight (decreased from 10)
           
      
# === Constants ===

inf = float('inf')

# Default values for maximum similarity scores (Kondrak 2002: 54)
C_skip = 10  # Indels
C_sub = 35  # Substitutions
C_exp = 45  # Expansions/compressions
C_vwl = 5  # Vowel/consonant relative weight (decreased from 10)

consonants = [
      'N', 'R', 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
      'n', 'p', 'q', 'r', 's', 't', 'v', 'x', 'z', 'ç', 'ð', 'ħ',
      'ŋ', 'ɖ', 'ɟ', 'ɢ', 'ɣ', 'ɦ', 'ɬ', 'ɮ', 'ɰ', 'ɱ', 'ɲ', 'ɳ', 'ɴ',
      'ɸ', 'ɹ', 'ɻ', 'ɽ', 'ɾ', 'ʀ', 'ʁ', 'ʂ', 'ʃ', 'ʈ', 'ʋ', 'ʒ',
      'ʔ', 'ʕ', 'ʙ', 'ʝ', 'β', 'θ', 'χ', 'ʐ', 'w', 'ɜ', 'ɡ', 'LB'
]

# consonants in the original aline (NLTK)
# consonants = [
#     "B", "N", "R", "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n",
#     "p", "q", "r", "s", "t", "v", "x", "z", "ç", "ð", "ħ", "ŋ", "ɖ", "ɟ",
#     "ɢ", "ɣ", "ɦ", "ɬ", "ɮ", "ɰ", "ɱ", "ɲ", "ɳ", "ɴ", "ɸ", "ɹ", "ɻ", "ɽ",
#     "ɾ", "ʀ", "ʁ", "ʂ", "ʃ", "ʈ", "ʋ","ʐ", "ʒ", "ʔ", "ʕ", "ʙ", "ʝ", "β",
#     "θ", "χ", "ʐ", "w",
# ]


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
    'trill': 0.7, 'tap': 0.65, 'approximant': 0.6,
    #high
#     'high': 0.4, 'mid': 0.2,
    'high': 1.0, 'mid': 0.5, 'low': 0.0, 'vowel2': 0.5,  # added vowel
    #back
    'front': 1.0, 'central': 0.5, 'back': 0.0,
    #binary features
    'plus': 1.0, 'minus': 0.0,
    # lexical boundary
    'lexical': 0.0,
}

# Relative weights of phonetic features (Kondrak 2002: 55)
# TODO: convert to defaultdict with 0 as default value?
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
    'boundary': 0,
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
# need to be verified
    'ɡ': {'place': 'velar', 'manner': 'stop', 'syllabic': 'minus', 'voice': 'plus',
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

    # Vowels w/ stress
    # FIXME: correct features and values for stress
    'ɑ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'back', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'ɑ1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'back', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'ɑ2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'back', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'ɑ3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'back', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
      # FIXME: correct features and values for stress
    'ɪ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ɪ1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ɪ2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ɪ3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},

      # FIXME: correct features and values for stress
    'i': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'i1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'i2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'i3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'y': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'y1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'y2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'y3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'e': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'e1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'e2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'e3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'E': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'E1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'E2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'E3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'ø': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'ø1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'ø2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'ø3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'ɛ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ɛ1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ɛ2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ɛ3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},  
    # FIXME: correct features and values for stress
    'œ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'œ1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'œ2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'œ3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'front', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'æ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'æ1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'æ2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'æ3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'a': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'front', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'a1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'front', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'a2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'front', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'a3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'front', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'A': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'A1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'A2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'A3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'ɨ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'central', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ɨ1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'central', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ɨ2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'central', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ɨ3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'central', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'ʉ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'central', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'ʉ1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'central', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'ʉ2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'central', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'ʉ3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'central', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'ə': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'central', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ə1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'central', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ə2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'central', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ə3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'central', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'u': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    'u1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    'u2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    'u3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'U': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    'U1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    'U2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    'U3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'o': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    'o1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    'o2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    'o3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'O': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    'O1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    'O2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    'O3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'ɔ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    'ɔ1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    'ɔ2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    'ɔ3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'plus', 'long': 'plus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'ɒ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'back', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ɒ1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'back', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ɒ2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'back', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ɒ3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'low',
          'back': 'back', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'I': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'I1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'I2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    'I3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'front', 'round': 'minus', 'long': 'plus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'ʌ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ʌ1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ʌ2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    'ʌ3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'mid',
          'back': 'back', 'round': 'minus', 'long': 'minus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'ʊ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'ʊ1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'ʊ2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'ʊ3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    # FIXME: correct features and values for stress
    'ɜ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'ɜ1': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'ɜ2': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'ɜ3': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
          'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
          'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},

    # Diphthongs
    'ɑɪ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
        'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
        'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'ɑi': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
        'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
        'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'ɔɪ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
        'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
        'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
    'ɑʊ': {'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
        'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
        'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus'},
            

    # FIXME: are these all needed?
     'LB': {
           'place': 'vowel', 'manner': 'vowel2', 'syllabic': 'plus', 'voice': 'plus',
           'nasal': 'minus', 'retroflex': 'minus', 'lateral': 'minus', 'high': 'high',
           'back': 'back', 'round': 'plus', 'long': 'minus', 'aspirated': 'minus',
           'boundary': 'lexical',
           }
#      'LB': {
#              'boundary': 'lexical','aspirated': 'minus',
#    }

}
