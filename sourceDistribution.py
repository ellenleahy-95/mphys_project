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

        labelText = tk.StringVar()
        labelText.set("Source distribution:")

        labelDir = tk.Label(app, textvariable=labelText, height=4)
        labelDir.place(relx = 0.48, rely = 0.57)

        self.sourceDist = tk.OptionMenu(master, self.dist, *self.distOptions)
        self.sourceDist.config(width=20)
        self.sourceDist.place(relx=0.62, rely=0.6)

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
            self.addToTableInput(i, x)
            self.addToTableInput(i, y)
            self.addToTableInput(i, z)
            i += 1

    def distributeEvenly(self, size, table):
        R = size/2
        rho = len(table)/(4/3 * math.pi * math.pow(R,3))
        dr = R/100
        r = 0
        start = 0
        while r < R:
            n = 4/3 * math.pi * rho * (math.pow(r+dr,3) - math.pow(r,3))
            if int(n) > 0:
                self.distributeOverShell(r+dr, int(round(n)), start)
                start += int(round(n))
                print("n: " + str(n) + "\n int n: " + str(int(round((n)))) + "\n  start: " + str(start))
            r += dr
        self.distributeOverShell(R, len(table)-start, start)
        print(table)
        print(str(len(table)))

    def distributeOverShell(self, r, n, start):
        offset = 2/n
        increment = math.pi * (3 - math.sqrt(5))
        i = 0
        for i in range(n):
            # y = ((i * offset) - 1) + (offset / 2)
            # r_unit = math.sqrt(1 - pow(y,2))
            #
            # phi = ((i + 1) % n) * increment
            #
            # x = math.cos(phi) * r_unit
            # z = math.sin(phi) * r_unit
            #
            # self.addToTableInput(i+start, x*r)
            # self.addToTableInput(i+start, y*r)
            # self.addToTableInput(i+start, z*r)

            phi = np.random.uniform(low=0, high=2*math.pi)
            costheta = np.random.uniform(low=-1, high=1)
            theta = math.acos(costheta)

            x = r * math.sin(theta) * math.cos(phi)
            y = r * math.sin(theta) * math.sin(phi)
            z = r * math.cos(theta)

            self.addToTableInput(i+start, x)
            self.addToTableInput(i+start, y)
            self.addToTableInput(i+start, z)

            i += 1

    def addToTableInput(self, star, input):
        SourceInput.addToTable(self._app._sInput, star, input)
