from aline import ReAline
import pandas as pd
import numpy as np

def read_files(path):
    file = pd.read_excel(path, header=None)
    
    return file


s = read_files('alignments.xlsx')
print (s)





# cat = ReAline()
# print(cat)
# a = cat.sigma_skip('p')
# print(a)
# b = cat.V('p')
# print(b)
# c = cat.R('p', 'b')
# print(c)
# d = cat.diff('p', 'b', 'place')
# print(d)
# e = cat.delta('p', 'b')
# print(e)
# f = cat.sigma_sub('p', 'b')
# print(f)
# g = cat.sigma_exp('p', 'bi')
# print(g)
# h = cat.align('cat', 'bat')
# print(h)
