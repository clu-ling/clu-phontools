from typing import Text, Dict, List, Callable, Optional
import os

ConverterFunc = Callable[[Text], Text]
identity: Callable[[Text], Text] = lambda x: x

class BuckwalterUtils:
    """
    `BuckwalterUtils` maps from Arabic Orthography to Buckwalter symbols and vice-versa
    """
    arabic_to_buckwalter_dict: Dict[Text, Text] = {
        u"ا": "A", # alif
		u"ب": "b", # ba
		u"ت": "t", # ta
		u"ث": "^", # tha
		u"ج": "j", # jim 
		u"ح": "H", # Ḥa
		u"خ": "x", # kha
		u"د": "d", # dal
		u"ذ": "*", # dhal
		u"ر": "r", # ra
		u"ز": "z", # zin
		u"س": "s", # sin
		u"ش": "$", # shin
		u"ص": "S", # ṣad
		u"ض": "D", # Ḍad
		u"ط": "T", # Ṭa
		u"ظ": "Z", # Ẓa
		u"ع": "E", # 'Ayn
		u"غ": "g", # ghayn
		u"ف": "f", # fa
		u"ق": "q", # qaf
		u"ك": "k", # kaf
		u"ل": "l", # lam
		u"م": "m", # mim
		u"ن": "n", # nun
		u"ه": "h", # ha
		u"و": "w", # waw
		u"ي": "y", # ya
		#hamza
		u"ء": "'", # lone hamza
		u"أ": ">", # hamza on alif
		u"إ": "<", # hamza below alif
		u"ؤ": "&", # hamza on waw
		u"ئ": "}", # hamza on ya
		#alif
		u"آ": "|", # madda on alif
		u"ٱ": "{", # alif alwasla
		u"\u0670": "`", # dagger alif
		u"ى": "Y", # alif maqsura
		#harakat
		u"\u064E": "a", # fatha
		u"\u064F": "u", # Damma
		u"\u0650": "i", # kasra
		u"\u064B": "F", # fathatayn
		u"\u064C": "N", # dammatayn
		u"\u064D": "K", # kasratayn
		u"\u0651": "~", # shadda
		u"\u0640": "_", # tatwil
		#others
		u"ة": "p", # ta marbuta
		u"\u0652": "o", # sukun
        " ": " ",
    }

    def arabic_to_buckwalter(symbol: Text) -> Text:
        """Converts  arabic text to buckwalter
        Example:
        arabic_word = ['ل', 'ع', 'ب']
        converted_buck = list(ConverterUtils.arabic_to_buckwalter(symb) for symb in arabic_word)
        print(converted_buck)
        # ['l', 'E', 'b']
        """
        return BuckwalterUtils.arabic_to_buckwalter_dict.get(symbol, symbol)

    def buckwalter_to_arabic(symbol: Text) -> Text:
        """Converts arabic text to to buckwalter
        Example:
        buck_word = ['l','E','b']
        converted = list(ConverterUtils.arabic_to_buckwalter(symb) for symb in buck_word)
        print(converted)
        # ['ل', 'ع', 'ب']
        """
        for (arabic, buckwalter) in BuckwalterUtils.arabic_to_buckwalter_dict.items():
            if buckwalter == symbol:
                return arabic
        return symbol





class IPAUtils:

    """Converter utilities to map between phonological symbol sets"""

    phoneme_to_ipa_dict: Dict[Text, Text] = {
        # consonants 
        "b": "b", 
        "t": "t", 
        "^": "θ",
        "J": "ʒ", 
        "H": "ħ",
        "x": "x", 
        "d": "d", 
        "*": "ð",
        "r": "r", 
        "z": "z", 
        "s": "s", 
        "$": "ʃ", 
        "S": "sˤ", 
        "D": "dˤ", 
        "T": "tˤ",
        "Z": "ðˤ",
        "E": "ʕ",
        "g": "ɣ",
        "f": "f", 
        "q": "q", 
        "k": "k", 
        "l": "l",
        "m": "m",
        "n": "n",
        "h": "h",
        "w": "w",
        "y": "j",
        # OTHER
        # ">":"",
        # "<":"",
        # "&":"",
        # "}":"",
        # geminates
        "<<": u"ʔʔ", 
        "bb": u"bb",
        "tt": u"tt", 
        "^^": u"θθ", 
        #"J": u"ج", # does not exist
        "HH": u"ħħ", 
        "xx": u"xx", 
        "dd": u"dd", 
        "**": u"ðð", 
        "rr": u"rr", 
        "zz": u"zz", 
        "ss": u"ss", 
        "$$": u"ʃʃ",
        "SS": u"sˤsˤ", 
        "DD": u"dˤdˤ", 
        "TT": u"tˤtˤ", 
        "ZZ": u"ðˤðˤ", 
        "EE": u"ʕʕ", 
        "gg": u"ɣɣ", 
        "ff": u"ff", 
        "qq": u"qq", 
        "kk": u"kk", 
        "ll": u"ll", 
        "mm": u"mm", 
        "nn": u"nn",
        "hh": u"hh",
        "ww": u"ww", 
        "yy": u"jj", 
        # foreign
        "p": u"p",  # پ"
        "pp": u"pp",
        "v": u"v", # ڤ"
        "G": u"dʒ", # ج"
        # long vowels ا
        "aa": u"aː", 
        "aa'": u"aː",     #replace("aa'", "aa")
        "AA": u"ɑː", 
        "AA'": u"ɑː",     #replace("AA'", "AA")
        # long vowels و
        "uu0": u"uː", 
        "uu0'": u"uː", 
        "UU0": u"uː", 
        "UU0'": u"uː",  
        "UU1": u"oː",
        "UU1'": u"oː",
        # long vowel ي
        "ii0": u"iː", 
        "ii0'": u"iː", 
        "II0": u"iː",
        "II0'": u"iː", 
        "ii1": u"ɪː",
        "ii1'": u"ɪː",
        # short vowel fatha
        "a": u"a", 
        "a'": u"a", 
        "A": u"ɑ", 
        "A'": u"ɑ",
        # short vowel damma
        "u": u"u", 
        "u0": u"u", 
        "u0'": u"u", 
        "U0": u"u", 
        "U0'": u"u", 
        "u1": u"o", 
        "u1'": u"o", 
        "U1": u"o",
        "uu1": u"oː",
        "uu1'": u"oː",
        # short vowel kasra
        "i": u"i", 
        "i0": u"i",
        "i0'": u"i", 
        "I0": u"i",
        "I0'": u"i",
        "i1": u"ɪ",
        "i1'": u"ɪ",
        "I1": u"ɪ",
        "I1'": u"ɪ",
        # more
        "sil": u"sil",
        "dist": u"dist",
        "-": u"-",
        "j": u"ʒ",
        "jj": u"ʒʒ",
        "Ah": u"ʔ",
        "AH": u"ʔ",
        "SH": u"ʃ",
        "TH": u"ð",
        #"@":" ",
    }

    def buckwalter_to_ipa(symbol: Text) -> Text:
        """Converts  dataset symbols to IPA
        """
        return IPAUtils.phoneme_to_ipa_dict.get(symbol, symbol)
    
    def ipa_to_buckwalter(symbol: Text) -> Text:
        """IPA to dataset symbols
        
        """
        for (arabic, phoneme) in IPAUtils.phoneme_to_ipa_dict.items():
            if phoneme == symbol:
                return arabic
        return symbol


class BuckwalterConverter:
    """
    This class uses `BuckwalterUtils` to do the mappings. 

    """
    @staticmethod
    def convert_buckwalter_to_arabic(text: Text) -> Text:
        text = list(text)
        res = list(BuckwalterUtils.buckwalter_to_arabic(symb) for symb in text)
        return "".join(res)

    @staticmethod
    def convert_arabic_to_buckwalter(text: Text) -> Text:
        text = list(text)
        res = list(BuckwalterUtils.arabic_to_buckwalter(symb) for symb in text)
        return "".join(res)



class IPAConverter:
    """
    This class uses `IPAUtils` to do the mappings. 

    This should take buckwater and convert it to IPA

    """
    @staticmethod
    def fix_long_vowel_yaa(symbols: List[Text]) -> List[Text]:
        """
        - This function fixes the long vowel `yaa` or `ي`.
        - `ي` serves as a consonant and a vowel.
            - When it is a consonant, it should be diacritized with a short vowel (a, i, u)
            - If not, then it is a long vowel /iː/
        """
        i = 0
        new_list = []
    
        while i < len(symbols):
            if (i < len(symbols) - 1 and symbols[i] == 'i' and symbols[i + 1] == 'j'):
                if i < len(symbols) - 2 and symbols[i + 2] in ['a', 'i', 'u']:
                    new_list.append(symbols[i])
                else:
                    new_list.append('iː')
                    i += 1  
            else:
                new_list.append(symbols[i])
            i += 1
        return new_list
    
    @staticmethod
    def fix_long_vowel_waw(symbols: List[Text]) -> List[Text]:
        pass
    
    @staticmethod
    def fix_a_after_emphatics(symbols: List[Text]) -> List[Text]:
        pass

    @staticmethod
    def fix_shada(symbols: List[Text], item: Text) -> List[Text]:
        if item in symbols:
            index = symbols.index(item)
            if index > 0:
                symbols[index] = symbols[index-1]
        return symbols
    
    @staticmethod
    def fix_sukuun(symbols: List[Text]) -> List[Text]:
        return [item for item in symbols if item != 'o']
    
    @staticmethod
    def fix_definite_article(symbols: List[Text]) -> List[Text]:
        # if "".join(symbols).startswith("ɑl"):
        #     x5 = '?' + "".join(symbols)
        #     print(x5)
        pass

    @staticmethod
    def fix(res: List[Text]) -> List[Text]:
        for i in range(len(res)):
            # replace أ with ʔ
            if res[i] == '>':
                res[i] = 'ʔ'
            # replace إ with ʔ
            elif res[i] == '<':
                res[i] = 'ʔ'
            # replace ؤ with ʔ
            elif res[i] == '&':
                res[i] = 'ʔ'
            # replace ئ with ʔ
            elif res[i] == '}':
                res[i] = 'ʔ'
            return res

    @staticmethod
    def convert_to_ipa(text: Text) -> List[Text]:
        # 1) get IPA symbols
        res = list(IPAUtils.buckwalter_to_ipa(symb) for symb in text)
        # 2) change some symbols
        res = IPAConverter.fix(res)
        # 3) fix shadda
        res = IPAConverter.fix_shada(res, "~")
        # 4) remove sukuun
        res = IPAConverter.fix_sukuun(res)
        # 5) fix ij
        res = IPAConverter.fix_long_vowel_yaa(res)
        # 6) fix uj
        
        # 7) fix definite article
        return res
    

if __name__ == '__main__':
    # Some tests later
    arabic = "أَحْمَد سَيّد"
    # First: get Buckwalter
    buck = BuckwalterConverter.convert_arabic_to_buckwalter(arabic)
    print("BUCKWALTER: ", buck)
    # second: get ipa
    ipa = IPAConverter.convert_to_ipa(buck)
    print("IPA: ", ipa)
    

