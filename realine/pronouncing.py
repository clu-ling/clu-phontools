from typing import Dict, Tuple, List, Optional
import os

Pronunciation = Tuple[str, ...]
Word = str


# FIXME: add APRAbetToIPA mappings

arpabet_to_ipa: Dict[str, str] =  {
  'AA': 'ɒ', 'AE': 'æ', 'AH': 'ʌ', 'AO': 'ɔ', 'AW': 'aʊ', 'AY': 'ai',
  'B': 'b',
  'CH': 'tʃ',
  'D': 'd',
  'DH': 'ð',
  'EH': 'ɛ', 'ER': 'ə', 'EY': 'ei',
  'F': 'f',
  'G': 'g',
  'HH': 'h',
  'IH': 'i', 'IY': 'I',
  'JH': 'dʒ', 
  'K': 'k',
  'L': 'l',
  'M': 'm',
  'N': 'n',
  'NG': 'ŋ',
  'OW': 'oʊ', 'OY': 'ɔi',
  'P': 'p',
  'R': 'ɹ',
  'S': 's',
  'SH': 'ʃ',
  'T': 't',
  'TH': 'θ', 'UH': 'ʊ', 'UW': 'U',
  'V': 'v',
  'W': 'w',
  'Y': 'j',
  'Z': 'z',
  'ZH': 'ʒ'
}

ipa_to_arpabet = { v:k for k,v in arpabet_to_ipa.items() }

 # ɖ, ɱ, ʔ, ɟ, ɲ, ɳ, ŋ, ʙ, ʀ, ɾ, ɽ, ɸ, β, ʂ , ʐ, ç, ʝ, ɰ, ɻ, ʋ, ɮ, is not present
arpabet_to_realine: Dict[str, str] = {
 'AA': 'ɒ','AA1': 'ɒ1', 'AA1': 'ɒ2', 'AA1': 'ɒ3',
 'AE': 'æ', 'AE1': 'æ1', 'AE2': 'æ2', 'AE3': 'æ3',
 'AH': 'ʌ', 'AH1': 'ʌ1', 'AH2': 'ʌ2','AH3': 'ʌ3',
 'AO': 'ɔ', 'AO1': 'ɔ1', 'AO2': 'ɔ2', 'AO3': 'ɔ3',
 'AW': 'aʊ', 
 'AY': 'ai', 
 'B': 'b', 
 'CH': 'tʃ', 
 'D': 'd',  
 'DH': 'ð',
 'EH': 'ɛ','EH1': 'ɛ1','EH2': 'ɛ2','EH3': 'ɛ3',
 'ER': 'ə',  'ER1': 'ə1',  'ER2': 'ə2',  'ER3': 'ə3',
 'EY': 'ei', 
 'F': 'f',
 'G': 'g',
 'HH': 'h',
 'IH': 'i',  'IH1': 'i1',  'IH2': 'i2',  'IH3': 'i3',
 'IY': 'I',  'IY1': 'I1',  'IY2': 'I2',  'IY3': 'I3',
 'JH': 'dʒ',
 'K': 'k',
 'L': 'l',
 'M': 'm',
 'N': 'n',
 'NG': 'ŋ',
 'OW': 'oʊ',
 'OY': 'ɔi',
 'P': 'p',
 'R': 'ɹ',
 'S': 's',
 'SH': 'ʃ',
 'T': 't',
 'TH': 'θ',
 'UH': 'ʊ',
 'UW': 'U',
 'V': 'v',
 'W': 'w',
 'Y': 'j',  'Y1': 'j1',  'Y2': 'j2', 'Y3': 'j3',
 'Z': 'z',
 'ZH': 'ʒ'

}
class PronouncingDict(dict):
  """
  Maps tuples of pronunciations -> lexical entries
  """
  def __init__(self, pairs: List[Tuple[Pronunciation, Word]] = []):
    self._dict = dict(pairs)

  def keys(self):
    return self._dict.keys()

  def values(self):
    return self._dict.values()

  def items(self):
    return self._dict.items()

  def __iter__(self):
    return iter(self._dict)
  
  def __len__(self):
    return len(self._dict)

  def add(self, key: Pronunciation, value: Word) -> None:
    self._dict[key] = value

  def __getitem__(self, key: Pronunciation) -> Word:
      return self._dict.__getitem__(key)

  def __setitem__(self, key: Pronunciation, value: Word) -> None:
    self._dict.__setitem__(self, key, value)
  
  @staticmethod
  def from_cmu_dict(filepath: Optional[str] = None, converter: Dict[str, str] = arpabet_to_ipa) -> "PronouncingDict":
    cmudict_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "cmudict")
    filepath = filepath or cmudict_file
    pairs = []
    with open(filepath, "r", encoding = "ISO-8859-1") as infile:
      for row in infile:
        # ignore comments
        if not row.startswith(";;"):
          res = row.strip().split("  ")
          value = res[0]
          # ARPAbet pronunciation.
          # optionally convert to provided format
          key = tuple(converter.get(phon, phon) for phon in res[-1].split(" "))
          pairs.append((key, value))
    return PronouncingDict(pairs)

p  = PronouncingDict()
pp = p.from_cmu_dict() 
print(pp.items())