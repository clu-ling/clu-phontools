#!/usr/bin/env python
import numpy as np
from typing import List, Tuple
from realine import ReAline

realine = ReAline()

class Metrics(object):
    '''
    Metrics take the output of ReAline and calculates edit distance, phoneme errors and phone similarity.

    Attributes:
    -----------
    alignments: [List[Tuple[str, str]]]

    Methods:
    -------
    '''
    def __init__(self, alignments) -> [List[Tuple[str, str]]]:
        self.alignments = alignments

    def similarity(self, t):
        a = t[0]
        b = t[1]
        return realine.delta(a, b)

    def phoneSimilarity(self):
        try:
            return [self.similarity(i) for i in self.alignments]
        except TypeError:
            pass
           
    def calcPhonemeErrors(self):
        main = 0
        insertions_count = 0
        insertions = []
        deletions_count = 0
        deletions = []
        substitutions_count = 0
        substitutions = []
        for item in self.alignments:
            self.phone_1 = item[0]
            self.phone_2 = item[1]
            if self.phone_1 == '-':
                i = self.phone_1, self.phone_2
                insertions.append(i)
                insertions_count += 1
                main += 1
            elif self.phone_2 == '-':
                d = self.phone_1, self.phone_2
                deletions.append(d)
                deletions_count += 1
                main += 1
            elif self.phone_1 != self.phone_2 and self.phone_1 != '-' and self.phone_2 != '-':
                s = self.phone_1, self.phone_2
                substitutions.append(s)
                substitutions_count += 1
                main += 1
        return "edit distance score:", main, "deletions:", deletions_count, deletions, "insertions:", insertions_count, insertions, "substitutions:", substitutions_count, substitutions

    # def calcLexicalBoundary(self):
    #     pass
    
