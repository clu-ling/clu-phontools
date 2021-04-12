import re
from scipy.io import loadmat, savemat
from autocorrect import Speller
import pronouncing
import numpy as np
from typing import List
import itertools

spell = Speller(lang='en')


def possible_pronunciations(phrase: List[str]) -> List[List[str]]:
    data = np.array([phrase]).flatten()
    phrase_phone = []
    for i in data:
        words = re.split(r'\s+', i)
        phrase_phone.append(words)
    #return phrase_phone
    cmu = []
    for ii in phrase_phone:
        each = []
        for i in ii:
            each.append(pronouncing.phones_for_word(i))
        cmu.append(each)
    
    each_flattened = []
    for x in cmu:
        data = [i for element in x for i in element]
        each_flattened.append(data)

    list_of_combinations = []
    for x in each_flattened:
        c = []
        for L in range(0, len(x) + 1):
            for subset in itertools.combinations(x, L):
                c.append(list(subset))
        print(len(c))
        list_of_combinations.append(c)

    he = []
    for i in list_of_combinations:
        for ii in i:
            if ii != []:
                c = ii
                he.append(c)

    stresses = []
    for i in he:
        f = []
        for ii in i:
            s = pronouncing.stresses(ii)
            f.append(s)
        stresses.append(f)

    stress_pattern = ['010101', '101010']
    f = [i for i in stresses if len(i) > 1]
    f = [''.join(i) for i in f]
    f = [i for i in f if i in stress_pattern]

    print(f)

   
    




    

def generate_stress_assignment(pronounciation: List[str], stress_constrains) -> List[List[str]]:
    stress_constrains = ['101010', '010101']
    pass
    

   





if __name__ == "__main__":
    phrases = ['address her meeting time', 'admit the gear beyond']
    p = possible_pronunciations(phrases)
    



