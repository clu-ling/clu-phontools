from typing import Text, Dict, List, Callable, Tuple
import os

ConverterFunc = Callable[[Text], Text]
identity: Callable[[Text], Text] = lambda x: x


class IPAUtils:
    buckwalter_to_ipa_dict: Dict[Text, Text] = {
        # consonants 27
        "b": "b",  # ب
        "t": "t",  # ت
        "v": "θ",  # ث
        "j": "ʒ",  # ج
        "H": "ħ",  # ح
        "x": "x",  # خ
        "d": "d",  # د
        "V": "ð",  # ذ
        "r": "r",  # ر
        "z": "z",  # ز
        "s": "s",  # س
        "$": "ʃ",  # ش
        "S": "sˤ",  # ص
        "D": "dˤ",  # ض
        "T": "tˤ",  # ط
        "Z": "ðˤ",  # ظ
        "E": "ʕ",  # ع
        "g": "ɣ",  # غ
        "f": "f",  # ف
        "q": "q",  # ق
        "k": "k",  # ك
        "l": "l",  # ل
        "m": "m",  # م
        "n": "n",  # ن
        "h": "h",  # ه
        "w": "w",  # و
        "y": "j",  # ي
        # other 8
        "a": "a",
        "i": "i",
        "u": "u",
        "A": "aː",
        "I": "iː",
        "U": "uː",
        "G": "ʔ",
        "p": "h",
    }

    buckwalter_to_arabic_dict: Dict[Text, Text] = {
        # consonants 27
        "b": "ب",  # ب
        "t": "ت",  # ت
        "v": "ث",  # ث
        "j": "ج",  # ج
        "H": "ح",  # ح
        "x": "خ",  # خ
        "d": "د",  # د
        "V": "ذ",  # ذ
        "r": "ر",  # ر
        "z": "ز",  # ز
        "s": "س",  # س
        "$": "ش",  # ش
        "S": "ص",  # ص
        "D": "ض",  # ض
        "T": "ط",  # ط
        "Z": "ظ",  # ظ
        "E": "ع",  # ع
        "g": "غ",  # غ
        "f": "ف",  # ف
        "q": "ق",  # ق
        "k": "ك",  # ك
        "l": "ل",  # ل
        "m": "م",  # م
        "n": "ن",  # ن
        "h": "ه",  # ه
        "w": "و",  # و
        "y": "ي",  # ي
        # other 8
        "a": "َ",
        "i": "ِ",
        "u": "ُ",
        "A": "ا",
        "I": "ي",
        "U": "و",
        "G": "ء",
        "p": "ة",
    }

    buckwalter_to_arabic_dict_orginal: Dict[Text, Text] = {
        # consonants 27
        "b": "ب",  # ب
        "t": "ت",  # ت
        "v": "ث",  # ث
        "j": "ج",  # ج
        "H": "ح",  # ح
        "x": "خ",  # خ
        "d": "د",  # د
        "V": "ذ",  # ذ
        "r": "ر",  # ر
        "z": "ز",  # ز
        "s": "س",  # س
        "$": "ش",  # ش
        "S": "ص",  # ص
        "D": "ض",  # ض
        "T": "ط",  # ط
        "Z": "ظ",  # ظ
        "E": "ع",  # ع
        "g": "غ",  # غ
        "f": "ف",  # ف
        "q": "ق",  # ق
        "k": "ك",  # ك
        "l": "ل",  # ل
        "m": "م",  # م
        "n": "ن",  # ن
        "h": "ه",  # ه
        "w": "و",  # و
        "y": "ي",  # ي
        # other 8
        "a": "َ",
        "i": "ِ",
        "u": "ُ",
        "A": "ا",
        "I": "ي",
        "U": "و",
        "G": "ء",
        "p": "ة",
    }

    def buckwalter_to_ipa(symbol: Text) -> Text:
        """Converts  dataset symbols to IPA"""
        return IPAUtils.buckwalter_to_ipa_dict.get(symbol, symbol)

    def ipa_to_buckwalter(symbol: Text) -> Text:
        """IPA to dataset symbols"""
        for arabic, phoneme in IPAUtils.buckwalter_to_ipa_dict.items():
            if phoneme == symbol:
                return arabic
        return symbol

    def buckwalter_to_arabic(symbol: Text) -> Text:
        """Converts  dataset symbols to IPA"""
        return IPAUtils.buckwalter_to_arabic_dict.get(symbol, symbol)

    def arabic_to_buckwalter(symbol: Text) -> Text:
        """IPA to dataset symbols"""
        for arabic, phoneme in IPAUtils.buckwalter_to_arabic_dict.items():
            if phoneme == symbol:
                return arabic
        return symbol


class Converter:
    def __init__(self) -> None:
        pass

    def read_file(self) -> List[Tuple[Text]]:
        arabic_file = os.path.join("resources", "arabic")
        pairs = []
        with open(arabic_file, "r", encoding="ISO-8859-1") as infile:
            for row in infile:
                if not row.startswith("#"):
                    res = row.strip().split(" ")
                    res = [res[0], " ".join(res[1:])]
                    key = res[0]
                    value = tuple("".join(res[1:]).split(" "))
                    value = "".join(value)
                    pairs.append((key, value))
        return pairs

    @staticmethod
    def convert_buckwalter_to_ipa(text: Text) -> Text:
        text = list(text)
        res = list(IPAUtils.buckwalter_to_ipa(symb) for symb in text)
        return "".join(res)

    @staticmethod
    def convert_buckwalter_to_arabic(text: Text) -> Text:
        text = list(text)
        res = list(IPAUtils.buckwalter_to_arabic(symb) for symb in text)
        return "".join(res)

    @staticmethod
    def convert_arabic_to_buckwalter(text: Text) -> Text:
        text = list(text)
        res = list(IPAUtils.arabic_to_buckwalter(symb) for symb in text)
        return "".join(res)

    @staticmethod
    def nomalize_hamza(text):
        if text.startswith("ءُ"):
            return "أُ" + text[2:]
        elif text.startswith("ءَ"):
            return "أَ" + text[2:]
        elif text.startswith("ءِ"):
            return "إِ" + text[2:]
