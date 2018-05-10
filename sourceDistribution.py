import tkinter as tk   # python3
import numpy as np
import random
import math
from sourceInput import SourceInput

class SourceDistribution(object):

    def __init__(self, app, master):
        self._app = app
        # set up the options for the dropdown menu
        self.distOptions = ["random", "evenly distributed"]
        self.dist = tk.StringVar(master)

        # inputting the label
        self.labelSourceDist = tk.Label(master, text="Source distribution:")
        self.labelSourceDist.place(relx=0.46, rely = 0.35)

        # dropdown menu for source distribution
        self.sourceDist = tk.OptionMenu(master, self.dist, *self.distOptions)
        self.sourceDist.config(width=20)
        self.sourceDist.place(relx=0.6, rely=0.35)

    def getDistribution(self):
        # get the distribution in the dropdown
        distribution = self.dist.get()
        return distribution

    def createRandomXYZ(self, size):
        # returns a random X Y and Z coordinate
        # calculating polar coordinates
        phi = np.random.uniform(low=0, high=2*math.pi)
        u = random.uniform(0, 1)
        theta = math.acos(1 - 2*u)
        v = np.random.uniform(low=0, high=1)
        r = size/2 * math.pow(v, 1/3)

        # change polar coordinates to cartesian
        x = r * math.sin(theta) * math.cos(phi)
        y = r * math.sin(theta) * math.sin(phi)
        z = r * math.cos(theta)

        return x,y,z

    def distributeRandomly(self, size, table):
        # calculates random coordinates for each star
        i = 0
        while i < len(table):
            x,y,z = self.createRandomXYZ(size)
            self.addToTableInput(i, "XCoord", x)
            self.addToTableInput(i, "YCoord", y)
            self.addToTableInput(i, "ZCoord", z)
            i += 1

    def distributeEvenly(self, size, table):
        # the radius should be half the size given
        R = size/2
        # calcualte the density for a constant density
        rho = len(table)/(4/3 * math.pi * math.pow(R,3))
        # thickness of the shells
        dr = R/100
        r = 0
        start = 0
        total = 0
        # for rach shell calculate how many stars are on it and then distribute over the shell
        while r < R:
            # calculate the number in the shell
            n = 4/3 * math.pi * rho * (math.pow(r+dr,3) - math.pow(r,3))
            total += int(round(n))
            # only do the next bit if there are some in this shell
            if int(n) > 0:
                # make sure we haven't gone over the total number of stars
                if total > len(table):
                    n = len(table) - start
                self.distributeOverShell(r+dr, int(round(n)), start)
                start += int(round(n))
            r += dr
        # put all stars that haven't already been added in the outer shell
        self.distributeOverShell(R, len(table)-start, start)

    def distributeOverShell(self, r, n, start):
        # as for before but r is a constant
        for i in range(n):
            phi = np.random.uniform(low=0, high=2*math.pi)
            u = random.uniform(0,1)
            theta = math.acos(1-2*u)

            x = r * math.sin(theta) * math.cos(phi)
            y = r * math.sin(theta) * math.sin(phi)
            z = r * math.cos(theta)

            self.addToTableInput(i+start, "XCoord", x)
            self.addToTableInput(i+start, "YCoord", y)
            self.addToTableInput(i+start, "ZCoord", z)


    def addToTableInput(self, star, inputName, input):
        # add that star t the main table
        SourceInput.addToTable(self._app._sInput, star, inputName, input)
