import tkinter as tk   # python3
import numpy as np
import random

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

    def distributeRandomly(self, size):
        sizeArray = np.arange(0.0, size, 0.01)
        x = random.choice(sizeArray)
        y = random.choice(sizeArray)
        print(x)
        print(y)
        return x,y
