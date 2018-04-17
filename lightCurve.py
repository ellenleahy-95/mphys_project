import tkinter as tk   # python3
import random
import numpy as np

class LightCurve(object):

    def __init__(self, app, master):
        self._app = app
        self.lightCurve = tk.Canvas(master, bg="red", height=250, width=300)
        self.lightCurve.place(relx=0.55, rely=0.1)

        self.labelfovCanvas = tk.Label(master, text="Light Curve")
        self.labelfovCanvas.place(relx=0.55, rely=0.05)

    def assignFeatures(self):
        self.starTable = self._app._sInput.starTable
        timeTable = self._app._timeInput.timeValues
        for star in self.starTable:
            star["binary"] = self.checkFeature(0.5)

            if star["binary"] == True:
                self.addZeroFlux(star, timeTable)
            elif star["binary"] == False:
                # check if it is a Herbst Type I
                if star["type"] == "T-Tauri":
                    star["herbstTI"] = self.checkFeature(0.4)
                    if star["herbstTI"] == True:
                        self.herbstTypeI(star, timeTable)
                    else:
                        self.addZeroFlux(star, timeTable)
                else:
                    self.addZeroFlux(star, timeTable)

    def checkFeature(self, prob):
        if random.uniform(0,1) <= prob:
            return True
        else:
            return False

    def herbstTypeI(self, star, times):
        timeScale = random.randint(2,10)
        amplitude = 0.1
        fluxes = []
        i = 0
        for time in times:
            fluxes.append(self.sineFeature(amplitude, timeScale, times[i]))
            i += 1
        self.addFluxes(star, fluxes)

    def sineFeature(self, amplitude, timeScale, time):
        flux = amplitude/2 * np.sin(2 * np.pi * time/timeScale) + amplitude
        return flux


    def addFluxes(self, star, fluxes):
        # get the table returned by Herbst and actually put this in the star
        i = 1
        for flux in fluxes:
            star["flux"+str(i)] = flux
            i += 1
        return star


    def addZeroFlux(self, star, timeTable):
        fluxes = np.zeros(len(timeTable))
        self.addFluxes(star, fluxes)
