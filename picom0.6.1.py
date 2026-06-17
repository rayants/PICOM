''' 
Welcome to picom 0.6.1! This script is a project built by Ryan Zhu (rzhu249@uwo.ca)
picom is a custom made dicom reader for Dr. Matthew Fox and Dr. Alexei Ouriadov's research labs. 

Picom 0.6.1 features:
    -able to view a specific slice given input  
    -button code revamped (ryan is happy now)

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
            exit()

    def readDicom(self):
        for i,n in enumerate(self.filePath): #uses enumerate to determine number of slices
            ds = picom.dcmread(n)
            self.figs.append(ds.pixel_array)
            
        print(f'Received {i+1} Slices')

    def renderPlot(self):
        index = 0 # used for indexing
        fig, ax = plt.subplots() # creates the subplot
        plt.subplots_adjust(bottom=0.15, left=-0.1) # adjusts the positioning
        img = ax.imshow(self.figs[index], cmap = 'gray') #displays the image
        title = ax.set_title(f'Slice {index + 1}')
        cbar = fig.colorbar(img)
        cbar.set_label("Brightness", loc='top')
        
        # creates the slider
        ax_slider = plt.axes([0.2, 0.05, 0.6, 0.05])
        slider = Slider(ax_slider,'SLICE',valmin=1,valmax=len(self.figs),valinit=1,valstep=1) # slider config
     
        def update(val): #function for slider
            i = int(slider.val) - 1             
            img.set_data(self.figs[i])
            title.set_text(f'Slice {i+1}')
            fig.canvas.draw_idle()
        slider.on_changed(update)

        #refined buttons (rewrites it into list of tuples)
        buttonConfigs = [('+2',0.75),('+1',0.7),('-1',0.65),('-2',0.6)]
        buttons = []

        for x,y in buttonConfigs:
            btn_ax = plt.axes([.1, y, 0.04, 0.04])
            buttons.append(Button(btn_ax, x,hovercolor='0.975'))
        
        def buttonFunc(event): # single unified button function to scroll between slices
            for button in buttons:
                if button.ax == event.inaxes:
                    mod = int(button.label.get_text()) #named mod for modifier
                    val = slider.val
                    if slider.valmin < val+mod < slider.valmax: #if the modifier is within acceptable ranges then it will work
                        slider.set_val(val+mod)
                    elif val+mod <= slider.valmin: #if modifier touches min or max, set it to the respective min/max
                        slider.set_val(slider.valmin)
                    elif val+mod >= slider.valmax:
                        slider.set_val(slider.valmax)               
        
        for button in buttons:
            button.on_clicked(buttonFunc)

        #input box for slice selector
        box = plt.axes([0.07, 0.055, 0.08, 0.04])
        inputBox = TextBox(box,'Input Slice',label_pad=0.05)
        
        def enter(text): #selects a specific slice in the dataset
                    if text =='':
                        return
                    try:
                        sliceNum = int(text)
                        if slider.valmin <= sliceNum <= slider.valmax:
                            slider.set_val(sliceNum)        
                        else:
                            print('Number out of range') 
                    except:
                        print('Please Input an Integer') #if anything other than a number is input, this will scold you 
                    finally:
                        inputBox.set_val('')
        inputBox.on_submit(enter)
        
        plt.show()



viewer = dicomViewer()
viewer.openFile()
viewer.readDicom()
viewer.renderPlot()