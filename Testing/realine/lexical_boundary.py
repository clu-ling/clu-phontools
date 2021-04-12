# This code is an organization of ASU's code
import re
from typing import List

class Phrase(object):

    def cmu_pronunciations(self, phrase: List[str]) -> List[List[str]]:
        data = [i.lower().split() for i in phrase]
        return data


if __name__ == "__main__":
    x = ['address her meeting time', 'admit the gear beyond']
    p = Phrase()
    print(p.cmu_pronunciations(x))
