import tkinter as tk
import math


class InputBoxes(object):
    def __init__(self, app, master):
        self._app = app

        # Create labels
        self.labelSize = tk.Label(master, text="Size (pc):")
        self.labelSize.place(relx=0.05,rely=0.3)
        self.labelDistance = tk.Label(master, text="Distance (pc):")
        self.labelDistance.place(relx=0.05,rely=0.35)
        self.labelFofV = tk.Label(master, text="Field of View (arcmin):")
        self.labelFofV.place(relx=0.05,rely=0.4)
        self.labelBeamSize = tk.Label(master, text="Beam size (arcsec):")
        self.labelBeamSize.place(relx=0.05, rely=0.45)

        # Create entry fields
        InputBoxes.sizeIn = tk.Entry(master)
        self.sizeIn.place(relx=0.18,rely=0.3)
        InputBoxes.distanceIn = tk.Entry(master)
        self.distanceIn.place(relx=0.18,rely=0.35)
        InputBoxes.fofvIn = tk.Entry(master)
        self.fofvIn.place(relx=0.18,rely=0.4)
        InputBoxes.beamIn = tk.Entry(master)
        self.beamIn.place(relx=0.18, rely=0.45)

    def getInput(self):
        results = {}

        # get all the values from the input fields
        size = self._app.strToFloat(self.sizeIn.get(), "Size input error")
        distance = self._app.strToFloat(self.distanceIn.get(), "Distance input error")
        fOfV = self._app.strToFloat(self.fofvIn.get(), "Field of view input error")
        beamSize = self._app.strToFloat(self.beamIn.get(), "Beam size input error")

        # try statement let's it break if beamSize or size aren't numbers
        try:
            beamSize = beamSize/60
        except:
            return False

        try:
            results["skySize"] = self.sizeCalculation(size, distance)
        except:
            return False

        # puts all the values in a disctionary so its easy to read
        results["size"] = size
        results["distance"] = distance
        results["fieldOfView"] = fOfV
        results["beam"] = beamSize

        return results

    def sizeCalculation(self, s, d):
        # This calculates an angularSize in arcminutes
        angularSize = ((s*(648000/math.pi))/d)/60
        return angularSize
