import pydicom as picom
import matplotlib.pylab as plt
import tkinter as tk
from tkinter import filedialog as fdlg
from matplotlib.widgets import Slider

#third iteration of the picom viewer that enables rapid switching of the slice view

#opens file selector
filePath = fdlg.askopenfilenames(
    title = "Select DICOM File",
    filetypes =[("*.dcm, *.ima","*.dcm *.ima")] 
)

#reads dicom files and adds it to a list
figs = []
for n in filePath:
    ds = picom.dcmread(n)
    figs.append(ds.pixel_array)

#setup figures for each slice
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2, left=-0.15)
index = 0 # used for indexing each slice
img = ax.imshow(figs[index], cmap = 'gray')
title = ax.set_title(f'Slice {index + 1}')
cbar = fig.colorbar(img)
cbar.set_label("Brightness", loc='top')

#slider axis
ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])
slider = Slider(ax_slider, 'SLICE', 1, len(figs), valinit=1, valstep=1)

#update function
def update(val):
    i = int(slider.val) - 1             
    img.set_data(figs[i])
    title.set_text(f'Slice {i+1}')
    fig.canvas.draw_idle()

slider.on_changed(update)
#show final plot(s)
plt.show()
    

