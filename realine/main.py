import aline
from aline import ReAline
#from aline import ReAline.align as al
import pandas as pd
import numpy as np

al = ReAline()

# reading the file
def read_files(path):
    file = pd.read_excel(path, header=None)
    df = file.stack().groupby(level=0).apply(''.join)
    # list of lists
    K = 'LB'
    list_of_lists = []
    for i in df:
        res = [i for j in i.split(K) for i in (j, K)][:-1]
        res = [i for i in res if i]
        list_of_lists.append(res)
    # list of tuples
    v = iter(list_of_lists)
    list_of_tuples = [(i, next(v)) for i in v]
    another_list = []
    for i in list_of_tuples:
        s = list(zip(i[0], i[1]))
        another_list.append(s)

    return another_list

def do_align(a):
    alignments = []
    for L in a:
        print ('--------------------')
        print (L)
        print ('--------------------')
        for pair in L:
            alignment = al.align(pair[0], pair[1])[0]
            alignment = ['({})'.format(a) for a in alignment]
            alignment = ' '.join(alignment)
            alignment = ('{} ~ {} : {}'.format(pair[0], pair[1], alignment))
            alignments.append(alignment)
            print (alignment)
    return alignments


# save to file
read_file = read_files('./data/alignments.xlsx')  # list of lists of tuples
#print (s)
alignments = do_align(read_file)


df = pd.DataFrame()
# Creating a column
df['alignments'] = alignments
df.to_excel('./results/results.xlsx', index= False)
