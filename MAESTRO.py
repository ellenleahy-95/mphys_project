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
        # set up the main frame
        tk.Frame.__init__(self, width=1230, height=800)
        Title(self, master)
        self.setUpMAESTRO(master)

    def setUpMAESTRO(self, master):
        self._sInput = SourceInput(self, master)
        self._fofv = FieldOfView(self, master)
        self._lCurve = LightCurve(self, master)
        self._goAndR = GoAndReset(self, master)
        self._sDist = SourceDistribution(self, master)
        self._inputboxes = InputBoxes(self, master)
        self._timeInput = TimeInput(self, master)

    def runMAESTRO(self, clicked):
        # get the results from the input boxes
        results = self._inputboxes.getInput()
        try:
            size = results["skySize"]
        except:
            return False
        fieldOfView = results["fieldOfView"]
        beamSize = results["beam"]
        if type(fieldOfView) != float:
            return False
        # get the distribution selected from the dropdown menu
        dist = self._sDist.getDistribution()
        if not dist:
            messagebox.showwarning("Warning", "Please enter a distribution")
            return False
        # make sure a time file has been input
        if not self._timeInput.timeValues:
            messagebox.showwarning("Warning", "Please enter a time file")
            return False
        # create the table of stars and distribute
        self._sInput.createTable()
        if dist == "random":
            self._sDist.distributeRandomly(size, self._sInput.starTable)
        elif dist == "evenly distributed":
            self._sDist.distributeEvenly(size, self._sInput.starTable)
        # get the coordinates and output the plots etc
        self._fofv.getCoords(size)
        self._lCurve.assignFeatures()
        self._fofv.createFits(size, beamSize)
        self._fofv.createSlider(size)
        self._goAndR.writeOutput()

    def strToFloat(self, value, message):
        # change a string to a float
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
    while True:
        try:
            app.mainloop()
            break
        except UnicodeDecodeError:
            pass
