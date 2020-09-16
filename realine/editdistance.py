import sys
import numpy as np
import pandas as pd

class EditDistance(object):

    def read_file(self, path):
        file = pd.read_excel(path, header=None)
        df = file.stack().groupby(level=0).apply(''.join)
        #print (df)
        h = [i.replace('LB', '') for i in df]
        v = iter(h)
        list_of_tuples = [(i, next(v)) for i in v]
        return list_of_tuples
    
    def distance(self, t):
        self.t = t
        ref = self.t[0]
        hyp = self.t[1]
       
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

    

if __name__ == "__main__":
    
    edit = EditDistance()
    data = edit.read_file('./data/alignments.xlsx')
    values = [edit.distance(item) for item in data]
    print (values)

