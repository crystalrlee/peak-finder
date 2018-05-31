# Peaks of Interest
Automated peak finder for fragment analysis data from Peak Scanner program using assays. 

## Setting up a Windows development/run environment

### Step 1: Download GitHub files
Go to https://github.com/crystalrlee/peak-finder. Click on the green button that says "Clone or download", 
and click on Download ZIP. Extract ZIP file to wherever you want the program on your computer.  

### Step 2: Install Python 3. 
Go to https://www.python.org/downloads, and download Python 3.6.5. Run installer. 
Make sure to tick the box that says "Add Python 3.6 to PATH."

### Step 3: Install PyQt 
Open a command prompt, and cd to the peak-finder folder you extracted from Github. Install dependencies by running this code:
```sh
pip3 install PyQt5
```
### Step 4: Install Qt
Go to https://www1.qt.io/offline-installers/ and click on Qt 5.11.0 for Windows(2.4GB). Run installer. You do not need a Qt account,
just press the "skip" button when it asks for account info. Install Qt.

## Using the Program
Process data using Peak Scanner. Export as "Export Combined Table". Click on .bat file "run" in folder containing Peaks of Interest python code. Choose assay, data file, and save file. Click Run. If any error occurs in program status bar will output an error, saying that the user should check files. 
