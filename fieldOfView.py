import tkinter as tk   # python3
import numpy as np
import os
from astropy.io import fits
from astropy.convolution import convolve, Gaussian2DKernel, Tophat2DKernel
from astropy.modeling.models import Gaussian2D
#Set up matplotlib and use set of plot parameters
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.wcs import WCS
plt.style.use(astropy_mpl_style)

from astropy.utils.data import get_pkg_data_filename

import PIL
from PIL import Image

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
        self.point_color = '#fff'
        self.border_color = '#000'
        self.line_color = '#00f'
        self.background_color = '#fff'

        self.coordsX = []
        self.coordsY = []

    def addBorder(self, xmin, xmax, ymin, ymax):
        self.border = self.fovCanvas.create_rectangle(-xmin, -ymin, xmax, ymax, tags='border',outline=self.border_color)

    def scaleAndCenter(self):
        # Find the scale factor from size of bounding box
        bb = self.fovCanvas.bbox('plot')
        bbwidth = bb[2] - bb[0]
        bbheight = bb[3] - bb[1]
        while((bbheight < self.height-1 or bbheight > self.height+1) and (bbwidth < self.width-1 or bbwidth > self.width+1)):
            xscale = self.width / bbwidth
            yscale = self.height / bbheight
            # Scale accordingly
            self.fovCanvas.scale('plot', 0, 0, xscale, yscale)
            self.fovCanvas.scale('border', 0, 0, xscale, yscale)
            bb = self.fovCanvas.bbox('border')
            bbwidth = bb[2] - bb[0]
            bbheight = bb[3] - bb[1]

        # Move to center the image on the canvas

        self.fovCanvas.scale('border', 0, 0, 1.05, 1.05)
        self.fovCanvas.move('all', self.width/2*1.1, self.height/2*1.1)
        

    def addPoint(self, x, y, star, size):
        tag = "star" + str(star)
        self.points.append(self.fovCanvas.create_oval(x-(size/100), y+(size/100), x+(size/100), y-(size/100), tags=('plot',tag), fill=self.border_color, activefill=self.point_color))
        callback = lambda event, tag=tag: self.onStarClick(event, tag)
        self.fovCanvas.tag_bind(tag, '<Button-1>', callback)

    def onStarClick(self, event, tag):
        star = tag[4:]
        self._app._lCurve.plotLightCurve(int(star))

#Coordinates obtained from random function extracted from 'starTable'
    def getCoords(self, size):
        i = 0
        while i < len(self._app._sInput.starTable):
            self.coordsX.append(self._app._sInput.starTable[i]["XCoord"])
            self.coordsY.append(self._app._sInput.starTable[i]["YCoord"])
            i += 1

    def plotStars(self, size):

        self.addBorder(size/2, size/2, size/2, size/2)
        j=0
        while j < len(self.coordsX):
            self.addPoint(self.coordsX[j], self.coordsY[j], j, size)
            j += 1
        self.scaleAndCenter()

    def createFrame(self, size, time, unitSize):
        frame = np.zeros((unitSize, unitSize))
        newX = []
        newY = []
        for value in self.coordsX:
            value += size/2
            newX.append(value)
        for value in self.coordsY:
            value += size/2
            newY.append(value)
        segmentSize = size/unitSize
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
        #Resolution of fits file is set so that there are 8 pixels across the beam width
        unitSize = size * 4/beamSize
        time = 1
        while time <= len(self._app._timeInput.timeValues):
            frame = self.createFrame(size, time, int(unitSize))
            frames.append(frame)
            time += 1
        data = np.array(frames, np.int32)
        convolvedData = self.convolveFits(data, beamSize, size, int(unitSize))
        hdu = fits.PrimaryHDU(convolvedData)

        hdu.writeto('test.fits', overwrite=True)


        #This function convolves the model points with a gaussian of width corresponding to the user input beam width
    def convolveFits(self, fitsData, beamSize, size, unitSize):
        convolvedData = []
        pixelSize = size/unitSize
        beamPixel = beamSize/pixelSize
        gauss_kernel = Gaussian2DKernel(beamPixel)
        for frame in fitsData:
            smoothed_data_gauss = convolve(frame, gauss_kernel)
            convolvedData.append(smoothed_data_gauss)
        return convolvedData

    def plotImage(self, size):
   
        #Open the fits file created
        hdu_list = fits.open('test.fits', memmap=True)
        
        scidata = hdu_list[0].data

        hdu_list.close()
        image_data = scidata[0,:,:]
        image_data = image_data.T

        plt.imsave("tempimgfile.png", image_data, cmap= "autumn", origin="lower")
        #Resize image to fit canvas
        img = Image.open("tempimgfile.png")
        wpercent = (self.width/ float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((self.width, hsize), PIL.Image.ANTIALIAS)
        img.save("resized_image.png")

        hold = tk.PhotoImage(file="resized_image.png")
        #Put image in to canvas
        self.fovCanvas.create_image(0, 0, image=hold, anchor ='center')

        #Plot stars over image and scale and center them
        self.plotStars(size)

    def clear(self):
        self.fovCanvas.delete('all')
