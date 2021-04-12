from enum import Enum
import re
from scipy.io import loadmat, savemat
from autocorrect import Speller
import pronouncing
import numpy as np
from typing import List, Dict, Tuple, Any
import itertools
from dataclasses import dataclass

spell = Speller(lang='en')

class LexicalBoundaryErrorType(Enum):
    '''
    avoid typos with strings. enumerate all of the lb error types. 
    '''
    IW = "IW"
    IS = "IS"
    DW = "DW"
    DS = "DS"
    #TODO: add more

@dataclass
class LexicalBoundaryError:
    target_index:            int
    transcript_indices: List[int]
    error_type: LexicalBoundaryErrorType

    def to_dict(self):
        return {
            "target_index": self.target_index,
          # add other two here
            }

@dataclass
class LexicalBoundaryErrorReport:
   # list attributes here
    target_stress: List[str]
    transcript_stress: List[str]
    lbes: List[LexicalBoundaryError]
   # more here ...
   # NOTE: unsure all of all types needed for values

    def to_dict(self) -> Dict[str, Any]:
    # TODO: implement me by using class atributes

        #returns a json string (3 keys)
        return {
            "target_stress": self.target_stress,
            "transcript_stress": self.transcript_stress,
            "lbes": [lbe.to_dict() for lbe in self.lbes] # list of dics
        }


class Phrase(object):

    def possible_pronunciations(self, phrase: List[str]) -> List[List[str]]:
        '''
        This function takes a list of phrases and returns a list of list of cmu pronunciations
        OUTPUT EXAMPLE:
        [['AH0 D R EH1 S', 'HH ER0', 'M IY1 T IH0 NG', 'T AY1 M'], ['AH0 D M IH1 T', 'DH IY0', 'G IH1 R', 'B IH0 AO1 N D']]
        '''
        data = [np.array(i.split(',')) for i in phrase]
        pronunciations = []
        for item in data:
            item = str(item[0])
            words = re.split(r'\s+', item)
            phone = []
            for word in words:
                word = spell(word).lower()
                word = word.lower()
                pronunciation = pronouncing.phones_for_word((word))
                if len(pronunciation) == 1:
                    current_phone = pronunciation[0]
                elif len(pronunciation) == 2:
                    current_phone = pronunciation[1]
                else:
                    current_phone = pronunciation[2]
                phone.append(current_phone)      
            pronunciations.append(phone)
        return pronunciations

    def generate_stress_assignment(self, pronounciation: List[str]) -> List[List[str]]:
        '''
        This function takes a list of list of cmu pronunciations and returns a list of lists.
        OUTPUT EXAMPLE:
        [['01', '0', '10', '1'], ['01', '0', '1', '01']]
        '''
        stresses = []
        for i in pronounciation:
            stress = []
            for pronounciations in i:
                stress.append(pronouncing.stresses(pronounciations))
            stresses.append(stress)
        return stresses


    def arpabet_to_ipa(self) -> Dict[str, str]:
        '''
        This function outputs a dictonary: 
        KEY: Arpabet symbol
        VALUE: ipa symbol
        '''
        # FIXME: add more symbols 
        # TODO: test cases
        arpabet_to_ipa: Dict[str, str] = {
            'AA': 'ɒ', 'AE': 'æ', 'AH': 'ʌ', 'AO': 'ɔ', 'AW': 'aʊ', 'AY': 'ai', 'B': 'b', 'CH': 'tʃ',
            'D': 'd', 'DH': 'ð', 'EH': 'ɛ', 'ER': 'ə', 'EY': 'ei', 'F': 'f', 'G': 'g', 'HH': 'h', 'IH':
            'i', 'IY': 'I', 'JH': 'dʒ', 'K': 'k', 'L': 'l', 'M': 'm', 'N': 'n', 'NG': 'ŋ', 'OW': 'oʊ',
            'OY': 'ɔi', 'P': 'p', 'R': 'ɹ', 'S': 's', 'SH': 'ʃ', 'T': 't', 'TH': 'θ', 'UH': 'ʊ', 'UW': 'U',
            'V': 'v', 'W': 'w', 'Y': 'j', 'Z': 'z', 'ZH': 'ʒ'}
        return arpabet_to_ipa

    def string_to_arpabet(self, phrase: str) -> Tuple[List[str]]:
        '''
        This function takes a phrase (string) and outputs a tuple of 
        two lists. The first list is a list of cmu pronunciations and
        the second list is a list of the corresponding stress patterns
        OUTPUT EXAMPLE:
        (['AH0 D R EH1 S', 'HH ER0', 'M IY1 T IH0 NG', 'T AY1 M'], ['01', '0', '10', '1'])
        '''
        # FIXME: this should be a list of tuples.
        words = re.split(r'\s+', phrase)
        cmu = possible_pronunciations(words)
        cmu_flat = [i for element in cmu for i in element]
        stress = generate_stress_assignment(cmu)
        stress_flat = [i for element in stress for i in element]
        return cmu_flat, stress_flat

    
    # return lbe errors
    def calc_lbes(self, target_stress: List[str], transcript_stress: List[str]) -> List[LexicalBoundaryErrorReport]:
        '''
        This function a target stress pattern and a transcript stress pattern and returns
        a decompisition of lexical boundary errors.
        LBE_IS: Insertion Strong
        LBE_IW: Insertion Weak
        LBE_DS: Deletion Strong
        LBE_DW: Deletion Weak
        EXPECTED INPUT: target = ['01', '0', '10', '1'] - transcript = ['01', '0', '10', '1']
        EXPECTED OUTPUT: (0.0, 1.0, 1.0, 0.0)
        '''
        if len(''.join(transcript_stress)) >= 7 or len(''.join(transcript_stress)) <= 5:
            return None, None, None, None
        if len(''.join(transcript_stress)) == 6:
            LBE_IS_count = 0
            LBE_IW_count = 0
            LBE_DS_count = 0
            LBE_DW_count = 0

            loc_target_stress = []
            #print(loc_target_stress)
            for ind_stress in range(len(target_stress)):
                if ind_stress == 0:
                    loc_target_stress.append(len(target_stress[ind_stress]))
                else:
                    loc_target_stress.append(
                        len(target_stress[ind_stress]) + loc_target_stress[-1])

            loc_transcript_stress = []
            for ind_stress in range(len(transcript_stress)):
                if ind_stress == 0:
                    loc_transcript_stress.append(len(transcript_stress[ind_stress]))
                else:
                    loc_transcript_stress.append(len(transcript_stress[ind_stress]) + loc_transcript_stress[-1])

            concat_target_stress = ''.join(target_stress)
            #print(concat_target_stress)
            #print(target_stress)
            #print(transcript_stress)
            for stress in loc_transcript_stress:
                if stress not in loc_target_stress:
                    #print(concat_target_stress)
                    #print(stress)
                    if concat_target_stress[stress] == '1':
                        LBE_IS_count += 1
                    elif concat_target_stress[stress] == '0':
                        LBE_IW_count += 1
            for stress in loc_target_stress:
                if stress not in loc_transcript_stress:
                    if concat_target_stress[stress] == '1':
                        LBE_DS_count += 1
                    elif concat_target_stress[stress] == '0':
                        LBE_DW_count += 1
            LBE_IS = float(LBE_IS_count)
            LBE_IW = float(LBE_IW_count)
            LBE_DS = float(LBE_DS_count)
            LBE_DW = float(LBE_DW_count)
        s = LBE_IS, LBE_IW, LBE_DS, LBE_DW
        return s


if __name__ == '__main__':
    phrases = ['address her meeting time', 'admit the gear beyond']
    p = Phrase()
    


    p = possible_pronunciations(phrases)
    s = generate_stress_assignment(p)
    a = arpabet_to_ipa()
    ph = 'address her meeting time'
    b = processTarget(ph)
    print(b)
    a = processTarget(ph)
    print(a[1])
    #FIXME: write test cases
    #DW: deletion before week (her) - this is the lexical boundary before (her)
    target = ['01', '0', '10', '1'] # address her meeting time
    transcript = ['010', '10', '1'] # adjusted reading time
    transcript = ['1', '0', '0', '10', '1']
    transcript = ['01', '01', '0', '1']
    #insertion before strong syllable 
    IS = []
    #insertion before week syllable
    IW = []
    #deletion before strong syllable
    DS = []
    #deletion before week syllable
    DW = []
    iS, iW, dS, dW = calcLBE(target, transcript)
    IS.append(iS)
    IW.append(iW)
    DS.append(dS)
    DW.append(dW)
    cc = [i for i in target if i in transcript]
    print(cc)
    hh = {'01': 'WS', '0': 'W', '10':'SW', '1':'S'}
    for i in target:
        if i == '0':
            print(i, 'W')
        elif i == '1':
            print(i, 'S')
        elif i == '10':
            print(i, 'SW')
        elif i == '01':
            print(i, 'WS')
    if len(target) == len(transcript):
        c = zip(target, transcript)
        print(type(c))
        for i in c:
            if i[0] == i[1]:
                print(i, 'No lexical boundary')
            elif i[0] != i[1]:
                if len(i[0]) > len(i[1]):
                    print(i, 'There is a lexical boundary: Deletion')
                else:
                    print(i, 'There is a lexical boundary: Insertion')
    else:
        print('How are you, ASU?')



#         target = 'address'
#         transcript = 'add is'
#         ReAline.align(target, transcript)


# for this small job of deletion before weak:
#     WS (01) + W (0) > WSW (010)
# firs loop for stress pattern in target for WS 01 followed by W 0
# print True if found in target
# loop in transcribed to find the 010 


# for key in a_dict:
# ...     print(key, '->', a_dict[key])

# indtance of deletion before strong 
# divide across retreat = ['01', '01', '01']
# 'the body cross returned' = ['0', '10', '1', '01']
# IS 01 > 0 and 1 added to next syllable divide > the body
#  DW 01 > 0 accross > cross 

# index[0]01 index[1]01 index[2] 01 
# idex[0]0 index[1]0 index[2]1 index[3] 01



# if there is a space after 0 and before 1, this I
# if there is a 

# Q1 Is there one index in target mapped to multiple indecies in transcribed?
#     YES, Example 01 > 0 1  or 10 > 1 0 
#     example: address  her ['01', '0'] in  'address her meeting time' address ['01']
#         is mapped to 0
# Q2 Is there one index in transcribed mapped to multiple indecies in trarget?
#     example: address  her ['01', '0'] in  'address her meeting time' address ['01']
#         is mapped to index[0]  in 'adjusted reading time' adjusted = WSW 010 


# [49]: for i in transcript:
#     ...: for k, v in d.items():
#     ...: if i == k:
#     ...: print(i, v)
