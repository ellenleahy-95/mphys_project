#will add size, distance and FofV button

import tkinter as tk
import math


class InputBoxes(object):


    def __init__(self, app, master):

        self._app = app

        # Create labels
        self.labelSize = tk.Label(master, text="Size (pc):")
        self.labelSize.place(relx=0.05,rely=0.175)
        self.labelDistance = tk.Label(master, text="Distance (pc):")
        self.labelDistance.place(relx=0.05,rely=0.225)
        self.labelFofV = tk.Label(master, text="Field of View (arcmin):")
        self.labelFofV.place(relx=0.05,rely=0.275)
        self.labelBeamSize = tk.Label(master, text="Beam size (arcsec):")
        self.labelBeamSize.place(relx=0.05, rely=0.325)

        # Create entry fields
        InputBoxes.sizeIn = tk.Entry(master)
        self.sizeIn.place(relx=0.19,rely=0.175)
        InputBoxes.distanceIn = tk.Entry(master)
        self.distanceIn.place(relx=0.19,rely=0.225)
        InputBoxes.fofvIn = tk.Entry(master)
        self.fofvIn.place(relx=0.19,rely=0.275)
        InputBoxes.beamIn = tk.Entry(master)
        self.beamIn.place(relx=0.19, rely=0.325)





    def getInput(self):
        results = {}

        size = self._app.strToFloat(self.sizeIn.get(), "Size input error")

        distance = self._app.strToFloat(self.distanceIn.get(), "Distance input error")

        fOfV = self._app.strToFloat(self.fofvIn.get(), "Field of view input error")

        beamSize = self._app.strToFloat(self.beamIn.get(), "Beam size input error")

        try:
            beamSize = beamSize/60
        except:
            return False

        try:
            results["skySize"] = self.sizeCalculation(size, distance)
        except:
            return False

        results["size"] = size
        results["distance"] = distance
        results["fieldOfView"] = fOfV
        results["beam"] = beamSize

        return results

    # This calculates an angularSize in arcminutes
    def sizeCalculation(self, s, d):
        angularSize = ((s*(648000/math.pi))/d)/60
        return angularSize
