#will add size, distance and FofV button

import tkinter as tk
import math


class InputBoxes(object):


    def __init__(self, app, master):

        self._app = app

        # Create labels
        self.labelSize = tk.Label(master, text="Size (pc):")
        self.labelSize.place(relx=0.05,rely=0.75)
        self.labelDistance = tk.Label(master, text="Distance (pc):")
        self.labelDistance.place(relx=0.05,rely=0.8)
        self.labelFofV = tk.Label(master, text="Field of View (arcmin):")
        self.labelFofV.place(relx=0.05,rely=0.85)

        # Create entry fields
        self.sizeIn = tk.Entry(master)
        self.sizeIn.place(relx=0.19,rely=0.75)
        self.distanceIn = tk.Entry(master)
        self.distanceIn.place(relx=0.19,rely=0.8)
        self.fofvIn = tk.Entry(master)
        self.fofvIn.place(relx=0.19,rely=0.85)

    def getInput(self):
        size = self.sizeIn.get()
        size = self._app.strToFloat(size)

        distance = self.distanceIn.get()
        distance = self._app.strToFloat(distance)

        fieldOfView = self.fofvIn.get()
        fieldOfView = self._app.strToFloat(fieldOfView)

        self.sizeCalculation(size, distance)


        # 206264.806247au in 1pc. This calculates an angularSize in arcminutes
    def sizeCalculation(self, s, d):
        angularSize = ((s*206264.806247)/d)/60


