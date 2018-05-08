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


# Looks for important peaks
def look_for_peaks(peak_data):
    # Populates a dictionary called peaks_of_interest with peaks of interest.
    # Keys organize failed samples into one list, and the other lists are possible
    # species identifications

    # M3 peaks
    peaks_of_interest = {
        'Failed Sample': [],
        'Schizophyllum': [],
        'Perenniporia': [],
        'Stereum': [],
        'Trametes': []
    }
    # Empty list to hold failed sample names
    list_of_failed_samples = []
    # Populates a dictionary called peaks_of_interest with M3 found peak data
    for sample in peak_data:
        for fragment in peak_data[sample]:
            # Looks for failed samples
            if fragment['quality'] == 'Fail':
                if sample not in list_of_failed_samples:
                    peaks_of_interest['Failed Sample'].append({
                        'sample': sample,
                        'size': fragment['size'],
                        'height': fragment['height'],
                        'quality': fragment['quality']
                    })
                    list_of_failed_samples.append(sample)

            # Schizophyllum
            if fragment['dye'].startswith('B') and 188 < fragment['size'] < 192:
                peaks_of_interest['Schizophyllum'].append({
                    'sample': sample,
                    'size': fragment['size'],
                    'height': fragment['height'],
                    'quality': fragment['quality']
                })
            # Perenniporia
            if fragment['dye'].startswith('B') and 150 < fragment['size'] < 154:
                peaks_of_interest['Perenniporia'].append({
                    'sample': sample,
                    'size': fragment['size'],
                    'height': fragment['height'],
                    'quality': fragment['quality']
                })
            # Stereum
            if fragment['dye'].startswith('B') and 231 < fragment['size'] < 236 or fragment['dye'].startswith('B') and 241 < fragment['size'] < 245:
                peaks_of_interest['Stereum'].append({
                    'sample': sample,
                    'size': fragment['size'],
                    'height': fragment['height'],
                    'quality': fragment['quality']
                })
            # Trametes
            if fragment['dye'].startswith('G') and 219 < fragment['size'] < 223:
                peaks_of_interest['Trametes'].append({
                    'sample': sample,
                    'size': fragment['size'],
                    'height': fragment['height'],
                    'quality': fragment['quality']
                })
    # Takes peaks_of_interest and prints it to a .csv file
    csvfile = open("/home/crystal/Education/bio_work/python_project_MVZ/m3-python-peaks_quality2.csv", "w")
    writer = csv.writer(csvfile, delimiter='\t')
    # Writes header
    writer.writerow(['PEAK ID','SAMPLE', 'SIZE', 'HEIGHT', 'QUALITY'])
    # Writes rows
    for species in peaks_of_interest:
        for peak_dict in peaks_of_interest[species]:
            writer.writerow([species, peak_dict['sample'], peak_dict['size'], peak_dict['height'], peak_dict['quality']])

    print(list_of_failed_samples)
def main():
    peak_data = populate_dict()
    look_for_peaks(peak_data)

main()
