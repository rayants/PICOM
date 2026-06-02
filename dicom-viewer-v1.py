import pydicom as picom
import matplotlib.pylab as plt
import tkinter as tk
from tkinter import filedialog as fdlg

#proof of concept script that only works for single DICOM file selected

#opens file selector
filePath = fdlg.askopenfilename(
    title = "Select DICOM File",
    filetypes =[("DICOM Files","*.dcm *.ima")] 
)

#reads the dicom file
ds = picom.dcmread(filePath)

#generates and shows the image from the selected dicom file
plt.imshow(ds.pixel_array, cmap='gray')
plt.show()