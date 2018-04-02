
import tkinter as tk   # python3
from fieldOfView import FieldOfView
from lightCurve import LightCurve
from Title import Title
from sourceInput import SourceInput
from goButton import GoButton
from sourceDistribution import SourceDistribution
from inputBoxes import InputBoxes
from timeInput import TimeInput
from tkinter import messagebox

class MAESTRO(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, width=1080, height=700)

        Title(self, master)
        SourceInput(self, master)
        self._fofv = FieldOfView(self, master)
        LightCurve(self, master)
        GoButton(self, master)
        SourceDistribution(self, master)
        self._inputboxes = InputBoxes(self,master)
        TimeInput(self, master)


    def runMAESTRO(self, clicked):
        self._fofv.createFits()
        self._inputboxes.getInput()

    def strToFloat(self, value, message):
        try:
            if float(value) <= 0:
                #Gives error message if entry is negative
                result = messagebox.showwarning("Invalid Entry", message)
            else:   
                return float(value)
        except ValueError:
            #Gives this error message if entry is not a number
            result = messagebox.showwarning("Invalid Entry", message)


if __name__ == "__main__":
    app = MAESTRO()
    app.pack()
    app.mainloop()
