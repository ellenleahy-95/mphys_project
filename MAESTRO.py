
import tkinter as tk   # python3
from fieldOfView import FieldOfView
from lightCurve import LightCurve
from Title import Title
from sourceButton import SourceButton
from goButton import GoButton

class MAESTRO(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, width=1080, height=700)

        Title(self, master)
        sourceButton(self, master)
        self._fofv = FieldOfView(self, master)
        LightCurve(self, master)
        GoButton(self, master)

    def runMAESTRO(self, clicked):
        self._fofv.createFits()

if __name__ == "__main__":
    app = MAESTRO()
    app.pack()
    app.mainloop()
