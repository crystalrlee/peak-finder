# Takes in tab seperated .txt files with DNA peak data- generate by export all in software
# Outputs peaks of importance for M2, M3, Mgano, and Mhyme assays

import csv

# {
#     key1:[
#         {'quality': '', 'dye': '', 'size': '', height: ''}, {}, {}
#     ],
#     key2:[
#         {}, {}, {}
#     ]
# }

def populate_dict():
    peak_data = {}
    # Opens & reads a tab delineated .txt file
    data = open("/home/crystal/Education/bio_work/python_project_MVZ/M3 export all.txt", "r")
    reader = csv.reader(data, delimiter='\t')
    # Makes a dictionary where each sample is a key, with nested dictionaries for each row in file
    for row in reader:
        sample_name = row[1]
        if sample_name not in peak_data:
            peak_data[sample_name] = []

        peak_data[sample_name].append({
            'quality': row[7],
            'dye': row[11],
            'size': row[13],
            'height': row[14]
        })
    return peak_data

# Prints out samples that failed, removes them from sample dictionary
def check_quality(peak_data):
    failed_samples = []
    # Creates a list of samples that failed
    for sample in peak_data:
        if peak_data[sample][0]['quality'] == 'Fail':
            failed_samples.append(sample)
    print('These samples failed: \n{}'.format(failed_samples))
    # Deletes failed samples from dictionary
    for fail in failed_samples:
        del peak_data[fail]
    return peak_data

def main():
    peak_data = populate_dict()
    filtered_data = check_quality(peak_data)

    # for sample in peak_data:
    #     print('{}\n{}'.format(sample, peak_data[sample]))

main()
