import pydicom as picom
import matplotlib.pylab as plt
import tkinter as tk
from tkinter import filedialog as fdlg

#second iteration of the picom viewer, enabling multiple files to be read simultaneously

#opens file selector
filePath = fdlg.askopenfilenames(
    title = "Select DICOM File",
    filetypes =[("DICOM Files","*.dcm *.ima")] 
)

#reads the dicom file, for all files selected and adds it to a list
slices = []
for i, n in enumerate(filePath, start=1): #simultaneously parses throught the input files and counts
    ds = picom.dcmread(n)

    #creates the image from the selected dicom file
    slice = plt.figure()
    plt.imshow(ds.pixel_array, cmap='gray')
    plt.title(f'Slice {i}')
    slices.append(slice)

plt.show()
    

