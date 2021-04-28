import pandas as pd
from realine import ReAline
from typing import List, Tuple
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder


def read_file(path: str) -> List[List[Tuple[str, str]]]:
    al = ReAline()
    file = pd.read_excel(path, header=None)
    df = file.stack().groupby(level=0).apply(' '.join)
    myList = [i .split(' ') for i in df]
    v = iter(myList)
    list_of_tuples = [(i, next(v)) for i in v]
    # return list of alignments
    return [al.align(i[0], i[1])[0] for i in list_of_tuples]


class Classifier(object):
    def __init__(self):
        """
        Initializes the classifier.
        """
        self.label_encoder = LabelEncoder()
        self.model = LogisticRegression(solver="liblinear", multi_class="ovr")

    def train(self, alignments):
        """
        This function iteracts over the alignments and labels each tuple as either:
        - perfect 
        - deletion
        - inserion
        - substitution
        - LB
        - one-to-many

        The output is a dictionary {('b','b'), 'perfect} with the tuple as key and the label as the value
        """
        labels = ['perfect', 'deletion', 'insertion', 'substitution']
        dict = {}
        for item in alignments:
            for i in item:
                if i[0] == i[1]:
                    dict[i] = labels[0]
                elif i[0] == '-':
                    dict[i] = labels[1]
                elif i[1] == '-':
                    dict[i] = labels[2]
                # elif i[0] != i[1] and i[0] != '-' and i[1] != '-':
                #     dict[i] = labels[3]

        return dict, labels




if __name__ == "__main__":
    readFile = read_file('NonseAlignments.xlsx')
    c = Classifier()
    a = c.train(readFile)
    print (a)
