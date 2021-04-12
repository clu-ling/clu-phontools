from typing import List
import pronouncing
import itertools
import numpy as np
import re

def possible_pronunciations(phrase: List[str]) -> List[List[str]]:
    # step 1: for each token in phrase, look up token in CMU dict and store
    data = np.array(phrase)
    phrase_phone = []
    for i in data:
        words = re.split(r'\s+', i)
        phrase_phone.append(words)

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
    for xx in each_flattened:
        for L in range(0, len(xx) + 1):
            
            for subset in itertools.combinations(data, L):
                a.append(list(subset))
            list_of_combinations.append(a)
    len(list_of_combinations)
    list_of_combinations = [i for i in list_of_combinations if i != [[]]]
    # data = [i for element in data for i in element]
    # list_of_combinations= []
    # for L in range(0, len(data)+1):
    #     for subset in itertools.combinations(data, L):
    #         list_of_combinations.append(list(subset))
    # list_of_combinations = [i for i in list_of_combinations if i != []]
    # stresses = []
    # for i in list_of_combinations:
    #     ss = [pronouncing.stresses(ii) for ii in i]
    #     stresses.append(ss)
    # stress_pattern = ['010101', '101010']
    # f = [i for i in stresses if len(i) > 1]
    # f = [''.join(i) for i in f]
    # f = [i for i in f if i in stress_pattern]
    
    return list_of_combinations


x = ['address her meeting time', 'admit the gear beyond']
s = possible_pronunciations(x)
print(s)

