''' 
Welcome to picom 0.5! This script is a project built by Ryan Zhu (rzhu249@uwo.ca)
picom is a custom made dicom reader for Dr. Matthew Fox and Dr. Alexei Ouriadov's research labs. 

Picom 0.5 features:
    -introduces description at the top of the file
    -code now exits when no files are selected
    -image slice slider
    -introduces basic buttons for +/- scrolling through slices

'''

import numpy as np #numpy isn't used yet
import pydicom as picom
import matplotlib.pylab as plt
import tkinter as tk
from tkinter import filedialog as fdlg
from matplotlib.widgets import Button, Slider, TextBox

class dicomViewer:
    def __init__(self):
        self.figs = []
        self.filePath = []
        
    def openFile(self):
        self.filePath = fdlg.askopenfilenames( #opens the files through file explorer
            title = "Select DICOM File",
            filetypes =[("*.dcm, *.ima","*.dcm *.ima")] 
            )
        if not self.filePath: # failsafe to prevent errors when you don't input files
            print('No File(s) Selected')
            self.openFile = False
            exit()

    def readDicom(self):
        for i,n in enumerate(self.filePath): #uses enumerate to determine number of slices
            ds = picom.dcmread(n)
            self.figs.append(ds.pixel_array)
            
        print(f'Received {i+1} Slices')

    def createSubplots(self):
        index = 0 # used for indexing
        fig, ax = plt.subplots() # creates the subplot
        plt.subplots_adjust(bottom=0.15, left=-0.1) # adjusts the positioning
        img = ax.imshow(self.figs[index], cmap = 'gray') #displays the image
        title = ax.set_title(f'Slice {index + 1}')
        cbar = fig.colorbar(img)
        cbar.set_label("Brightness", loc='top')
        
        # creates the slider
        ax_slider = plt.axes([0.2, 0.05, 0.6, 0.05])
        slider = Slider(ax_slider, 
                        'SLICE', 
                        valmin=1, 
                        valmax=len(self.figs), 
                        valinit=1, 
                        valstep=1) # slider config

        # creates the button(s)
        fButton = plt.axes([0.1, 0.7, 0.04, 0.04])
        fwdButton = Button(fButton, '+1', hovercolor='0.975')
        bButton = plt.axes([0.1, 0.65, 0.04, 0.04])
        backButton = Button(bButton, '-1', hovercolor='0.975')

        def update(val): #function for slider
            i = int(slider.val) - 1             
            img.set_data(self.figs[i])
            title.set_text(f'Slice {i+1}')

        def nextSlice(event): #function for +1 slice
            if slider.val < slider.valmax:
                slider.set_val(slider.val+1)
            else:
                pass

        def prevSlice(event): #function for -1 slice
            if slider.val > slider.valmin:
                slider.set_val(slider.val-1)
            else:
                pass

        slider.on_changed(update)
        fwdButton.on_clicked(nextSlice)
        backButton.on_clicked(prevSlice)
        plt.show()

viewer = dicomViewer()
viewer.openFile()
viewer.readDicom()
viewer.createSubplots()