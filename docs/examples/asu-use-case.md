# Introduction

Let's take a look at how to use `ReAline` to *align phonological sequences* and then *analyze errors* in the style of [Jiao et al. (2019)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6808349/pdf/JSLHR-62-3359.pdf#page=4)

For this example, we'll need the following imports:

```python
from clu.phontools.lang.en import EnglishUtils
from clu.phontools.struct import *
from clu.phontools.pronouncing import ConverterUtils
from clu.phontools.alignment.realine import *
from clu.phontools.alignment.lbe import *
```

We'll be aligning a **target** phrase with a **transcript** phrase.

In our example, our **target** phrase will be ...

>balance clamp and bottle

... and our **transcribed** phrase will be ...

>bell is glad a bottle

# Phrases and syllables

`clu-phontools` makes it easy to find all possible attested pronunciations for a phrase via a pronouncing dictionary.  In the case of English, we can use the **CMU pronouncing dictionary**:

```python
# prompt/target is "balance clamp and bottle"
# get all pronunciations for the phrase
# return a sequence of `clu.phontools.struct.Phrase`
target_phrases = EnglishUtils.all_possible_phrases_for(["balance", "clamp", "and", "bottle"])
```

How many pronunciations did we find?  In this case, there should be 2:

```python
assert len(target_phrases) == 2
```

Let's examine the *stress patterns*. Perhaps we only care about the distinction between **strong** (S) and **weak** (W) syllables:

```python
# let's examine the stress patterns...
for phrase in target_phrases:
  print(phrase.coarse_stress)
```

Perhaps we have a particular stress pattern we're interested in examining.  For this example, we'll pretend we're interested in finding phrases with the stres pattern **SW S W SW**:

```python
# our stress pattern of interest
pattern = "SW S W SW"

# find the first Phrase that matches our pattern.
# we'll use the first entry (stress pattern = ["SW", "S", "W", "SW"])
# as our target.
match_stress = lambda phrase: phrase.match_coarse_stress_pattern(pattern)
target: Phrase = next(filter(match_stress, target_phrases))
```

We'll apply the same steps to find transcript phrases:

```python
# transcript says "bell is glad a bottle"
# get all pronunciations for the phrase
transcript_phrases = EnglishUtils.all_possible_phrases_for(
  ["bell", "is", "glad", "a", "bottle"]
)

# in this case, there should be 4:
assert len(transcript_phrases) == 4
```

Before we searched for a particular syllable-stress pattern.  Let's ignore stress for a moment and simply look for a pattern of syllables.  Imagine we're interested in phrases composed of 4 monosyllabic words followed by a disyllabic word.  We can represent this pattern using **X X X X XX** where **X** denotes a syllable and whitespace represents a lexical boundary:

```python
# all of these phrases have 6 syllables with the structure "X X X X XX".
# If you're unfamiliar with regular expressions, keep in mind that ...
#   ^ in the pattern below means "starts with"
#   $ in the pattern below denotes the "end of sequence"
all(phrase.match_masked_syllables(pattern="^X X X X XX$", mask="X") for phrase in transcript_phrases)

# for our comparisons, let's use the first one:
transcript: Phrase = transcript_phrases[0]
```

# Alignment

Now that we have both a **target** and **transcript**, let's use **ReAline** to align the two phonological sequences:


```python
# let's calculate lexical boundary errors for the first one:
aligner = ReAline()
```

By default, ReAline expects to align IPA, so we'll first want to convert our ARPABet-based representations to IPA:

```python
target_phones = [ConverterUtils.arpabet_to_ipa(phone) for phone in target.phones]
transcript_phones = [ConverterUtils.arpabet_to_ipa(phone) for phone in transcript.phones]
alignment = aligner.align(target_phones, transcript_phones)
```

`alignment` should have the following value in this case (NOTE: newlines added for better legibility):

```python
[
  ('b', 'b'), ('æ', 'ɛ'), ('l', 'l'), ('ʌ', 'i'), ('n', '-'), ('s', 'z'),
  ('k', 'g'), ('l', 'l'), ('æ', 'æ'), ('m', '-'), ('p', '-'),
  ('ʌ', '-'), ('n', '-'), ('d', 'd'),
  ('-', 'ʌ'), ('b', 'b'), ('ɒ', 'ɒ'), ('t', 't'), ('ʌ', 'ʌ'), ('l', 'l')
]
```

# Error analysis

Now that we have an automatically aligned sequence, let's analyze the phonological and lexical boundary errors in our **transcript**.

## Phoneme errors

First, let's calculate phoneme errors:

```python
#
phoneme_errors = aligner.phoneme_errors(alignment)
```

## Lexical boundary errors

Next, let's calculate lexical boundary errors (LBEs):

```python
target_stress = target.coarse_stress
# should produce ['SW', 'S', 'W', 'SW']

transcript_masked_stress = transcript.mask_syllables(mask="X")
# should produce ['X', 'X', 'X', 'X', 'XX']

lbe_errors = calculate_lbes_from_stress(target_stress, transcript_masked_stress)
# should produce [LexicalBoundaryError(error_type=LexicalBoundaryErrorType.INSERTION_WEAK, target_index=0, transcript_index=0)]
```

# Wrapping up

A script containing this same example can be found at [`examples/asu-use-case.py`](https://github.com/clu-ling/clu-phontools/blob/main/examples/asu-use-case.py)
