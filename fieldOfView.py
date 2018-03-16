import tkinter as tk   # python3
import numpy as np
import os
from astropy.io import fits

class FieldOfView(object):

    def __init__(self, app, master):
        self._app = app
        self.fovCanvas = tk.Canvas(master, height=250, width=300)
        self.fovCanvas.place(relx=0.05, rely=0.1)

        self.labelfovCanvas = tk.Label(master, text="Field of View")
        self.labelfovCanvas.place(relx=0.05, rely=0.05)

        self.height=250
        self.width=300
        self.points = []
        self.lines = []
        self.axes = []
        self.borderwidth = 10
        self.axis_color = '#000'
        self.point_color = '#f00'
        self.border_color = '#000'
        self.line_color = '#00f'
        self.background_color = '#fff'

    def addAxes(self, xmin, xmax, ymin, ymax):
        self.border = self.fovCanvas.create_rectangle(xmin, -ymin, xmax, -ymax, tags='all',outline=self.border_color,fill=self.background_color)
        self.axes.append(self.fovCanvas.create_line(xmin, 0, xmax, 0, tags='all',fill=self.axis_color))
        self.axes.append(self.fovCanvas.create_line(0, -ymin, 0, -ymax, tags='all',fill=self.axis_color))

    def scaleAndCenter(self):
        # Find the scale factor from size of bounding box
        bb = self.fovCanvas.bbox('all')
        bbwidth = int(bb[2]) - int(bb[0])
        print("BBwidth 1: ", bbwidth)
        bbheight = int(bb[3]) - int(bb[1])
        print("BBheight 1: ", bbheight)
        xscale = self.width / bbwidth
        yscale = self.height / bbheight
        # Scale accordingly
        self.fovCanvas.scale('all', 0, 0, xscale, yscale)
        # Move to center the image on the canvas
        bb = self.fovCanvas.bbox('all')
        bbwidth = int(bb[2]) - int(bb[0])
        print("BBwidth 2: ", bbwidth)
        bbheight = int(bb[3]) - int(bb[1])
        print("BBheight 2: ", bbheight)
        print(xscale)
        print(yscale)
        self.fovCanvas.move('all', self.width/2, self.height/2)

    def addPoint(self, x, y):
        self.points.append(self.fovCanvas.create_oval(x, y, x, y, tags='all', fill=self.point_color))

    def plotStars(self):
        coordsX, coordsY = [], []
        i = 0
        while i < len(self._app._sInput.starTable):
            coordsX.append(self._app._sInput.starTable[i][2])
            coordsY.append(self._app._sInput.starTable[i][3])
            i += 1
        self.addAxes(min(coordsX), max(coordsX), min(coordsY), max(coordsY))
        j=0
        while j < len(coordsX):
            self.addPoint(coordsX[j], coordsY[j])
            j += 1
        self.scaleAndCenter()
        print("done")

    def createFits(self):
        # This function will create the fits file which will be shown in the Field of field of view
        # The data will be calculated using source information input by the user

        # fake data until real data can be created
        data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], np.int32)
        hdu = fits.PrimaryHDU(data)

        hdu.writeto('test.fits', overwrite=True)
