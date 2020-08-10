from realine import *

# reading the file
import csv
all_rows = []
with open("asd.csv", 'r', encoding="mac_roman") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    print(csvreader)

    for row in csvreader:
        parser = " ".join(row).strip()
        print(parser)
        all_rows.append(parser)
len(all_rows)


# v = iter(hi)

# list_of_tuples = [(i, next(v)) for i in v]  # creates list of tuples
# #vv = iter(li)
# #vv
# for i in list_of_tuples:
#     print (i)
