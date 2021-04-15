import unittest
from lb import *


class LexicalBoundaryTests(unittest.TestCase):

    def test_possible_pronunciations(self):
        x = ['address her meeting time', 'admit the gear beyond']
        self.assertEqual([possible_pronunciations(i) for i in x],
                         [['AE1 D R EH2 S', 'AH0 D R EH1 S'], ['HH ER1', 'HH ER0'], ['M IY1 T IH0 NG'], ['T AY1 M']], [['AH0 D M IH1 T'], ['DH AH0', 'DH AH1', 'DH IY0'], ['G IH1 R'], ['B IH0 AA1 N D', 'B IY2 AO1 N D', 'B IH0 AO1 N D']])


    def test_stress_assignments(self):
        stress_pattern = ['010101', '101010']
        pass

    def arpabet_to_ipa(self):
        pass

    def phrase_to_ipa(self):
        pass


if __name__ == "__main__":
    data = ['address her meeting time', 'admit the gear beyond']
    l = LexicalBoundaryTests()
    l.test_possible_pronunciations()

