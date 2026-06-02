# 4th iteration cleans up the code into a class
import numpy as np
import pydicom as picom
import matplotlib.pylab as plt
import tkinter as tk
from tkinter import filedialog as fdlg
from matplotlib.widgets import Button, Slider

class dicomViewer:
    def __init__(self):
        self.figs = []
        self.filePath = []
        
    def openFile(self):
        self.filePath = fdlg.askopenfilenames(
        title = "Select DICOM File",
        filetypes =[("*.dcm, *.ima","*.dcm *.ima")] 
        )
        if not self.filePath:
            print('No Files Selected')
            pass

    def readDicom(self):
        for i,n in enumerate(self.filePath):
            ds = picom.dcmread(n)
            self.figs.append(ds.pixel_array)
            
        print(f'Received {i+1} Slices')

    def createSubplots(self):
        index = 0 # used for labelling
        fig, ax = plt.subplots()    # creates the subplot
        plt.subplots_adjust(bottom=0.15, left=-0.1) # adjusts the positioning
        img = ax.imshow(self.figs[index], cmap = 'gray')
        title = ax.set_title(f'Slice {index + 1}')
        cbar = fig.colorbar(img)
        cbar.set_label("Brightness", loc='top')
        
        # creates the slider
        ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
        slider = Slider(ax_slider, 'SLICE', 1, len(self.figs), valinit=1, valstep=1)

        def update(val):
            i = int(slider.val) - 1             
            img.set_data(self.figs[i])
            title.set_text(f'Slice {i+1}')
            
        slider.on_changed(update)
        plt.show()

viewer = dicomViewer()
viewer.openFile()
viewer.readDicom()
viewer.createSubplots()

