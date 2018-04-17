
import tkinter as tk   # python3
from fieldOfView import FieldOfView
from lightCurve import LightCurve
from Title import Title
from sourceInput import SourceInput
from goAndReset import GoAndReset
from sourceDistribution import SourceDistribution
from inputBoxes import InputBoxes
from timeInput import TimeInput
from tkinter import messagebox

class MAESTRO(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, width=1080, height=700)

        Title(self, master)

        self.setUpMAESTRO(master)


    def setUpMAESTRO(self, master):
        self._sInput = SourceInput(self, master)
        self._fofv = FieldOfView(self, master)
        # self._graph = Graph(self)
        self._lCurve = LightCurve(self, master)
        self._goAndR = GoAndReset(self, master)
        self._sDist = SourceDistribution(self, master)
        self._inputboxes = InputBoxes(self, master)
        self._timeInput = TimeInput(self, master)


    def runMAESTRO(self, clicked):
        results = self._inputboxes.getInput()
        try:
            size = results["skySize"]
        except:
            return False
        fieldOfView = results["fieldOfView"]
        beamSize = results["beam"]
        if type(fieldOfView) != float:
            return False
        dist = self._sDist.getDistribution()
        if not dist:
            messagebox.showwarning("Warning", "Please enter a distribution")
            return False

        if not self._timeInput.timeValues:
            messagebox.showwarning("Warning", "Please enter a time file")
            return False
        self._sInput.createTable()
        if dist == "random":
            self._sDist.distributeRandomly(size, self._sInput.starTable)
        elif dist == "evenly distributed":
            self._sDist.distributeEvenly(size, self._sInput.starTable)
        self._fofv.plotStars(size)
        self._lCurve.assignFeatures()
        self._fofv.createFits(size, beamSize)


    def strToFloat(self, value, message):
        try:
            if float(value) <= 0:
                # Gives error message if entry is negative
                result = messagebox.showwarning("Invalid Entry", message)
            else:
                return float(value)
        except ValueError:
            # Gives this error message if entry is not a number
            result = messagebox.showwarning("Invalid Entry", message)


if __name__ == "__main__":
    app = MAESTRO()
    app.pack()
    app.mainloop()
