import unittest
#from tt import Phrase
import numpy as np
from try_another import Phrase
import re

p = Phrase()


class TestPhrase(unittest.TestCase):

    def test_cmu_pronunciation(self):
        '''
        This function tests converting a list of strings into a list of lists of cmu transcriptions.
        '''
        phrases = np.array([['address her meeting time'], ['admit the gear beyond']]).flatten()

        self.assertEqual(p.pronounciation_and_stress(phrases), 
                          [['AH0 D R EH1 S', 'HH ER1', 'M IY1 T IH0 NG', 'T AY1 M'],
                                                                     ['AH0 D M IH1 T', 'DH AH0', 'G IH1 R', 'B IH0 AA1 N D']])

    def test_cmu_stress(self):
        '''
        This function tests stress assignment from the cmu dictionary. It takes the cmu transcriptions and outputs
        the stress pattern for each phrase.
        '''
        phrases = np.array([['address her meeting time'], [
                           'admit the gear beyond']]).flatten()

        self.assertEqual(p.pronounciation_and_stress(phrases),
                         [['01', '0', '10', '1'],
                          ['01', '0', '1', '01']])

    def test_arpabet_to_ipa(self):
        #ipa_phrase = 'kæt
        phrases = [['AH0 D R EH1 S', 'HH ER1', 'M IY1 T IH0 NG', 'T AY1 M'],
                        ['AH0 D M IH1 T', 'DH AH0', 'G IH1 R', 'B IH0 AA1 N D']]
        pattern_phone_ipa = []
        for phrase in phrases:
            for item in phrase:
                item = re.sub('[0-9]+', '', item)
                temp = re.split(r'\s+', item)
                print(temp)
                for phn in temp:
                    pattern_phone_ipa.append(p.arpabet_to_ipa[phn])
        print(pattern_phone_ipa)
        #self.assertEqual()
    

    def test_phrase_to_arpabet(self):
        phrase = 'address her meeting time'
        self.assertEqual(Phrase.string_to_arpabet(phrase), (['AH0 D R EH1 S', 'HH ER1', 'M IY1 T IH0 NG', 'T AY1 M'],
                                                            ['01', '1', '10', '1']))

    def test_calc_lbe(self):
        target = ['01', '0', '10', '1']
        transcript = ['1', '0', '0', '10', '1']
        res = calc_lbe(target, transcript)
        error_report = LexicalBoundaryErrorReport(
            target_stress = target,
            transcript_stress = transcript,
            lbes=[
                LexicalBoundaryError(
                    target_index=0,
                    transcript_indices=[0, 1],
                    error_type=LexicalBoundaryErrorType.IW
                )
            ]
        )
        self.assertEqual(res, error_report)

      
if __name__ == "__main__":
    f = TestPhrase()
    ff = f.test_arpabet_to_ipa()
    print(ff)
        

        






