''' 
Welcome to picom 0.6! This script is a project built by Ryan Zhu (rzhu249@uwo.ca)
picom is a custom made dicom reader for Dr. Matthew Fox and Dr. Alexei Ouriadov's research labs. 

Picom 0.6 features:
    -able to view a specific slice given input
    -error handling improvements
    -improved buttons
    -renamed some variables along the way

Comments:
    -code works but is very inefficient, which needs to be changed for upcoming planned features
    -will need to build more classes
    -planning on implementing window/level sliders

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
            try:
                self.figs.append(ds.pixel_array)
            except:
                print('Incompatible File(s)')
                exit() # failsafe for inputting incompatible files
            
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

        # creates the button(s)
        fButton = plt.axes([0.1, 0.7, 0.04, 0.04])
        fwdButton = Button(fButton, '+1', hovercolor='0.975')
        bButton = plt.axes([0.1, 0.65, 0.04, 0.04])
        backButton = Button(bButton, '-1', hovercolor='0.975')
        ffButton = plt.axes([0.1, 0.75, 0.04, 0.04])
        ffwdButton = Button(ffButton, '+2', hovercolor='0.975')
        bbButton = plt.axes([0.1, 0.6, 0.04, 0.04])
        bbackButton = Button(bbButton, '-2', hovercolor='0.975') #the buttons can be optimized but later issue

        #input box
        box = plt.axes([0.07, 0.055, 0.08, 0.04])
        inputBox = TextBox(box,'Input Slice',label_pad=0.05)

        def update(val): #function for slider
            i = int(slider.val) - 1             
            img.set_data(self.figs[i])
            title.set_text(f'Slice {i+1}')
            fig.canvas.draw_idle()
        
        def nextSlice(event): #function for +1 button
            if slider.val < slider.valmax:
                slider.set_val(slider.val+1)
        def prevSlice(event): #function for -1 button
            if slider.val > slider.valmin:
                slider.set_val(slider.val-1)
        def slicePlus(event): #function for +2 button
            if slider.val < slider.valmax:
                if slider.val +2 <= slider.valmax:
                    slider.set_val(slider.val+2)
                else:
                    slider.set_val(slider.valmax) # if the value would be out of range then just set it to the max/min
        def sliceMinus(event): #function for -2 button
            if slider.val > slider.valmin:
                if slider.val -2 >= slider.valmin:
                    slider.set_val(slider.val-2)
                else:
                    slider.set_val(slider.valmin)
        
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

        slider.on_changed(update)
        fwdButton.on_clicked(nextSlice)
        backButton.on_clicked(prevSlice)
        ffwdButton.on_clicked(slicePlus)
        bbackButton.on_clicked(sliceMinus)
        inputBox.on_submit(enter)
        plt.show()
        
viewer = dicomViewer()
viewer.openFile()
viewer.readDicom()
viewer.renderPlot()
