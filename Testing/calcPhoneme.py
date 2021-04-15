import numpy as np

alignments = [[('æ', 'æ'), ('d', 'd'), ('v', 'v'), ('æ', 'æ'), ('n', 'n'), ('s', 's'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('s', 's'), ('æ', 'ɛ'), ('t', 't'), ('ə', 'ə'), ('p', 'p'), ('i', 'i'), ('l', 'l')], [('æ', 'æ'), ('d', 'd'), ('v', 'v'), ('æ', 'æ'), ('n', 'n'), ('s', 's'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('s', 's'), ('æ', 'æ'), ('t', 'd'), ('ə', 'ə'), ('p', 'p'), ('-', 'h'), ('i', 'ɪ'), ('l', 'l')], [('d', 'b'), ('v', '-'), ('æ', 'æ'), ('n', 'n'), ('-', 'd'), ('s', 'z'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('s', 's'), ('æ', 'æ'), ('t', 't'), ('ə', 'ə'), ('p', 'p'), ('-', 'h'), ('i', 'ɪ'), ('l', 'l')], [('æ', 'æ'), ('d', 'd'), ('v', 'v'), ('æ', 'æ'), ('n', 'n'), ('s', 's'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('s', 's'), ('æ', 'æ'), ('t', 'd'), ('ə', 'ɔ'), ('-', 'r'), ('p', 'p'), ('i', 'i'), ('l', 'l')], [('æ', 'ə'), ('d', 'd'), ('v', '-'), ('æ', 'æ'), ('n', 'n'), ('s', 's'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('s', 's'), ('æ', 'æ'), ('t', 'd'), ('ə', 'ə'), ('p', 'p'), ('i', 'i'), ('l', 'l')], [('æ', 'æ'), ('d', 'd'), ('v', 'v'), ('æ', 'ɑ'), ('n', '-'), ('-', 'ɪ'), ('s', 'z'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('s', 'ð'), ('æ', 'æ'), ('t', 't'), ('ə', 'ə'), ('p', 'p'), ('i', 'i'), ('l', 'l')], [('ə', 'ə'), ('m', 'm'), ('ɛ', 'æ'), ('n', 'n'), ('d', 'd'), ('ə', 'ə'), ('s', 's'), ('t', 't'), ('e', 'e'), ('t', 't'), ('ə', 'ə'), ('p', 'p'), ('r', 'r'), ('o', 'o'), ('tʃ', 'tʃ')], [('m', 'm'), ('ɛ', 'ɛ'), ('n', 'n'), ('d', 'd'), ('ə', 'ə'), ('s', 's'), ('t', '-'), ('e', 'i'), ('t', '-'), ('ə', 'ə'), ('p', 'p'), ('r', 'r'), ('o', 'o'), ('tʃ', 'tʃ')], [('ə', 'ə'), ('m', 'm'), ('ɛ', 'ɪ'), ('n', '-'), ('d', 'd'), ('ə', 'ə'), ('s', 's'), ('t', 't'), ('e', 'e'), ('t', 't'), ('ə', 'ə'), ('p', 'p'), ('r', 'r'), ('o', 'o'), ('tʃ', 'tʃ')], [('m', 'm'), ('ɛ', 'ɛ'), ('n', 'n'), ('d', 'd'), ('ə', 'ʌ'), ('s', 'z'), ('t', '-'), ('-', 'h'), ('e', 'i'), ('t', '-'), ('ə', 'ə'), ('p', 'p'), ('r', 'r'), ('o', 'o'), ('tʃ', 'tʃ')], [('ə', ['ɑ', 'ɪ']), ('m', 'm'), ('ɛ', 'ɛ'), ('n', 'n'), ('d', 't'), ('ə', 'ə'), ('s', 's'), ('t', 't'), ('e', 'e'), ('t', 't'), ('ə', 'ə'), ('p', 'p'), ('r', 'r'), ('o', 'o'), ('tʃ', 'tʃ')], [('v', 'b'), ('ɔ', 'ɔ'), ('ɪ', 'ɪ'), ('d', '-'), ('ɔ', 'ɔ'), ('r', 'r'), ('b', 'b'), ('i', 'i'), ('t', 'p'), ('k', 'k'), ('ə', 'ə'), ('m', 'm'), ('æ', 'æ'), ('n', 'n'), ('d', 'd')], [('ə', 'ə'), ('v', 'v'), ('ɔ', 'ɔ'), ('ɪ', 'ɪ'), ('d', 'd'), ('ɔ', 'ɑ'), ('r', 'r'), ('-', 'tʃ'), ('-', 's'), ('b', 'p'), ('i', 'i'), ('t', 'tʃ'), ('k', 'k'), ('ə', 'ə'), ('m', 'm'), ('æ', 'æ'), ('n', 'n'), ('d', 'd')], [('v', 'b'), ('ɔ', 'ɔ'), ('ɪ', 'ɪ'), ('d', 'b'), ('ɔ', 'ɜ'), ('r', 'r'), ('b', 'p'), ('i', 'i'), ('t', '-'), ('k', 'k'), ('ə', 'ə'), ('m', 'm'), ('æ', 'æ'), ('n', 'n'), ('d', 'd')], [('ə', 'ə'), ('v', 'v'), ('ɔ', 'ɔ'), ('ɪ', 'ɪ'), ('d', 'd'), ('ɔ', 'e'), ('r', 'r'), ('b', '-'), ('i', 'ɪ'), ('t', 'd'), ('k', 'k'), ('ə', 'ə'), ('m', 'm'), ('æ', 'æ'), ('n', 'n'), ('d', 'd')], [('ə', 'ɑ'), ('v', '-'), ('ɔ', 'ɪ'), ('-', 'w'), ('ɪ', 'e'), ('d', 't'), ('-', 'f'), ('ɔ', 'ɔ'), ('r', 'r'), ('b', 'ð'), ('i', 'ə'), ('t', '-'), ('k', 'k'), ('ə', 'ə'), ('m', 'm'), ('æ', 'æ'), ('n', 'n'), ('d', 'd')], [('ə', 'ə'), ('w', 'w'), ('ɑ', 'ɜ'), ('r', 'r'), ('d', 'd'), ('h', 'h'), ('ɪ', 'ɪ'), ('z', 'z'), ('d', 'd'), ('r', 'r'), ('e', 'e'), ('n', 'n'), ('-', 'd'), ('ə', 'ə'), ('w', 'w'), ('e', 'e')], [('ə', 'ə'), ('w', 'v'), ('ɑ', 'ɔ'), ('r', '-'), ('-', 'ɪ'), ('d', 'd'), ('h', 'h'), ('ɪ', 'ɪ'), ('z', 'z'), ('d', 'd'), ('r', 'r'), ('e', 'i'), ('n', 'm'), ('ə', 'ə'), ('w', 'w'), ('e', 'e')], [('ə', 'ə'), ('w', 'w'), ('ɑ', 'ɑ'), ('r', 'r'), ('d', 'd'), ('h', 'h'), ('ɪ', 'ɪ'), ('z', 'z'), ('d', 'g'), ('r', 'r'), ('e', 'i'), ('n', 'n'), ('ə', 'ə'), ('w', 'w'), ('e', 'e')], [('ə', 'ə'), ('-', 'p'), ('w', 'w'), ('ɑ', 'ɜ'), ('r', 'r'), ('d', 'd'), ('h', 'h'), ('ɪ', 'ɪ'), ('z', 'z'), ('d', 't'), ('r', 'r'), ('e', 'e'), ('n', 'n'), ('ə', 'ə'), ('w', 'w'), ('e', 'e')], [('b', 'b'), ('æ', 'æ'), ('l', 'l'), ('ə', 'ə'), ('n', 'n'), ('s', 's'), ('k', 'k'), ('l', 'l'), ('æ', ['ɑ', 'ɪ']), ('m', 'm'), ('p', '-'), ('æ', 'æ'), ('n', 'n'), ('d', 'd'), ('b', 'b'), ('ɑ', 'ɑ'), ('t', 't'), ('ə', 'ə'), ('l', 'l')], [('b', 'b'), ('æ', 'ɑ'), ('l', '-'), ('ə', 'ʊ'), ('n', 'n'), ('s', 's'), ('k', 'k'), ('l', 'l'), ('æ', 'æ'), ('m', '-'), ('p', 'p'), ('æ', 'æ'), ('n', 'n'), ('d', 'd'), ('b', 'b'), ('ɑ', 'ɑ'), ('t', 'b'), ('ə', 'ə'), ('l', 'l')], [('b', 'b'), ('æ', 'æ'), ('l', 'l'), ('ə', 'ə'), ('n', 'n'), ('s', 's'), ('k', 'k'), ('l', 'l'), ('æ', 'æ'), ('m', 'm'), ('p', 'p'), ('æ', 'ɛ'), ('n', 'm'), ('d', '-'), ('b', 'b'), ('ɑ', 'ɛ'), ('t', 'z'), ('ə', 'ə'), ('l', 'l')], [('b', 'b'), ('æ', 'æ'), ('l', 'l'), ('ə', 'ə'), ('n', 'n'), ('s', 's'), ('k', 'k'), ('l', 'l'), ('-', 'ɑ'), ('æ', ['ɪ', 'ə']), ('m', 'n'), ('p', 't'), ('æ', 'æ'), ('n', 'n'), ('d', 'd'), ('b', '-'), ('-', 'm'), ('ɑ', 'ɑ'), ('t', 't'), ('ə', 'ə'), ('l', 'l')], [('b', 'b'), ('æ', 'æ'), ('l', 'l'), ('ə', 'ə'), ('n', 'n'), ('s', 's'), ('k', 'k'), ('l', 'l'), ('æ', 'æ'), ('m', 'n'), ('p', '-'), ('æ', 'ɪ'), ('n', 'n'), ('d', '-'), ('b', 'b'), ('ɑ', 'æ'), ('t', 't'), ('ə', 'ə'), ('l', 'l')], [('b', 'b'), ('ə', 'ə'), ('s', 's'), ('ɑ', 'ɑ'), ('ɪ', 'ɪ'), ('d', 'd'), ('ə', 'ɪ'), ('-', 't'), ('s', 's'), ('ʌ', 'ʌ'), ('ŋ', 'ŋ'), ('k', '-'), ('ə', 'ə'), ('n', '-'), ('b', 'b'), ('æ', 'æ'), ('t', 't')], [('b', 'b'), ('ə', 'i'), ('s', 's'), ('ɑ', 'ɑ'), ('-', 'r'), ('ɪ', 'i'), ('d', 's'), ('ə', 'ʌ'), ('-', 'n'), ('-', 'j'), ('-', 'u'), ('s', 's'), ('-', 'w'), ('ʌ', 'ʌ'), ('ŋ', 'ŋ'), ('k', '-'), ('-', 'ð'), ('ə', 'ə'), ('n', '-'), ('b', 'b'), ('æ', 'æ'), ('t', 't')], [('b', 's'), ('ə', 'ɑ'), ('s', '-'), ('ɑ', 'ɪ'), ('-', 'n'), ('ɪ', 'ə'), ('d', '-'), ('ə', '-'), ('s', 's'), ('ʌ', 'ʌ'), ('ŋ', 'ŋ'), ('k', 'k'), ('ə', 'ə'), ('n', 'n'), ('b', 'b'), ('æ', 'æ'), ('t', 't')], [('ə', 'ə'), ('s', 's'), ('ɑ', 'ɑ'), ('ɪ', 'ɪ'), ('d', '-'), ('-', 'n'), ('ə', 'ə'), ('s', 's'), ('ʌ', 'ʌ'), ('ŋ', 'ŋ'), ('k', 'k'), ('ə', 'ə'), ('n', 'n'), ('b', 'b'), ('æ', 'æ'), ('t', 't')], [('b', 'ð'), ('ə', 'ə'), ('s', 's'), ('ɑ', 'ɑ'), ('ɪ', 'ɪ'), ('d', 'd'), ('-', 'h'), ('ə', 'æ'), ('-', 'z'), ('s', 's'), ('ʌ', 'ʌ'), ('ŋ', 'ŋ'), ('k', 'k'), ('ə', 'ə'), ('n', 'n'), ('b', 'b'), ('æ', 'æ'), ('t', 'k')], [('-', 'h'), ('ə', 'i'), ('s', 's'), (['ɑ', 'ɪ'], 'ɛ'), ('-', 'n'), ('d', 't'), ('ə', 'ʌ'), ('s', ['s', 's']), ('ʌ', 'ʌ'), ('-', 'm'), ('-', 'θ'), ('-', 'ɪ'), ('ŋ', 'ŋ'), ('k', '-'), ('ə', '-'), ('n', '-'), ('b', 'b'), ('æ', 'æ'), ('t', 'k')], [('b', 'b'), ('ʊ', 'ʊ'), ('ʃ', 'ʃ'), ('ɪ', 'ə'), ('z', 'z'), ('tʃ', 'tʃ'), ('o', 'o'), ('z', 'z'), ('ə', 'ə'), ('n', 'n'), ('æ', 'æ'), ('f', 'f'), ('t', 't'), ('ə', 'ə'), ('r', 'r')], [('b', 'b'), ('ʊ', 'ʊ'), ('ʃ', 'ʃ'), ('ɪ', 'i'), ('z', '-'), ('tʃ', 'ʃ'), ('o', 'ɛ'), ('-', 'l'), ('z', 'z'), ('ə', 'æ'), ('n', 'n'), ('-', 'd'), ('æ', 'æ'), ('f', 'f'), ('t', 't'), ('ə', 'ə'), ('r', 'r')], [('b', 'b'), ('ʊ', 'ʊ'), ('ʃ', 'ʃ'), ('ɪ', '-'), ('z', '-'), ('tʃ', '-'), ('o', '-'), ('z', '-'), ('ə', '-'), ('n', 'n'), ('æ', 'ɛ'), ('f', '-'), ('-', 'k'), ('t', 't'), ('ə', 'ə'), ('r', 'r')], [('b', 'ð'), ('ʊ', 'ɪ'), ('ʃ', 's'), ('ɪ', 'ɪ'), ('z', 'z'), ('tʃ', '-'), ('-', 'f'), ('-', 'r'), ('o', 'o'), ('z', 'z'), ('ə', 'ə'), ('n', 'n'), ('æ', 'æ'), ('f', 'f'), ('t', 't'), ('ə', 'ə'), ('r', 'r')], [('tʃ', 'tʃ'), ('i', 'i'), ('p', 'p'), ('k', 'k'), ('ə', 'ə'), ('n', 'n'), ('t', 't'), ('r', 'r'), ('o', 'o'), ('l', 'l'), ('ɪ', 'ɪ'), ('n', 'ŋ'), ('p', 'p'), ('e', 'e'), ('p', 'p'), ('ə', 'ə'), ('r', 'r')], [('tʃ', 'ʃ'), ('i', 'i'), ('p', '-'), ('k', 'k'), ('ə', 'ə'), ('n', 'n'), ('t', 't'), ('r', 'r'), ('o', 'o'), ('l', 'l'), ('ɪ', 'ɪ'), ('n', 'n'), ('p', 'p'), ('e', 'e'), ('p', 'p'), ('ə', 'ə'), ('r', 'r')], [('tʃ', 'k'), ('i', 'i'), ('p', 'p'), ('k', 'k'), ('ə', 'ə'), ('n', 'n'), ('t', 't'), ('r', 'r'), ('o', 'o'), ('l', 'l'), ('ɪ', 'ɪ'), ('n', 'ŋ'), ('p', 'p'), ('e', 'e'), ('p', 'p'), ('ə', 'ə'), ('r', 'r')], [('tʃ', 'tʃ'), ('i', 'i'), ('p', 'p'), ('k', '-'), ('-', 'p'), ('ə', 'ɛ'), ('n', 'n'), ('t', 't'), ('r', 'r'), ('o', 'o'), ('l', 'l'), ('ɪ', 'æ'), ('n', 'n'), ('-', 'd'), ('p', 'p'), ('e', 'e'), ('p', 'p'), ('ə', 'ə'), ('r', 'r')], [('k', 'ð'), ('ə', 'ɛ'), ('n', '-'), ('f', '-'), ('j', '-'), ('-', 'r'), ('u', 'ɪ'), ('z', 'z'), ('d', '-'), ('-', 'ə'), ('b', 'b'), ('ʌ', 'ɔ'), ('t', '-'), ('r', 'r'), ('ɔ', '-'), ('r', '-'), ('d', 'd'), ('ə', 'ə'), ('g', 'g'), ('ɛ', 'ɛ'), ('n', 'n')], [('-', 'm'), ('ə', 'ɑ'), ('n', '-'), ('f', '-'), ('j', '-'), ('u', 'ɪ'), ('-', 'k'), ('-', 'i'), ('z', 'z'), ('-', 'f'), ('-', 'ɛ'), ('-', 'l'), ('d', 't'), ('b', 'b'), ('ʌ', 'ɜ'), ('t', '-'), ('r', 'r'), ('ɔ', '-'), ('r', '-'), ('-', 'n'), ('d', 'd'), ('ə', 'ə'), ('g', 'g'), ('ɛ', 'ɛ'), ('n', 'n')], [('k', 'k'), ('ə', 'ə'), ('n', 'n'), ('f', 'f'), ('j', 'j'), ('u', 'u'), ('z', 'z'), ('d', 'd'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('r', '-'), ('-', 'w'), ('ɔ', 'ɑ'), ('r', 'r'), ('d', 'd'), ('ə', 'ə'), ('g', 'g'), ('ɛ', 'ɛ'), ('n', 'n')], [('k', 'k'), ('ə', 'ə'), ('n', 'n'), ('f', 'f'), ('j', 'j'), ('u', 'u'), ('z', 'z'), ('d', 'd'), ('b', 'b'), ('ʌ', 'ɑ'), ('t', '-'), ('r', '-'), ('-', 'ɪ'), ('-', 'w'), ('ɔ', 'ɜ'), ('r', 'r'), ('d', 'd'), ('-', 'z'), ('ə', 'ə'), ('g', 'g'), ('ɛ', 'ɛ'), ('n', 'n')], [('d', 'd'), ('ɪ', 'ɪ'), ('s', 's'), ('t', 't'), ('ə', 'ə'), ('n', 'n'), ('t', 't'), ('l', 'l'), ('i', 'ʊ'), ('k', 'k'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ'), ('b', 'b'), ('e', 'e'), ('s', 's'), ('m', 'm'), ('ə', 'ə'), ('n', 'n'), ('t', 't')], [('d', 'd'), ('ɪ', 'ʌ'), ('s', 's'), ('t', 't'), ('ə', 'i'), ('n', '-'), ('t', '-'), ('l', 'l'), ('i', 'i'), ('k', 'k'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ'), ('b', 'b'), ('e', 'e'), ('s', 's'), ('m', 'm'), ('ə', 'ə'), ('n', 'n'), ('t', 't')], [('d', 'ð'), ('ɪ', 'ɪ'), ('s', 's'), ('-', 'ɪ'), ('-', 'n'), ('t', 's'), ('ə', 'ɛ'), ('-', 's'), ('-', 'ə'), ('n', 'n'), ('t', 't'), ('l', 'l'), ('i', 'i'), ('-', 'l'), ('-', 'i'), ('k', 'k'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ'), ('b', 'b'), ('e', 'e'), ('s', 's'), ('m', 'm'), ('ə', 'ə'), ('n', 'n'), ('t', 't')], [('d', 'ð'), ('ɪ', 'ɪ'), ('s', 's'), ('t', '-'), ('ə', 'ɪ'), ('n', '-'), ('t', 'z'), ('l', 'l'), ('i',
['ɑ', 'ɪ']), ('k', 't'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ'), ('b', 'b'), ('e', 'e'), ('s', 's'), ('m', 'm'), ('ə', 'ə'), ('n', 'n'), ('t', 't')], [('d', 'θ'), ('ʌ', 'ʌ'), ('n', 'm'), ('w', 'w'), ('ɪ', 'ɪ'), ('θ', 'θ'), ('f', 'f'), (['ɑ', 'ɪ'], 'ʌ'), ('n', 'n'), ('ɛ', 'ɪ'), ('s', 'z'), ('t', '-'), ('h', 'h'), ('æ', 'æ'), ('n', 'n'), ('d', 'd'), ('ə', 'ə'), ('l', 'l')], [('d', 'd'), ('ʌ', 'ʌ'), ('n', 'm'), ('w', 'w'), ('ɪ', 'ɪ'), ('θ', 'θ'), ('f', 'f'), (['ɑ', 'ɪ'], 'ʌ'), ('n', 'n'), ('ɛ', 'ɪ'), ('s', 'z'), ('t', '-'), ('h', 'h'), ('æ', 'æ'), ('n', 'n'), ('d', 'd'), ('ə', 'ə'), ('l', 'l')], [('d', 'dʒ'), ('ʌ', 'ɑ'), ('n', 'n'), ('w', 'w'), ('ɪ', 'ʌ'), ('θ', 'z'), ('f', 'f'), (['ɑ', 'ɪ'], 'ʌ'), ('n', 'n'), ('ɛ', ['i', 'ɛ']), ('s', 's'), ('t', 't'), ('h', '-'), ('æ', 'ɪ'), ('n', 'n'), ('d', 'ð'), ('ə', 'o'), ('l', '-')], [('d', 'd'), ('ʌ', 'ʌ'), ('n', 'n'), ('w', 'w'), ('ɪ', 'ɪ'), ('θ', 'θ'), ('f', 'f'), (['ɑ', 'ɪ'], 'ʌ'), ('n', ['n', 'n']), ('ɛ', 'ɪ'), ('s', '-'), ('-', 'n'), ('t', 't'), ('h', '-'), ('æ', 'ɛ'), ('n', 'n'), ('d', 'd'), ('ə', 'o'), ('l', '-')], [('d', 'dʒ'), ('ʌ', 'ɑ'), ('n', 'n'), ('w', 'w'), ('ɪ', 'ʌ'), ('θ', 'z'), ('f', 'f'), ('ɑ', 'ɑ'), ('ɪ', 'ɪ'), ('n', 'n'), ('ɛ', 'æ'), ('s', 'z'), ('t', 'ð'), ('h', '-'), ('æ', ['i', 'ɛ']), ('n', 'n'), ('d', 'd'), ('-', 'ð'), ('ə', 'o'), ('l', '-')], [('ɛ', 'e'), ('m', '-'), ('b', 'b'), ('ɑ', 'ɑ'), ('r', 'r'), ('k', 'k'), ('ɔ', 'ɔ'), ('r', 'r'), ('-', 'ɔ'), ('-', 'r'), ('-', 'm'), ('-', 'e'), ('t', 't'), ('e', 'e'), ('k', 'k'), ('h', '-'), ('-', 'f'), ('ɜ', 'ɔ'), ('r', 'r'), ('ʃ', 'ʃ'), ('i', 'i'), ('t', 't')], [('ɛ', 'ɛ'), ('m', 'm'), ('b', 'b'), ('ɑ', 'ɑ'), ('r', 'r'), ('k', 'k'), ('ɔ', 'ɔ'), ('r', 'r'), ('t', 't'), ('e', 'e'), ('k', 'k'), ('h', 'h'), ('ɜ', 'ɜ'), ('r', 'r'), ('ʃ', 'ʃ'), ('i', 'i'), ('t', 't')], [('ɛ', 'ɛ'), ('m', 'm'), ('b', 'b'), ('ɑ', 'ɑ'), ('r', 'r'), ('k', 'k'), ('ɔ', 'ɔ'), ('r', 'r'), ('t', 't'), ('e', 'e'), ('k', 'k'), ('h', '-'), ('-', 'j'), ('ɜ', 'ɔ'), ('r', 'r'), ('ʃ', 'ʃ'), ('i', 'i'), ('t', 'p')], [('ɛ', 'æ'), ('m', 'n'), ('-', 'd'), ('b', 'b'), ('ɑ', 'ɑ'), ('r', 'r'), ('k', 'k'), ('ɔ', 'ə'), ('r', 'r'), ('t', 't'), ('e', 'e'), ('k', 'k'), ('h', 'h'), ('ɜ', 'ɜ'), ('r', 'r'), ('ʃ', 'ʃ'), ('i', 'i'), ('t', 't')], [('ɛ', 'æ'), ('m', 'n'), ('-', 'd'), ('b', 'b'), ('ɑ', 'ɑ'), ('r', 'r'), ('k', '-'), ('-', 'b'), ('ɔ', 'ɔ'), ('r', 'r'), ('t', 't'), ('e', 'e'), ('k', 'k'), ('h', 'h'), ('ɜ', 'ɜ'), ('r', 'r'), ('ʃ', 'ʃ'), ('i', 'i'), ('t', 'p')], [('ɛ', 'æ'), ('ʒ', 'z'), ('-', 'j'), ('ə', 'ɔ'), ('r', 'r'), ('f', 'f'), ('e', 'e'), ('m', 'm'), ('w', 'w'), ('ɪ', 'ɪ'), ('θ', 'θ'), ('l', 'l'), ('i', 'i'), ('g', 'g'), ('ə', 'ə'), ('l', 'l')], [('m', 'm'), ('ɛ', 'ɛ'), ('ʒ', 'ʒ'), ('ə', 'ə'), ('r', 'r'), ('f', ['f', 'f']), ('e', 'e'), ('m', 'm'), ('w', 'w'), ('ɪ', 'ɪ'), ('θ', 'θ'), ('l', '-'), ('-', 'p'), ('i', 'i'), ('g', 'k'), ('ə', 'o'), ('l', '-')], [('m', 'm'), ('ɛ', 'ɛ'), ('ʒ', 'ʒ'), ('ə', 'ə'), ('r', 'r'), ('f', 'v'), ('e', 'e'), ('m', 'n'), ('w', 'w'), ('ɪ', 'ɪ'), ('θ', 'θ'), ('l', '-'), ('-', 'ð'), ('i', 'ə'), ('g', 'k'), ('ə', 'ʊ'), ('l', 'l')], [('m', 'm'), ('ɛ', 'ɛ'), ('ʒ', 'ʒ'), ('ə', 'ə'), ('r', 'r'), ('f', '-'), ('e', 'ɪ'), ('m', '-'), ('-', 'ŋ'), ('w', 'w'), ('ɪ', 'ɪ'), ('θ', 'θ'), ('l', '-'), ('-', 'ð'), ('i', 'ə'), ('g', 'g'), ('ə', 'o'), ('l', 'l')], [('m', 'm'), ('ɛ', 'ɛ'), ('ʒ', 'ʒ'), ('ə', 'ə'), ('r', 'r'), ('f', 'f'), ('-', 'l'), ('e', 'e'), ('m', 'm'), ('w', 'w'), ('ɪ', 'ɪ'), ('θ', 'θ'), ('-', 'f'), ('l', 'l'), ('i', 'e'), ('g', '-'), ('-', 'v'), ('ə', 'ə'), ('l', '-'), ('-', 'r')], [('-', 'w'), ('ɛ', 'ɛ'), ('-', 'r'), ('ʒ', 'z'), ('-', 'j'), ('ə', 'ɔ'), ('r', 'r'), ('f', 'f'), ('e', 'e'), ('m', 'm'), ('w', 'w'), ('ɪ', 'ɪ'), ('θ', 'θ'), ('l', 'l'), ('i', 'i'), ('g', 'g'), ('ə', 'ə'), ('l', 'l')], [('r', 'r'), ('æ', 'æ'), ('m', '-'), ('p', 'b'), ('ə', 'ɪ'), ('n', '-'), ('t', 't'), ('b', 'b'), ('o', 'o'), ('s', 's'), ('t', 't'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ'), ('k', 'k'), ('æ', 'æ'), ('p', 'p'), ('t', 't'), ('ə', 'ə'), ('n', 'n')], [('r', 'r'), ('æ', 'æ'), ('m', 'n'), ('-', 'd'), ('p', 'p'), ('ə', 'ə'), ('n', '-'), ('t', '-'), ('b', 'b'), ('o', 'o'), ('s', 's'), ('t', 't'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ'), ('k', 'k'), ('æ', 'æ'), ('p', 'p'), ('t', 't'), ('ə', 'ə'), ('n', 'n')], [('-', 'b'), ('æ', 'o'), ('m', '-'), ('p', '-'), ('ə', '-'), ('n', '-'), ('t', 'θ'), ('b', '-'), ('o', '-'), ('s', 's'), ('t', '-'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ'), ('k', 'k'), ('-', 'f'), ('æ', 'ɔ'), ('-', 'r'), ('-', 'ð'), ('-', 'ə'), ('-', 'k'), ('-', 'æ'), ('p', 'p'), ('t', 't'), ('ə', 'ə'), ('n', 'n')], [('r', 'r'), ('æ', 'æ'), ('m', '-'), ('p', 'p'), ('ə', 'æ'), ('n', '-'), ('t', 't'), ('b', 'b'), ('o', 'o'), ('s', 's'), ('t', 't'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ'), ('k', 'k'), ('æ', 'æ'), ('p', 'p'), ('t', 't'), ('ə', 'ə'), ('n', 'n')], [('r', 'r'), ('æ', 'æ'), ('m', 'n'), ('p', 't'), ('ə', 'ə'), ('n', '-'), ('t', 'd'), ('b', 'b'), ('o', 'ɜ'), ('-', 'r'), ('s', 's'), ('t', 't'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ'), ('k', 'k'), ('æ', 'æ'), ('p', 'p'), ('t', 't'), ('ə', 'ə'), ('n', 'n')], [('r', 'r'), ('æ', 'æ'), ('m', 'm'), ('p', 'p'), ('ə', 'ɪ'), ('n', '-'), ('t', 't'), ('b', 'b'), ('o', 'o'), ('s', '-'), ('t', 't'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ'), ('k', 'k'), ('æ', 'æ'), ('p', 'p'), ('t', 't'), ('ə', 'ə'), ('n', 'n')], [('r', 'r'), ('æ', 'æ'), ('m', 'm'), ('p', 'p'), ('ə', 'ɛ'), ('n', '-'), ('t', 't'), ('b', 'b'), ('o', 'o'), ('-', 'θ'), ('s', 's'), ('t', 't'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ'), ('k', ['k', 'k']), ('æ', 'ɛ'), ('p', 'p'), ('t', 't'), ('ə', 'ɪ'), ('n', 'n')], [('r', 'r'), ('æ', 'æ'), ('m', 'm'), ('p', '-'), ('-', 'r'), ('ə', 'æ'), ('n', 'm'), ('t', 'f'), ('b', '-'), ('o', 'æ'), ('s', 's'), ('t', 't'), ('ɪ', '-'), ('ŋ', '-'), ('k', 'k'), ('æ', 'æ'), ('p', 'p'), ('t', 't'), ('ə', '-'), ('n', '-')], [('r', 'r'), ('o', 'ʌ'), ('d', 'b'), ('ð', 'ð'), ('ə', 'ə'), ('l', 'l'), ('æ', 'æ'), ('m', 'm'), ('p', 'p'), ('f', 'f'), ('ɔ', 'ɔ'), ('r', 'r'), ('t', 't'), ('i', 'i'), ('z', 'z'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ')], [('r', 'r'), ('o', 'o'), ('d', 'd'), ('-', 'w'), ('-', 'ə'), ('ð', 'z'), ('ə', '-'), ('l', '-'), ('æ', '-'), ('m', 'm'), ('-', 'ɛ'), ('-', 'n'), ('p', 't'), ('f', 'f'), ('ɔ', 'ɔ'), ('r', 'r'), ('t', 't'), ('i', 'i'), ('z', 'z'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ')], [('r', 'r'), ('o', 'o'), ('d', 't'), ('ð', 'ð'), ('ə', 'ə'), ('l', 'l'), ('æ', 'æ'), ('m', 'm'), ('p', 'p'), ('f', 'f'), ('ɔ', 'ɔ'), ('r', 'r'), ('t', 't'), ('i', 'i'), ('z', 'z'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ')], [('r', 'r'), ('o', 'o'), ('d', 'd'), ('ð', 'ð'), ('ə', 'ə'), ('l', 'l'), ('æ', 'æ'), ('m', 'm'), ('p', 'p'), ('f', 'p'), ('ɔ', 'ɑ'), ('r', 'r'), ('t', ['t', 't']), ('i', 'i'), ('z', 'z'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ')], [('r', 'r'), ('o', 'o'), ('d', 'd'), ('ð', 'ð'), ('ə', 'ə'), ('l', 'l'), ('æ', 'ɛ'), ('m', '-'), ('-', 'ŋ'), ('p', 'θ'), ('f', 'f'), ('ɔ', 'ɔ'), ('r', 'r'), ('t', 'tʃ'), ('i', 'i'), ('z', 'z'), ('ɪ', 'i'), ('ŋ', '-')], [('r', 'r'), ('o', 'o'), ('d', '-'), ('-', 'k'), ('ð', 'ð'), ('ə', 'ə'), ('l', 'l'), ('æ', 'æ'), ('m', 'm'), ('p', 'p'), ('f', 'f'), ('ɔ', 'ɔ'), ('r', 'r'), ('t', '-'), ('i', 'i'), ('z', 'z'), ('ɪ', 'i'), ('ŋ', '-')], [('r', 'r'), ('o', 'o'), ('d', '-'), ('ð', 'ð'), ('ə', 'ə'), ('l', 'l'), ('æ', 'i'), ('-', 'p'), ('-', 'l'), ('-', 'æ'), ('m', 'm'), ('p', 'p'), ('f', 'f'), ('ɔ', 'ɔ'), ('r', 'r'), ('t', 't'), ('i', 'ɛ'), ('z', 's'), ('-', 't'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ')], [('s', 's'), ('ə', 'ə'), ('p', 'p'), ('ɔ', 'ɔ'), ('r', 'r'), ('t', 't'), ('w', 'w'), ('ɪ', 'ɪ'), ('θ', 'θ'), ('d', 'd'), ('ɑ', 'ɑ'), ('k', 'k'), ('æ', 'æ'), ('n', 'n'), ('d', 'd'), ('tʃ', 'tʃ'), ('i', 'e'), ('r', 'r')], [('s', 's'), ('ə', 'ə'), ('p', 'p'), ('ɔ', 'ɔ'), ('r', 'r'), ('t', 't'), ('w', 'w'), ('ɪ', 'ɪ'), ('θ', 'θ'), ('d', 'd'), ('ɑ', 'ɑ'), ('k', 'k'), ('æ', 'ɪ'), ('n', 'n'), ('d', 't'), ('tʃ', '-'), ('i', 'u'), ('r', '-')], [('s', 's'), ('ə', 'ə'), ('p', 'p'), ('ɔ', 'ɔ'), ('r', 'r'), ('t', 't'), ('w', 'w'), ('ɪ', 'ɪ'), ('θ', 'θ'), ('d', 'd'), ('ɑ', 'ɑ'), ('k', 'k'), ('æ', 'ɛ'), ('n', 'n'), ('d', 't'), ('tʃ', '-'), ('i', 'ə'), ('r', 'r')], [('s', 's'), ('ə', 'ə'), ('p', 'p'), ('ɔ', 'ɔ'), ('r', 'r'), ('t', 't'), ('w', 'w'), ('ɪ', 'ɪ'), ('θ', 'θ'), ('d', 'd'), ('ɑ', 'ɑ'), ('k', 'g'), ('æ', 'æ'), ('n', 'n'), ('d', 'd'), ('tʃ', 'tʃ'), ('i', 'i'), ('r', '-'), ('-', 'z')], [('t', 'θ'), ('ɛ', '-'), ('k', '-'), ('n', 'n'), ('i', 'ɪ'), ('k', 'k'), ('b', 'p'), ('ʌ', 'ɜ'), ('t', '-'), ('-', 'r'), ('s', 's'), ('ɛ', 'ɛ'), ('n', 'n'), ('t', 't'), ('r', 'r'), ('ɪ', 'ɪ'), ('z', 'z'), ('ʊ', 'ʊ'), ('l', 'l'), ('t', 't')], [('t', 't'), ('ɛ', 'ɛ'), ('k', 'k'), ('n', 'm'), ('i', 'i'), ('k', '-'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('s', 's'), ('ɛ', 'ɛ'), ('n', 'n'), ('t', 't'), ('r', 'r'), ('ɪ', 'ɪ'), ('z', 'z'), ('ʊ', 'ʊ'), ('l', 'l'), ('t', 't')], [('t', 't'), ('ɛ', 'ɛ'), ('k', 'k'), ('n', 'm'), ('i', 'i'), ('k', '-'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('s', 's'), ('ɛ', 'æ'), ('n', 'n'), ('t', 'd'), ('r', 'r'), ('ɪ', 'ɪ'), ('z', 'z'), ('ʊ', 'ʊ'), ('l', 'l'), ('t', 't')], [('-', 'n'), ('ɛ', 'ɛ'), ('k', 'k'), ('n', '-'), ('-', 'd'), ('i', 'i'), ('k', '-'), ('-', 'p'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('s', 's'), ('ɛ', 'ɛ'), ('n', 'n'), ('t', 't'), ('r', 'r'), ('ɪ', 'ɪ'), ('z', 'z'), ('ʊ', 'ʊ'), ('l', 'l'), ('t', 't')], [('θ', 'b'), ('ɪ', 'ɛ'), ('ŋ', '-'), ('k', 'g'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ'), ('f', 'f'), ('ɔ', 'ɔ'), ('r', 'r'), ('ð', 'ð'), ('ə', 'ə'), ('h', 'h'), ('i', 'i'), ('r', 'r'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ')], [('θ', 's'), ('ɪ', 'ɛ'), ('ŋ', 'n'), ('k', 't'), ('ɪ', 'ɪ'), ('-', 'n'), ('-', 's'), ('-', 'ɪ'), ('ŋ', 'ŋ'), ('f', 'f'), ('ɔ', 'ɔ'), ('r', 'r'), ('ð', 'ð'), ('ə', 'ə'), ('h', 'h'), ('i', 'i'), ('r', 'r'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ')], [('θ', 's'), ('-', 'p'), ('ɪ', 'i'), ('ŋ', '-'), ('k', 'k'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ'), ('f', 'f'), ('ɔ', 'ɔ'), ('r', 'r'), ('ð', 'ð'), ('ə', 'ə'), ('h', 'h'), ('i', 'i'), ('r', 'r'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ')], [('θ', 'ð'), ('ɪ', 'ə'), ('ŋ', '-'), ('k', 'g'), ('ɪ', 'ɪ'), ('ŋ', '-'), ('-', 'g'), ('f', 'f'), ('ɔ', 'ɔ'), ('r', 'r'), ('ð', 'ð'), ('ə', 'ə'), ('h', 'h'), ('i', 'i'), ('r', 'r'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ')], [('θ', 'f'), ('ɪ', 'ɪ'), ('ŋ', '-'), ('k', 'g'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ'), ('f', 'f'), ('ɔ', 'ɔ'), ('r', 'r'), ('ð', 'ð'), ('ə', 'ə'), ('h', 'h'), ('i', 'i'), ('r', 'r'), ('ɪ', 'ɪ'), ('ŋ', 'ŋ')], [('t', 't'), ('u', ['u', 'ə']), ('-', 'b'), ('s', 'z'), ('ɔ', 'ɔ'), ('r', 'r'), ('t', '-'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 'p'), ('f', 'ð'), ('i', ['ə', 'ɛ']), ('r', 'r'), ('ɪ', 'ɪ'), ('n', 'n'), ('s', 's'), ('ɑ', 'ɑ'), ('ɪ', 'ɪ'), ('d', 'd')], [('t', 's'), ('u', '-'), ('s', 't'), ('ɔ', 'ɑ'), ('r', 'r'), ('t', 't'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('f', 'f'), ('i', 'i'), ('r', 'r'), ('ɪ', 'ɪ'), ('n', 'n'), ('s', 's'), ('ɑ', 'ɑ'), ('ɪ', 'ɪ'), ('d', 'd')], [('t', 't'), ('u', 'u'), ('s', 's'), ('ɔ', 'ɔ'), ('r', 'r'), ('t', '-'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('f', 'v'), ('i', 'i'), ('r', 'r'), ('ɪ', 'ɪ'), ('n', 'n'), ('s', 's'), ('ɑ', 'ɑ'), ('ɪ', 'ɪ'), ('d', 'd')], [('t', 't'), ('u', 'u'), ('s', 's'), ('ɔ', ['ɑ', 'ʊ']), ('r', 'r'), ('t', '-'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('f', 'f'), ('i', 'i'), ('r', 'r'), ('ɪ', 'ɪ'), ('n', 'n'), ('s', 's'), ('ɑ', 'ɑ'), ('ɪ', 'ɪ'), ('d', 'd')], [('t', 't'), ('u', ['u', 'ə']), ('-', 'b'), ('s', 'z'), ('ɔ', 'ɔ'), ('r', 'r'), ('t', '-'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 'p'), ('f', 'ð'), ('i', ['ə', 'ɛ']), ('r', 'r'), ('ɪ', 'ɪ'), ('n', 'n'), ('s', 's'), ('ɑ', 'ɑ'), ('ɪ', 'ɪ'), ('d', 'd')], [('ɑ', 'ɑ'), ('ɪ', 'ɪ'), ('t', '-'), ('ə', '-'), ('l', '-'), ('s', 'z'), ('i', '-'), ('t', '-'), ('s', 's'), ('-', 'i'), ('w', 'w'), ('ɪ', 'ɪ'), ('θ', 'θ'), ('w', 'w'), ('ʌ', 'ʌ'), ('n', 'n'), ('d', 'd'), ('ə', 'ə'), ('r', 'r')], [('v', 'b'), (['ɑ', 'ɪ'], 'ɑ'), ('t', 't'), ('ə', 'ə'), ('l', 'l'), ('s', 's'), ('i', 'i'), ('t', 't'), ('s', 's'), ('w', 'w'), ('ɪ', 'ɪ'), ('θ', 'θ'), ('w', 'w'), ('ʌ', 'ʌ'), ('n', 'n'), ('d', 'd'), ('ə', 'ə'), ('r', 'r')], [('v', 'p'), ('ɑ', '-'), ('ɪ', '-'), ('t', '-'), ('ə', '-'), ('l', 'l'), ('-', 'e'), ('-', 'ð'), ('-', 'ə'), ('-', 'r'), ('-', 'ɪ'), ('s', 's'), ('i', 'i'), ('t', 't'), ('s', 's'), ('w', 'w'), ('ɪ', 'ɪ'), ('θ', 'θ'), ('w', 'w'), ('ʌ', 'ʌ'), ('n', 'n'), ('d', 'd'), ('ə', 'ə'), ('r', 'r')]]


def distance(t):
    '''
    calculates the distance between the strings in the output of realine
    '''
    t = t
    ref = t[0]
    hyp = t[1]

    m = len(ref)
    n = len(hyp)

    # special case
    if ref == hyp:
        return 0
    if m == 0:
        return n
    if n == 0:
        return m

    if m < n:
        ref, hyp = hyp, ref
        m, n = n, m
    # use O(min(m, n)) space
    distance = np.zeros((2, n + 1), dtype=np.int32)
    # initialize distance matrix
    for j in range(0, n + 1):
        distance[0][j] = j
    # calculate levenshtein distance
    for i in range(1, m + 1):
        prev_row_idx = (i - 1) % 2
        cur_row_idx = i % 2
        distance[cur_row_idx][0] = i
        for j in range(1, n + 1):
            if ref[i - 1] == hyp[j - 1]:
                distance[cur_row_idx][j] = distance[prev_row_idx][j - 1]
            else:
                s_num = distance[prev_row_idx][j - 1] + 1
                i_num = distance[cur_row_idx][j - 1] + 1
                d_num = distance[prev_row_idx][j] + 1
                distance[cur_row_idx][j] = min(s_num, i_num, d_num)
    return distance[m % 2][n]


# e = [distance(item) for item for in alignments]
# print (e)

c = [(distance(ii) for ii in i) for i in alignments]
# for i in alignments:
#     for ii in i:
#         c.append(distance(ii))
print(c)


# def calcPhonemeErrors(tup):
#     '''
#     source: the real string (stimuli)
#     target: the produced string by participants
#     '''

#     ##### calculate insertion #### ('-','p')
#     insertion_count = 0
#     insertions = []
#     for item in tup:
#         phone_1 = item[0]
#         #print (phone_1)
#         phone_2 = item[1]
#         #print (phone_2)
#         if phone_1 == '-':
#             i = phone_1, phone_2
#             insertions.append(i)
#             insertion_count += 1
#     print(f"Insertions' count: {insertion_count} ==> {insertions}")
#     print ()

#     ##### calculate deletion #### ('p','-')
#     deletion_count = 0
#     deletions = []
#     for item in tup:
#         phone_1 = item[0]
#         phone_2 = item[1]
#         if phone_2 == '-':
#             s = phone_1, phone_2
#             deletions.append(s)
#             deletion_count += 1
#     print(f"Deletions' count: {deletion_count} ==> {deletions}")
#     print()

    

#     ##### calculate substitution #### ('æ', 'ə')
#     substitution_count = 0
#     substitutions = []
#     for item in tup:
#         phone_1 = item[0]
#         phone_2 = item[1]
#         if phone_1 != phone_2 and phone_1 != '-' and phone_2 != '-':
#             x = phone_1, phone_2
#             substitutions.append(x)
#             substitution_count += 1
#     print(f"Substitutions' count: {substitution_count} ==> {substitutions}")
#     print()
    
#     return list((deletion_count, deletions)), list((insertions, insertion_count)), list((substitutions, substitution_count))



# calc = [calcPhonemeErrors(i) for i in alignments]

# #dict {}
# for i in calc:
#     print (i[0])

