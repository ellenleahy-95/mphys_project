import tkinter as tk   # python3

class LightCurve(object):

    def __init__(self, app, master):
        self._app = app
        self.lightCurve = tk.Canvas(master, bg="red", height=250, width=300)
        self.lightCurve.place(relx=0.55, rely=0.1)

        self.labelfovCanvas = tk.Label(master, text="Light Curve")
        self.labelfovCanvas.place(relx=0.55, rely=0.05)
