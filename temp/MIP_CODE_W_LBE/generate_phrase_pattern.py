import re
from scipy.io import loadmat, savemat
from autocorrect import Speller
import pronouncing

spell = Speller(lang='en')

class phrase(object):

    def __init__(self):
        self.phrase_test = loadmat('Phrase.mat')['Phrase']
        self.phrase_test = self.phrase_test.flatten()
        self.phrase_phn = []
        self.phrase_stress = []
        self.phrase_phn_modify = []
        alt_words = ['address','his','justice','is','its','them','it','can']
        alt_stress_1 = ['for','could','but','her','to','then','from','such','had','or','we']
        alt_stress_2 = ['instead','indeed','almost','increase','inside','playground']
        stress_pattern = ['010101','101010']
        for item in self.phrase_test:
            item = str(item[0])
            words = re.split(r'\s+', item)

            phn = []
            phn_modify = []
            stress = []
            for word in words:
                
                #word = spell(word).lower()
                word = word.lower()
                pron = pronouncing.phones_for_word((word))
                #if len(pron)>1:
                    #print(word)
                    #print(pron)
                if len(pron) == 1:
                    cur_phn = pron[0]
                elif word in alt_words:
                    cur_phn = pron[1]
                elif word=='with':
                    cur_phn = pron[2]
                else:
                    cur_phn = pron[0]

                phn.append(cur_phn)
                if word in alt_stress_1:
                    cur_phn=cur_phn.replace("1","0")
                elif word in alt_stress_2:
                    cur_phn = cur_phn.replace("2", "0")

                if word == 'in' and item == 'butcher in the middle':
                    cur_phn = cur_phn.replace("0","1")
                if word == 'for' and item == 'thinking for the hearing':
                    cur_phn = cur_phn.replace("0","1")
                if word == 'on' and item == 'children on the playground':
                    cur_phn = cur_phn.replace("0","1")
                if word == 'of':
                    cur_phn = cur_phn.replace("1","0")
                phn_modify.append(cur_phn)
                stress.append(str(pronouncing.stresses(cur_phn)))

            linked_stress = ''.join(stress)
            if linked_stress not in stress_pattern:
                print(item)
                print(phn_modify)

            self.phrase_phn.append(phn)
            self.phrase_stress.append(stress)
            self.phrase_phn_modify.append(phn_modify)

    def arpabet_to_ipa(self):
        f = open('ARPABET_TO_IPA.txt', 'r', encoding='UTF-8')
        dict = {}
        for line in f:
            if '\t' not in line:
                continue
            else:
                arpabet, ipa = re.split(r'\t+', line.strip())
                dict[arpabet.strip()] = ipa.strip()
        f.close()
        return dict

    def string_to_arpabet(self, phrase_str):

        alt_words = ['address', 'his', 'justice', 'is', 'its', 'them', 'it', 'can']

        words = re.split(r'\s+', phrase_str)
        phn = []
        stress = []
        for word in words:
            if '\'' not in word:
                word = spell(word).lower()
            pron = pronouncing.phones_for_word((word))
            if pron == []:
                cur_phn = '-'
            else:
                if len(pron) == 1:
                    cur_phn = pron[0]
                elif word in alt_words:
                    cur_phn = pron[1]
                elif word == 'with':
                    cur_phn = pron[2]
                else:
                    cur_phn = pron[0]
            phn.append(cur_phn)
            stress.append(str(pronouncing.stresses(cur_phn)))

        return phn, stress


