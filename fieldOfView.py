import tkinter as tk   # python3
import numpy as np
import os
from astropy.io import fits
from astropy.convolution import convolve, Gaussian2DKernel, Tophat2DKernel
from astropy.modeling.models import Gaussian2D
from astropy.visualization import astropy_mpl_style
import matplotlib.pyplot as plt
from PIL import Image

class FieldOfView(object):

    def __init__(self, app, master):
        self._app = app
        # set up the total field of view canvas
        self.fovCanvas = tk.Canvas(master, height=300, width=400)
        self.fovCanvas.place(relx=0.05, rely=0.48)

        # parameters which will be used when the field of view is drawn onto the canvas
        self.height=275
        self.width=275
        self.points = []
        self.borderwidth = 10
        self.axis_color = '#000'
        self.point_color = '#fff'
        self.border_color = '#000'
        self.line_color = '#00f'
        self.background_color = '#fff'

        # make arrays for coordinates so easy to access
        self.coordsX = []
        self.coordsY = []

    def addBorder(self, xmin, xmax, ymin, ymax):
        self.border = self.fovCanvas.create_rectangle(-xmin, -ymin, xmax, ymax, tags='border',outline=self.border_color)

    def scaleAndCenter(self):
        # Find the scale factor from size of bounding box
        bb = self.fovCanvas.bbox('plot')
        # Finds the width and height of the box using the edge points
        bbwidth = bb[2] - bb[0]
        bbheight = bb[3] - bb[1]
        # Loop over scaling until the height and width is close to what we want
        while((bbheight < self.height-1 or bbheight > self.height+1) and (bbwidth < self.width-1 or bbwidth > self.width+1)):
            xscale = self.width / bbwidth
            yscale = self.height / bbheight
            # Scale using scale factors given
            self.fovCanvas.scale('plot', 0, 0, xscale, yscale)
            self.fovCanvas.scale('border', 0, 0, xscale, yscale)
            self.fovCanvas.scale("field", 0, 0, xscale, yscale)
            bb = self.fovCanvas.bbox('border')
            bbwidth = bb[2] - bb[0]
            bbheight = bb[3] - bb[1]
        # Move to center the image on the canvas
        self.fovCanvas.scale('border', 0, 0, 1.05, 1.05)
        self.fovCanvas.move('all', self.width/2*1.1, self.height/2*1.1)


    def addPoint(self, x, y, star, size):
        # add tag to star so we know which number it is later
        tag = "star" + str(star)
        self.points.append(self.fovCanvas.create_oval(x-(size/100), y+(size/100), x+(size/100), y-(size/100), tags=('plot',tag), fill=self.border_color, activefill=self.point_color))
        # Bind a click event to a star
        callback = lambda event, tag=tag: self.onStarClick(event, tag)
        self.fovCanvas.tag_bind(tag, '<Button-1>', callback)

    def onStarClick(self, event, tag):
        # strip the word star off the tag and plot the light curve for that number
        star = tag[4:]
        self._app._lCurve.plotLightCurve(int(star))

    def getCoords(self, size):
        # gets the x and y coordinates for all stars
        i = 0
        while i < len(self._app._sInput.starTable):
            self.coordsX.append(self._app._sInput.starTable[i]["XCoord"])
            self.coordsY.append(self._app._sInput.starTable[i]["YCoord"])
            i += 1

    def plotStars(self, size):
        # Adds the border around the stars
        self.addBorder(size/2, size/2, size/2, size/2)
        #Add field of view box
        self.drawField()
        j=0
        while j < len(self.coordsX):
            # Plots each stellar point
            self.addPoint(self.coordsX[j], self.coordsY[j], j, size)
            j += 1
        self.scaleAndCenter()

    def createFits(self, size, beamSize):
        # This function will create the fits file which will be shown in the Field of field of view
        frames = []
        # Resolution of fits file is set so that there are 8 pixels across the beam width
        unitSize = size * 4/beamSize
        time = 1
        # Loop through time file and create a fram for each time
        while time <= len(self._app._timeInput.timeValues):
            frame = self.createFrame(size, time, int(unitSize))
            frames.append(frame)
            time += 1
        # Put all the frames into one big array and convolve with beam
        data = np.array(frames, np.int32)
        convolvedData = self.convolveFits(data, beamSize, size, int(unitSize))
        hdu = fits.PrimaryHDU(convolvedData)

        hdu.writeto('test.fits', overwrite=True)

    def createFrame(self, size, time, unitSize):
        # Creates the frame for the fits file
        frame = np.zeros((unitSize, unitSize))
        newX = []
        newY = []
        # making all x and y values positive
        for value in self.coordsX:
            value += size/2
            newX.append(value)
        for value in self.coordsY:
            value += size/2
            newY.append(value)
        segmentSize = size/unitSize
        i = 0
        # Adds the flux for each star in that time where is relevent
        while i < len(newX):
            self.addFluxes(frame, segmentSize, size, i, newX, newY, time)
            i += 1
        return frame


    def addFluxes(self, frame, segmentSize, size, star, xVals, yVals, time):
        # Addding fluxes to a box where that star shows fluxes
        # star at top corner, y is a max and x is a min
        Xsegment = 0
        Ysegment = size
        k = 0
        # loop over each segment and add the flux
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
        # gets the flux for that star at the required time
        return self._app._sInput.starTable[star]["flux" + str(time)]

    def convolveFits(self, fitsData, beamSize, size, unitSize):
        # This function convolves the model points with a gaussian of width corresponding to the user input beam width
        convolvedData = []
        pixelSize = size/unitSize
        # find the number of pixels across a beam
        beamPixel = beamSize/pixelSize
        # creates a gaussian to convolve with the point
        gauss_kernel = Gaussian2DKernel(beamPixel)
        for frame in fitsData:
            # does the convolution
            smoothed_data_gauss = convolve(frame, gauss_kernel)
            convolvedData.append(smoothed_data_gauss)
        return convolvedData

    def plotImage(self, time):
        """Plots the image on the field of FieldOfView
        Should do this before points are plot so that points appear on top"""
        results = self._app._inputboxes.getInput()
        size = results["skySize"]

        # Open the fits file created, read in data and close file
        hdu_list = fits.open('test.fits', memmap=True)
        scidata = hdu_list[0].data
        hdu_list.close()

        image_data = scidata[int(time),:,:]
        image_data = image_data.T  # Image_data is transposed to match with points plotted on canvas
        # Saves the plot as temporary file, and sets the colourmap
        plt.imsave("tempimgfile.png", image_data, cmap= "Spectral", origin="lower")
        # Resize image to fit canvas
        img = Image.open("tempimgfile.png")
        wpercent = (self.width/ float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((self.width, hsize), Image.ANTIALIAS)
        img.save("resized_image.gif")

        hold = tk.PhotoImage(file="resized_image.gif")
        label = tk.Label(image=hold)
        label.image = hold # keep a reference
        # Put image in to canvas
        self.fovCanvas.create_image(0, 0, image=hold, anchor ='center')

        # P lot stars over image and scale and center them
        self.plotStars(size)

        # delete temporary saved files
        os.remove("tempimgfile.png")
        os.remove("resized_image.gif")

    def createSlider(self, size):
        # add slider to the canvas and plot the first slice
        self.timeValues = self._app._timeInput.timeValues
        self.slider = tk.Scale(master=self._app, from_=0, to=len(self.timeValues)-1, orient=tk.HORIZONTAL, command = self.changeImage)
        self.slider.place(relx=0.05, rely=0.9)

        # plot first slice
        self.plotImage(0)

    def changeImage(self, time):
        # when slider is moved this will clear the canvas and change the image, the 'time' comes from slider value
        self.fovCanvas.delete("all")
        self.plotImage(time)
        self.showTime(time)

    def showTime(self, time):
        # create text box to show what time in days is being displayed
        displayTime = self.timeValues[int(time)]

        self.dispT = tk.Text(master=self._app, height=5, width=12)
        self.dispT.place(relx=0.2, rely=0.9)
        self.dispT.insert(tk.END, "Time (days):\n" + str(displayTime))


    def drawField(self):
        """Function will draw a box the size of field of view on the image"""
        results = self._app._inputboxes.getInput()
        fov = results["fieldOfView"]

        self.fovCanvas.create_rectangle(-fov/2,-fov/2,fov/2,fov/2,outline=self.border_color,tags = "field")

    def clearAll(self):
        # to be called by reset and delete everything needed
        self.fovCanvas.delete('all')
        self.slider.destroy()
        try:
            self.dispT.delete('1.0',tk.END)
        except:
            pass
