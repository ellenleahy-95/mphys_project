import tkinter as tk   # python3
import numpy as np
import os
from astropy.io import fits
from astropy.convolution import convolve, Gaussian2DKernel, Tophat2DKernel
from astropy.modeling.models import Gaussian2D

class FieldOfView(object):

    def __init__(self, app, master):
        self._app = app
        self.fovCanvas = tk.Canvas(master, height=300, width=400)
        self.fovCanvas.place(relx=0.05, rely=0.11)

        self.labelFovCanvas = tk.Label(master, text="Field of View")
        self.labelFovCanvas.place(relx=0.05, rely=0.05)

        self.height=275
        self.width=275
        self.points = []
        self.borderwidth = 10
        self.axis_color = '#000'
        self.point_color = '#f00'
        self.border_color = '#000'
        self.line_color = '#00f'
        self.background_color = '#fff'

        self.coordsX = []
        self.coordsY = []

    def addBorder(self, xmin, xmax, ymin, ymax):
        self.border = self.fovCanvas.create_rectangle(-xmin, -ymin, xmax, ymax, tags='all',outline=self.border_color,fill=self.background_color)

    def scaleAndCenter(self):
        # Find the scale factor from size of bounding box
        bb = self.fovCanvas.bbox('all')
        bbwidth = bb[2] - bb[0]
        bbheight = bb[3] - bb[1]
        while((bbheight < self.height-1 or bbheight > self.height+1) and (bbwidth < self.width-1 or bbwidth > self.width+1)):
            xscale = self.width / bbwidth
            yscale = self.height / bbheight
            # Scale accordingly
            self.fovCanvas.scale('all', 0, 0, xscale, yscale)
            bb = self.fovCanvas.bbox('all')
            bbwidth = bb[2] - bb[0]
            bbheight = bb[3] - bb[1]

        # Move to center the image on the canvas
        self.fovCanvas.move('all', self.width/1.5, self.height/1.7)

    def addPoint(self, x, y):
        self.points.append(self.fovCanvas.create_oval(x, y, x, y, tags='all', fill=self.point_color))

    def plotStars(self, size):
        i = 0
        while i < len(self._app._sInput.starTable):
            self.coordsX.append(self._app._sInput.starTable[i]["XCoord"])
            self.coordsY.append(self._app._sInput.starTable[i]["YCoord"])
            i += 1

        self.addBorder(size/2*1.1, size/2*1.1, size/2*1.1, size/2*1.1)
        j=0
        while j < len(self.coordsX):
            self.addPoint(self.coordsX[j], self.coordsY[j])
            j += 1
        self.scaleAndCenter()

    def createFrame(self, size, time):
        unit = 100
        frame = np.zeros((unit, unit))
        newX = []
        newY = []
        for value in self.coordsX:
            value += size/2
            newX.append(value)
        for value in self.coordsY:
            value += size/2
            newY.append(value)
        segmentSize = size/unit
        i = 0
        while i < len(newX):
            self.addFluxes(frame, segmentSize, size, i, newX, newY, time)
            i += 1
        return frame


    def addFluxes(self, frame, segmentSize, size, star, xVals, yVals, time):
        Xsegment = 0
        Ysegment = size
        k = 0
        while Xsegment <= size:
            j = 0
            if xVals[star] >= Xsegment and xVals[star] < Xsegment + segmentSize:
                while Ysegment >= 0:
                    if yVals[star] <= Ysegment and yVals[star] > Ysegment - segmentSize:
                        frame[k][j] += 100 * self.inputStarFlux(star, time)
                    j += 1
                    Ysegment -= segmentSize
            k += 1
            Ysegment = Ysegment
            Xsegment += segmentSize

    def inputStarFlux(self, star, time):
        return self._app._sInput.starTable[star]["flux" + str(time)]

    def createFits(self, size, beamSize):
        # This function will create the fits file which will be shown in the Field of field of view
        frames = []
        time = 1
        while time <= len(self._app._timeInput.timeValues):
            frame = self.createFrame(size, time)
            frames.append(frame)
            time += 1
        data = np.array(frames, np.int32)
        convolvedData = self.convolveFits(data, beamSize, size)
        hdu = fits.PrimaryHDU(convolvedData)

        hdu.writeto('test_new.fits', overwrite=True)

    def convolveFits(self, fitsData, beamSize, size):
        convolvedData = []
        pixelSize = size/100
        beamPixel = beamSize/pixelSize
        gauss_kernel = Gaussian2DKernel(beamPixel)
        for frame in fitsData:
            smoothed_data_gauss = convolve(frame, gauss_kernel)
            convolvedData.append(smoothed_data_gauss)
        return convolvedData

    def clear(self):
        self.fovCanvas.delete('all')
