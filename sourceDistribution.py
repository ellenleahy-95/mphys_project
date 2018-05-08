import tkinter as tk   # python3
import numpy as np
import random
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sourceInput import SourceInput

class SourceDistribution(object):

    def __init__(self, app, master):
        self._app = app

        self.distOptions = ["random", "evenly distributed"]
        self.dist = tk.StringVar(master)

        #labelText = tk.StringVar()
        #labelText.set("Source distribution:")

        #labelDir = tk.Label(app, textvariable=labelText, height=4)
        ##labelDir.place(relx = 0.44, rely = 0.125)

        self.labelSourceDist = tk.Label(master, text="Source distribution:")
        self.labelSourceDist.place(relx=0.44, rely = 0.125)

        self.sourceDist = tk.OptionMenu(master, self.dist, *self.distOptions)
        self.sourceDist.config(width=20)
        self.sourceDist.place(relx=0.59, rely=0.125)

    def getDistribution(self):
        distribution = self.dist.get()
        return distribution

    def createRandomXYZ(self, size):
        phi = np.random.uniform(low=0, high=2*math.pi)
        costheta = np.random.uniform(low=-1, high=1)
        theta = math.acos(costheta)
        u = np.random.uniform(low=0, high=1)
        r = size/2 * math.pow(u, 1/3)

        x = r * math.sin(theta) * math.cos(phi)
        y = r * math.sin(theta) * math.sin(phi)
        z = r * math.cos(theta)

        return x,y,z

    def distributeRandomly(self, size, table):
        i = 0
        while i < len(table):
            x,y,z = self.createRandomXYZ(size)
            self.addToTableInput(i, "XCoord", x)
            self.addToTableInput(i, "YCoord", y)
            self.addToTableInput(i, "ZCoord", z)
            i += 1

    def distributeEvenly(self, size, table):
        R = size/2
        rho = len(table)/(4/3 * math.pi * math.pow(R,3))
        dr = R/100
        r = 0
        start = 0
        total = 0
        while r < R:
            n = 4/3 * math.pi * rho * (math.pow(r+dr,3) - math.pow(r,3))
            total += int(round(n))
            if int(n) > 0:
                if total > len(table):
                    n = len(table) - start
                self.distributeOverShell(r+dr, int(round(n)), start)
                start += int(round(n))
            r += dr
        self.distributeOverShell(R, len(table)-start, start)

    def distributeOverShell(self, r, n, start):
        for i in range(n):
            phi = np.random.uniform(low=0, high=2*math.pi)
            costheta = np.random.uniform(low=-1, high=1)
            theta = math.acos(costheta)
            u = np.random.uniform(low=0, high=1)

            x = r * math.sin(theta) * math.cos(phi)
            y = r * math.sin(theta) * math.sin(phi)
            z = r * math.cos(theta)

            self.addToTableInput(i+start, "XCoord", x)
            self.addToTableInput(i+start, "YCoord", y)
            self.addToTableInput(i+start, "ZCoord", z)


    def addToTableInput(self, star, inputName, input):
        SourceInput.addToTable(self._app._sInput, star, inputName, input)
