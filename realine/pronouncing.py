from typing import Dict, Tuple, List, Optional
import os

Pronunciation = Tuple[str, ...]
Word = str


# FIXME: add APRAbetToIPA mappings
arpabet_to_ipa: Dict[str, str] = {

}

ipa_to_arpabet = {v:k for k,v in arpabet_to_ipa.items()}


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