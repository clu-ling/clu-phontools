from realine import ReAline

realine = ReAline()

alignments = [('æ', '-'), ('-', 'd'), ('v', 'v'), ('æ', 'ɛ')]


def phoneSimilarity(t):
    #realine = ReAline()
    a = t[0]
    b = t[1]
    return realine.delta(a, b)

for i in alignments:
    print (i)
    s = phoneSimilarity(i)
    print (s)