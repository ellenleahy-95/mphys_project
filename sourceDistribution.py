import tkinter as tk   # python3

class SourceDistribution(object):

    def __init__(self, app, master):
        self._app = app
        distOptions = ["random", "evenly distributed"]
        dist = tk.StringVar(master)

        labelText = tk.StringVar()
        labelText.set("Source distribution: ")

        labelDir = tk.Label(app, textvariable=labelText, height=4)
        labelDir.place(relx = 0.48, rely = 0.57)

        self.sourceDist = tk.OptionMenu(master, dist, *distOptions)
        self.sourceDist.config(width=20)
        self.sourceDist.place(relx=0.62, rely=0.6)
