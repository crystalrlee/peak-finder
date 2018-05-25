#!/usr/bin/env python3

# Takes in tab-deliniated .txt files with DNA peak data- generate by export all in software
# Outputs peaks of importance for M2, M3, Mgano, and Mhyme assays to .csv
from PyQt5 import QtWidgets, QtCore
import sys
import os
import csv
# How dictionary peaks_of_interest is organized:
# {
#     sample_name1:[
#         {'quality': '', 'dye': '', 'size': '', height: ''}, {}, {}
#     ],
#     sample_name2:[
#         {}, {}, {}
#     ]
# }

# This class does all the GUI stuff
class ProgramWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(ProgramWindow, self).__init__()

        self.input_filename = None
        self.output_filename = None

        # Opens and styles main window
        self.setWindowTitle('Fragment Analysis Peak Parser')
        self.show()
        self.resize(450, 200)

        # Assay dropdown
        assay_label = QtWidgets.QLabel('Choose assay: ')
        assay_dropdown = QtWidgets.QComboBox(self)
        assay_dropdown.addItem('M2')
        assay_dropdown.addItem('M3')
        assay_dropdown.addItem('Mgano')
        assay_dropdown.addItem('Mhyme')
        assay_layout = QtWidgets.QHBoxLayout()
        assay_layout.addWidget(assay_label)
        assay_layout.addWidget(assay_dropdown)
        assay_layout.addStretch()

        # Select Data File Button and Display
        load_button = QtWidgets.QPushButton('Select Data File')
        load_button.clicked.connect(self.select_data_file)
        load_button.setMinimumWidth(130)
        self.load_button_display = QtWidgets.QLineEdit()
        self.load_button_display.setEnabled(False)
        load_button_layout = QtWidgets.QHBoxLayout()
        load_button_layout.addWidget(load_button)
        load_button_layout.addWidget(self.load_button_display)

        # Save .csv File Button and Display
        save_button = QtWidgets.QPushButton('Select Save File')
        save_button.clicked.connect(self.select_save_location)
        save_button.setMinimumWidth(130)
        self.save_button_display = QtWidgets.QLineEdit()
        self.save_button_display.setEnabled(False)
        save_button_layout = QtWidgets.QHBoxLayout()
        save_button_layout.addWidget(save_button)
        save_button_layout.addWidget(self.save_button_display)

        # Populates GUI with layouts
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(assay_layout)
        layout.addLayout(load_button_layout)
        layout.addLayout(save_button_layout)

        # Main container everything goes in
        container = QtWidgets.QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Defines how save button works
    def select_data_file(self):
        filename, _filter = QtWidgets.QFileDialog.getOpenFileName(self, "Select DNA fragment data file", filter="Text files (*.txt)")
        if filename != '':
            self.input_filename = filename
            self.load_button_display.setText(os.path.basename(filename))

    # Defines how save button works
    def select_save_location(self):
        filename, _filter = QtWidgets.QFileDialog.getSaveFileName(self, "Select save file location", filter="Csv files (*.csv)")
        if filename != '':
            self.output_filename = filename
            self.save_button_display.setText(os.path.basename(filename))


# Takes all data from .txt, puts it into a dictionary called peak_data
def populate_dict(input_filename):
    peak_data = {}
    # Opens & reads a tab delineated .txt file
    data = open(input_filename, "r")
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
        # Maps sample to a dictionary of its properties
        peak_data[sample_name].append({
            'quality': row[7],
            'dye': row[11],
            'size': size,
            'height': height
        })
    return peak_data

# Looks for important peaks
def look_for_peaks(peak_data, assay, output_filename):
    # Takes data from a .txt, populates a dictionary called peaks_of_interest
    # Keys: failed samples, then name of species IDed (depending on assay)

    # Sets keys for dictionary depending on assay choice
    if assay == 'm2' or assay == 'M2':
        peaks_of_interest = {
            'Failed Sample': [],
            'Armillaria': [],
            'Hericium': [],
            'Pleurotus': [],
            'Laetiporus': []
        }
    if assay == 'm3' or assay == 'M3':
        peaks_of_interest = {
            'Failed Sample': [],
            'Schizophyllum': [],
            'Perenniporia' : [],
            'Stereum': [],
            'Trametes': []
        }
    if assay == 'Mgano' or assay == 'mgano' or assay == 'MGANO':
        peaks_of_interest = {
            'Failed Sample': [],
            'G. adspernum': [],
            'G. applanatum' : [],
            'G. lucidum': [],
            'G. resinaceum': []
        }
    if assay == 'Mhyme' or assay == 'mhyme' or assay == 'MHYME':
        peaks_of_interest= {
            'Failed Sample': [],
            'Inocutis': [],
            'Fomitiporia' : [],
            'Pseudoinonotus': [],
            'Fuscoporia': [],
            'Inonotus s.s.': [],
            'Phellinus': []
        }
    list_of_failed_samples = []

    # Iterates through .txt file, populates dictionary
    for sample in peak_data:
        for fragment in peak_data[sample]:
            # Looks for failed samples
            if fragment['quality'] == 'Fail':
                # makes sure each failed sample only listed once in .csv file
                if sample not in list_of_failed_samples:
                    peaks_of_interest['Failed Sample'].append({
                        'sample': sample,
                        'size': fragment['size'],
                        'height': fragment['height'],
                        'quality': fragment['quality']
                    })
                    list_of_failed_samples.append(sample)
            # Checks which assay you've run, and looks for species in assay
            # M2 assay
            elif assay == 'm2' or assay == 'M2':
                # Armillaria
                if fragment['dye'].startswith('B') and 183 < fragment['size'] < 187:
                    peaks_of_interest['Armillaria'].append({
                        'sample': sample,
                        'size': fragment['size'],
                        'height': fragment['height'],
                        'quality': fragment['quality']
                    })
                # Hericium
                if fragment['dye'].startswith('G') and 198 < fragment['size'] < 202:
                    peaks_of_interest['Hericium'].append({
                        'sample': sample,
                        'size': fragment['size'],
                        'height': fragment['height'],
                        'quality': fragment['quality']
                    })
                # Pleurotus
                if fragment['dye'].startswith('G') and 156 < fragment['size'] < 160:
                    peaks_of_interest['Pleurotus'].append({
                        'sample': sample,
                        'size': fragment['size'],
                        'height': fragment['height'],
                        'quality': fragment['quality']
                    })
                # Laetiporus
                if fragment['dye'].startswith('G') and 219 < fragment['size'] < 223:
                    peaks_of_interest['Laetiporus'].append({
                        'sample': sample,
                        'size': fragment['size'],
                        'height': fragment['height'],
                        'quality': fragment['quality']
                    })
            # M3 assay
            elif assay == 'm3' or assay == 'M3':
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
            # Mgano assay (Gano Derma)
            elif assay == 'Mgano' or assay == 'mgano' or assay == 'MGANO':
                    # G. adspernum
                    if fragment['dye'].startswith('B') and 209 < fragment['size'] < 213:
                        peaks_of_interest['G. adspernum'].append({
                            'sample': sample,
                            'size': fragment['size'],
                            'height': fragment['height'],
                            'quality': fragment['quality']
                        })
                    # G. applanatum
                    if fragment['dye'].startswith('B') and 198 < fragment['size'] < 202:
                        peaks_of_interest['G. applanatum'].append({
                            'sample': sample,
                            'size': fragment['size'],
                            'height': fragment['height'],
                            'quality': fragment['quality']
                        })
                    # G. lucidum
                    if fragment['dye'].startswith('B') and 191 < fragment['size'] < 195:
                        peaks_of_interest['G. lucidum'].append({
                            'sample': sample,
                            'size': fragment['size'],
                            'height': fragment['height'],
                            'quality': fragment['quality']
                        })
                    # G. resinaceum
                    if fragment['dye'].startswith('B') and 176 < fragment['size'] < 180:
                        peaks_of_interest['G. resinaceum'].append({
                            'sample': sample,
                            'size': fragment['size'],
                            'height': fragment['height'],
                            'quality': fragment['quality']
                        })
            # Mhyme assay
            elif assay == 'Mhyme' or assay == 'mhyme' or assay == 'MHYME':
                # Inocutis
                if fragment['dye'].startswith('G') and 263 < fragment['size'] < 267:
                    peaks_of_interest['Inocutis'].append({
                        'sample': sample,
                        'size': fragment['size'],
                        'height': fragment['height'],
                        'quality': fragment['quality']
                    })
                # Fomitiporia
                if fragment['dye'].startswith('G') and 256 < fragment['size'] < 260:
                    peaks_of_interest['Fomitiporia'].append({
                        'sample': sample,
                        'size': fragment['size'],
                        'height': fragment['height'],
                        'quality': fragment['quality']
                    })
                # Pseudoinonotus
                if fragment['dye'].startswith('G') and 252 < fragment['size'] < 256:
                    peaks_of_interest['Pseudoinonotus'].append({
                        'sample': sample,
                        'size': fragment['size'],
                        'height': fragment['height'],
                        'quality': fragment['quality']
                    })
                # Fuscoporia
                if fragment['dye'].startswith('G') and 223 < fragment['size'] < 227:
                    peaks_of_interest['Fuscoporia'].append({
                        'sample': sample,
                        'size': fragment['size'],
                        'height': fragment['height'],
                        'quality': fragment['quality']
                    })
                # Inonotus s.s.
                if fragment['dye'].startswith('G') and 212 < fragment['size'] < 216:
                    peaks_of_interest['Inonotus s.s.'].append({
                        'sample': sample,
                        'size': fragment['size'],
                        'height': fragment['height'],
                        'quality': fragment['quality']
                    })
                # Phellinus
                if fragment['dye'].startswith('G') and 171 < fragment['size'] < 175:
                    peaks_of_interest['Phellinus'].append({
                        'sample': sample,
                        'size': fragment['size'],
                        'height': fragment['height'],
                        'quality': fragment['quality']
                    })

    # Takes peaks_of_interest and prints it to a .csv file
    csvfile = open(output_filename, "w")
    writer = csv.writer(csvfile, delimiter='\t')
    # Writes header
    writer.writerow(['PEAK ID','SAMPLE', 'SIZE', 'HEIGHT', 'QUALITY'])
    # Writes rows
    for species in peaks_of_interest:
        for peak_dict in peaks_of_interest[species]:
            writer.writerow([species, peak_dict['sample'], peak_dict['size'], peak_dict['height'], peak_dict['quality']])

def main():
    # GUI stuff
    app = QtWidgets.QApplication(sys.argv)
    window = ProgramWindow()
    sys.exit(app.exec_())
    # Put into run button function
    # peak_data = populate_dict(input_filename)
    # look_for_peaks(peak_data, assay, output_filename)


main()
