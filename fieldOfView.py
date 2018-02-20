import tkinter as tk   # python3

class FieldOfView(object):

    def __init__(self, app, master):
        self._app = app
        self.fovCanvas = tk.Canvas(master, bg="blue", height=250, width=300)
        self.fovCanvas.place(relx=0.05, rely=0.1)
