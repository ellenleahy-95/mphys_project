import tkinter as tk   # python3
import random
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class LightCurve(object):

    def __init__(self, app, master):
        self._app = app

        self.labelfovCanvas = tk.Label(master, text="Light Curve")
        self.labelfovCanvas.place(relx=0.55, rely=0.05)

    def assignFeatures(self):
        self.starTable = self._app._sInput.starTable
        timeTable = self._app._timeInput.timeValues
        for star in self.starTable:
            star["binary"] = self.checkFeature(0.5)

            if star["binary"] == True:
                star["eclipse"] = self.checkFeature(0.4)
                if star["eclipse"] == True:
                    self.binaryEclipse(star, timeTable)
                else:
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
        phase = random.uniform(0, 2*np.pi)
        i = 0
        for time in times:
            fluxes.append(self.sineFeature(amplitude, timeScale, times[i], phase))
            i += 1
        self.addFluxes(star, fluxes)

    def binaryEclipse(self, star, times):
        timeScale = random.uniform(0.1, 1000)
        amplitude = random.uniform(0.1, 1)
        fluxes = []
        phase = random.uniform(0, 2*np.pi)
        i = 0
        for time in times:
            fluxes.append(self.sineFeature(amplitude, timeScale, times[i], phase))
            i += 1
        self.addFluxes(star, fluxes)

    def sineFeature(self, amplitude, timeScale, time, phase):
        flux = amplitude/2 * np.sin(2 * np.pi * time/timeScale + phase) + amplitude
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

    def plotLightCurve(self, star):
        self.clearLightCurve()
        fluxes = []
        times = self._app._timeInput.timeValues
        i = 1
        while i <= len(times):
            fluxes.append(self.starTable[star]["flux"+str(i)])
            i += 1

        fig = Figure()
        fig.set_size_inches(5, 4, forward=True)
        self.a = fig.add_subplot(111)
        self.a.plot(times, fluxes, '-x')

        self.a.set_title ("Light Curve for star " + str(star+1), fontsize=11)
        self.a.set_ylabel("Flux", fontsize=10)
        self.a.set_xlabel("Time (days)", fontsize=10)
        for tick in self.a.get_yticklabels():
            tick.set_rotation(65)
        fig.align_xlabels()
        self.a.tick_params(axis='x', labelsize=8)
        self.a.tick_params(axis='y', labelsize=8)

        self.lightCurve = FigureCanvasTkAgg(fig, master=self._app)
        self.lightCurve.get_tk_widget().place(relx=0.4, rely=0.05)
        self.lightCurve.draw()

    def clearLightCurve(self):
        try:
            self.lightCurve.get_tk_widget().destroy()
        except:
            pass

    def showText(self):


    def checkFeatures(self):
