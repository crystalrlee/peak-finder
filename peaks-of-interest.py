"""
Peaks of Interest

Copyright (c) 2018 Crystal Lee <crystalmayerlee@berkeley.edu>

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:
The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

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
        self.setWindowTitle('Peaks of Interest')
        self.show()
        self.resize(450, 180)

        # Assay dropdown
        assay_label = QtWidgets.QLabel('Choose assay: ')
        self.assay_dropdown = QtWidgets.QComboBox(self)
        self.assay_dropdown.addItem('M2')
        self.assay_dropdown.addItem('M3')
        self.assay_dropdown.addItem('Mgano')
        self.assay_dropdown.addItem('Mhyme')
        assay_layout = QtWidgets.QHBoxLayout()
        assay_layout.addWidget(assay_label)
        assay_layout.addWidget(self.assay_dropdown)
        assay_layout.addStretch()
        # In case user wants default assay and doesn't click on dropdown
        self.assay_choice = str(self.assay_dropdown.currentText())
        # Handles choices
        self.assay_dropdown.currentIndexChanged.connect(self.choose_assay)

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

        # Run Button
        self.run_button = QtWidgets.QPushButton('Run')
        self.run_button.setEnabled(False)
        self.run_button.clicked.connect(self.run_program)

        # Status Bar (to display when files are saved)
        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.setSizeGripEnabled (True)

        # Populates GUI with layouts
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(assay_layout)
        layout.addLayout(load_button_layout)
        layout.addLayout(save_button_layout)
        layout.addWidget(self.run_button)

        # Main container everything goes in
        container = QtWidgets.QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Makes dropdown work
    def choose_assay(self):
        self.assay_choice = str(self.assay_dropdown.currentText())

    # Makes save button work
    def select_data_file(self):
        filename, _filter = QtWidgets.QFileDialog.getOpenFileName(self, "Select DNA fragment data file", filter="Text files (*.txt)")
        if filename != '':
            self.input_filename = filename
            self.load_button_display.setText(os.path.basename(filename))
        # Enables run button if both files are set
        if self.input_filename != None and self.output_filename != None:
            self.run_button.setEnabled(True)

    # Defines how save button works
    def select_save_location(self):
        filename, _filter = QtWidgets.QFileDialog.getSaveFileName(self, "Select save file location", filter="Csv files (*.csv)")
        if filename != '':
            self.output_filename = filename
            self.save_button_display.setText(os.path.basename(filename))
        # Enables run button if both files are set
        if self.input_filename != None and self.output_filename != None:
            self.run_button.setEnabled(True)

    # Run program button
    def run_program(self):
        if self.input_filename != '' and self.output_filename != '':
            try:
                assay = self.assay_choice
                peak_data = populate_dict(self.input_filename)
                look_for_peaks(peak_data, assay, self.output_filename)
                # Displays a status saying file is saved
                self.setStatusBar(self.status_bar)
                self.status_bar.showMessage('File has been saved to {}'.format(self.output_filename))
            except:
                # Displays error
                self.setStatusBar(self.status_bar)
                self.status_bar.showMessage('Error. Make sure files are correct.')

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
    if assay == 'M2':
        peaks_of_interest = {
            'Failed Sample': [],
            'Armillaria': [],
            'Hericium': [],
            'Pleurotus': [],
            'Laetiporus': []
        }
    if assay == 'M3':
        peaks_of_interest = {
            'Failed Sample': [],
            'Schizophyllum': [],
            'Perenniporia' : [],
            'Stereum': [],
            'Trametes': []
        }
    if assay == 'Mgano':
        peaks_of_interest = {
            'Failed Sample': [],
            'G. adspernum': [],
            'G. applanatum' : [],
            'G. lucidum': [],
            'G. resinaceum': []
        }
    if assay == 'Mhyme':
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
            elif assay == 'M2':
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
            elif assay == 'M3':
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
            elif assay == 'Mgano':
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
            elif assay == 'Mhyme':
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
    app = QtWidgets.QApplication(sys.argv) # Starts GUI code
    window = ProgramWindow() # Opens GUI window
    sys.exit(app.exec_()) # Exits GUI program

main()
