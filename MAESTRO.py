
import tkinter as tk   # python3
from fieldOfView import FieldOfView
from lightCurve import LightCurve
from Title import Title
from sourceInput import SourceInput
from goButton import GoButton
from sourceDistribution import SourceDistribution
from inputBoxes import InputBoxes
from timeInput import TimeInput

class MAESTRO(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, width=1080, height=700)

        Title(self, master)
        self._sInput = SourceInput(self, master)
        self._fofv = FieldOfView(self, master)
        # self._graph = Graph(self)
        LightCurve(self, master)
        GoButton(self, master)
        self._sDist = SourceDistribution(self, master)
        self._inputboxes = InputBoxes(self, master)
        TimeInput(self, master)


    def runMAESTRO(self, clicked):
        self._fofv.createFits()
        size = self._inputboxes.getInput()
        dist = self._sDist.getDistribution()
        self._sInput.createTable()
        if dist == "random":
            self._sDist.distributeRandomly(size, self._sInput.starTable)
        elif dist == "evenly distributed":
            self._sDist.distributeEvenly(size, self._sInput.starTable)
        else:
            print("Please pick a distribution")
        self._fofv.plotStars(size)

    def strToFloat(self, value):
        try:
            return float(value)
        except ValueError:
            print("All values must be floats")
            exit()



if __name__ == "__main__":
    app = MAESTRO()
    app.pack()
    app.mainloop()
