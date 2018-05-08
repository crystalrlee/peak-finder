#!/usr/bin/env python3

# Takes in tab seperated .txt files with DNA peak data- generate by export all in software
# Outputs peaks of importance for M2, M3, Mgano, and Mhyme assays to .csv

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
        # Maps sample to a dictionary of it's properties
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
    print('\nThese samples failed: \n{}\n'.format(failed_samples))
    # Deletes failed samples from dictionary
    for fail in failed_samples:
        del peak_data[fail]
    return peak_data

# Looks for important peaks
def look_for_peaks(filtered_data):
    # M3 peaks
    possible_id = {
        'Failed Sample': [],
        'Schizophyllum': [],
        'Perenniporia': [],
        'Stereum': [],
        'Trametes': []
    }
    # Populates a dictionary called possible_id with M3 found peak data
    for sample in filtered_data:
        for fragment in filtered_data[sample]:
            # Schizophyllum
            if fragment['dye'].startswith('B') and 188 < fragment['size'] < 192:
                possible_id['Schizophyllum'].append({
                    'sample': sample,
                    'size': fragment['size'],
                    'height': fragment['height'],
                    'quality': fragment['quality']
                })
            # Perenniporia
            if fragment['dye'].startswith('B') and 150 < fragment['size'] < 154:
                possible_id['Perenniporia'].append({
                    'sample': sample,
                    'size': fragment['size'],
                    'height': fragment['height'],
                    'quality': fragment['quality']
                })
            # Stereum
            if fragment['dye'].startswith('B') and 231 < fragment['size'] < 236 or fragment['dye'].startswith('B') and 241 < fragment['size'] < 245:
                possible_id['Stereum'].append({
                    'sample': sample,
                    'size': fragment['size'],
                    'height': fragment['height'],
                    'quality': fragment['quality']
                })
            # Trametes
            if fragment['dye'].startswith('G') and 219 < fragment['size'] < 223:
                possible_id['Trametes'].append({
                    'sample': sample,
                    'size': fragment['size'],
                    'height': fragment['height'],
                    'quality': fragment['quality']
                })
    # Takes possible_id and prints it to a .csv file
    csvfile = open("/home/crystal/Education/bio_work/python_project_MVZ/m3-python-peaks.csv", "w")
    writer = csv.writer(csvfile, delimiter='\t')
    # Writes header
    writer.writerow(['PEAK ID','SAMPLE', 'SIZE', 'HEIGHT', 'QUALITY'])
    # Writes rows
    for species in possible_id:
        for peak_dict in possible_id[species]:
            writer.writerow([species, peak_dict['sample'], peak_dict['size'], peak_dict['height'], peak_dict['quality']])

def main():
    peak_data = populate_dict()
    filtered_data = check_quality(peak_data)
    look_for_peaks(filtered_data)

main()
