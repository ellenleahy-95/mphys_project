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


    def assignFeatures(self):
        self.starTable = self._app._sInput.starTable
        timeTable = self._app._timeInput.timeValues
        for star in self.starTable:
            star["binary"] = self.checkFeature(0.5)
            if star["binary"] == True:
                star["eclipse"] = self.checkFeature(0.03)
                star["herbstTI"] = False
                if star["eclipse"] == True:
                    self.binaryEclipse(star, timeTable)
                else:
                    self.addZeroFlux(star, timeTable)
            elif star["binary"] == False:
                star["eclipse"] = False
                # check if it is a Herbst Type I
                if star["type"] == "T-Tauri":
                    star["herbstTI"] = self.checkFeature(0.4)
                    if star["herbstTI"] == True:
                        self.herbstTypeI(star, timeTable)
                    else:
                        self.addZeroFlux(star, timeTable)
                else:
                    star["herbstTI"] = False
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
        timeScale = random.uniform(1/24, 1095.75)
        amplitude = random.uniform(0.1, 1)
        fluxes = []
        phase = random.uniform(0, 2*np.pi)
        i = 0
        for time in times:
            fluxes.append(self.sineFeature(amplitude, timeScale, times[i], phase))
            i += 1
        self.addFluxes(star, fluxes)

    def sineFeature(self, amplitude, timeScale, time, phase):
        flux = amplitude/2 * np.sin(2 * np.pi * time/timeScale + phase) + amplitude/2
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
        self.clearText()
        self.showText(star)
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
        self.a.set_ylabel("Change in Magnitude", fontsize=10)
        self.a.set_xlabel("Time (days)", fontsize=10)
        for tick in self.a.get_yticklabels():
            tick.set_rotation(65)
        fig.align_xlabels()
        self.a.tick_params(axis='x', labelsize=8)
        self.a.tick_params(axis='y', labelsize=8)

        self.lightCurve = FigureCanvasTkAgg(fig, master=self._app)
        self.lightCurve.get_tk_widget().place(relx=0.4, rely=0.4)
        self.lightCurve.draw()

    def clearLightCurve(self):
        try:
            self.lightCurve.get_tk_widget().destroy()
        except:
            pass

    def showText(self, star):
        features = self.checkFeatureTrue(star)

        self.T = tk.Text(master=self._app, height=30, width=30)
        self.T.place(relx=0.81, rely=0.45)
        self.T.insert(tk.END, "Variable features:\n")
        i = 0
        while i < len(features):
            self.T.insert(tk.END, features[i]+"\n")
            i += 1
        self.T.insert(tk.END, "\nMass: %.4f" % self.starTable[star]["mass"])
        self.T.insert(tk.END, "\nType: " + str(self.starTable[star]["type"]))
        self.T.insert(tk.END, "\nX coordinate: %.4f" % self.starTable[star]["XCoord"])
        self.T.insert(tk.END, "\nY coordinate: %.4f" % self.starTable[star]["YCoord"])
        self.T.insert(tk.END, "\nZ coordinate: %.4f" % self.starTable[star]["ZCoord"])

    def checkFeatureTrue(self, star):
        features = []
        for key in self.starTable[star]:
            if self.starTable[star][key] == True and key != "mass":
                features.append(key)
        return features

    def clearText(self):
        try:
            self.T.delete('1.0', tk.END)
        except:
            pass
