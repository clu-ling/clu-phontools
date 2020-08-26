import pandas as pd
import numpy as np
from realine import ReAline

al = ReAline()

def read_file(path):
    file = pd.read_excel(path, header=None)
    df = file.stack().groupby(level=0).apply(' '.join)

    myList = [i.split(' ') for i in df]

    v = iter(myList)
    list_of_tuples = [(i, next(v)) for i in v]

    # return list of alignments
    return [al.align(i[0], i[1])[0] for i in list_of_tuples]


# save to file
alignments = read_file('./data/NonseAlignments.xlsx')  

df = pd.DataFrame()
# Creating a column
df['alignments'] = alignments
df.to_excel('./results/results_with_stress.xlsx', index=False)
