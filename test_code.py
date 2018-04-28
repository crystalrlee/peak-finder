# Learning how to read .csv files

import csv

peak_data = open("/home/crystal/Education/bio_work/python_project_MVZ/M3 export all.txt", "r")
reader = csv.reader(peak_data, delimiter='\t')
name = ''
for row in reader:
    # if name != row[1]:
    #     if row[7] == 'Fail':
    #         print(row[1], ': ', row[7])
    #         name = row[1]
    print(row)
