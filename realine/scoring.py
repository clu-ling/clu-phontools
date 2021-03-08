#!/usr/bin/env python

import argparse

import pandas as pd
import numpy as np
from realine.realine import ReAline

al = ReAline()


def read_file(path):
    '''
    Read the excel file and create another excel file with the alignemnts (output of realine)
    '''
    file = pd.read_excel(path, header=None, engine='openpyxl')
    df = file.stack().groupby(level=0).apply(' '.join)
    #df = [i.replace('LB', '') for i in df]
    myList = [i.split(' ') for i in df]
    v = iter(myList)
    list_of_tuples = [(i, next(v)) for i in v]
    return [al.align(i[0], i[1])[0] for i in list_of_tuples]


def decompose_distance(tup):

    ##### calculate insertion #### ('-','p')
    insertion_count = 0
    insertions = []
    for item in tup:
        phone_1 = item[0]
        #print (phone_1)
        phone_2 = item[1]
        #print (phone_2)
        if phone_1 == '-':
            i = list((phone_1, phone_2))
            insertions.append(i)
            insertion_count += 1
    #print(f"Insertions' count: {insertion_count} ==> {insertions}")
    #print()

    ##### calculate deletion #### ('p','-')
    deletion_count = 0
    deletions = []
    for item in tup:
        phone_1 = item[0]
        phone_2 = item[1]
        if phone_2 == '-':
            s = list((phone_1, phone_2))
            deletions.append(s)
            deletion_count += 1
    #print(f"Deletions' count: {deletion_count} ==> {deletions}")
    #print()

    ##### calculate substitution #### ('æ', 'ə')
    substitution_count = 0
    substitutions = []
    for item in tup:
        phone_1 = item[0]
        phone_2 = item[1]
        if phone_1 != phone_2 and phone_1 != '-' and phone_2 != '-':
            x = list((phone_1, phone_2))
            substitutions.append(x)
            substitution_count += 1
    #print(f"Substitutions' count: {substitution_count} ==> {substitutions}")
    #print()
    return ("deletions:", list((deletion_count, deletions))), "inserions:", list((insertion_count, insertions)), "substitutions:", list((substitution_count, substitutions))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Realign Excel data using re-aline.')
    parser.add_argument("--input", "-i", help="Input file.",
                        type=str, required=True)
    parser.add_argument("--output", "-o", help="output file.",
                        type=str, required=True)

    args = parser.parse_args()

    infile = args.input
    outfile = args.output

    # read the excel file and generate alignments
    alignments = read_file(infile)
    # decompose
    decomposition = [decompose_distance(item) for item in alignments]

    # create a dataframe
    df = pd.DataFrame()
    # Column 1: creating a column for alignments
    df['alignments'] = alignments
    # Column 2: decompose processes (deletion, substitution, insertion)
    df['decomposition'] = decomposition

    df.to_excel(outfile, index=False)
