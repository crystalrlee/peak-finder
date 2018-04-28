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
    next(reader, None) # skips the header line
    for row in reader:
        # Sets each sample as a key
        sample_name = row[1]
        if sample_name not in peak_data:
            peak_data[sample_name] = []
        # Converts size and height data to floats
        try:
            size = float(row[13])
        except:
            size = 0
        try:
            height = float(row[14])
        except:
            height = 0
        # Maps sample to a dicitonary of it's properties
        peak_data[sample_name].append({
            'quality': row[7],
            'dye': row[11],
            'size': size,
            'height': height
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

# Looks for important peaks
def look_for_peaks(filtered_data):
    # Checks for M3 peaks
    M3 = []
    for sample in filtered_data:
        for fragment in filtered_data[sample]:
            if fragment['dye'].startswith('B') and 188 < fragment['size'] < 192:
                print('Sample {} has a peak at size {} with height {}.'.format(sample, fragment['size'], fragment['height']))

def main():
    peak_data = populate_dict()
    filtered_data = check_quality(peak_data)
    look_for_peaks(filtered_data)

    # for sample in peak_data:
    #     print('{}\n{}'.format(sample, peak_data[sample]))

main()
