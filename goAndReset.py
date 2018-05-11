import tkinter as tk   # python3
from inputBoxes import InputBoxes
from sourceInput import SourceInput
from timeInput import TimeInput
from fieldOfView import FieldOfView
from astropy.table import Table, Column
from astropy.io import ascii
import numpy as np

# Set font for buttons
GO_FONT = ("Helvetica", 20, "bold")

class GoAndReset(SourceInput, TimeInput):

    def __init__(self, app, master):
        self._app = app

        #Create a go button
        self.go = tk.Button(master, text="GO!", font=GO_FONT, command=self.goClick)
        self.go.place(relx=0.7, rely=0.9)

        # Create a reset button which is disabled until after the go button has been pressed.
        # This will delete all lists that have   been  submitted and clear all entry fields.
        self.reset = tk.Button(master, text="Reset", font=GO_FONT, command= lambda: self.resetClick(master), state ="disabled")
        self.reset.place(relx=0.8, rely=0.9)

    def goClick(self):
        # Change the configurations once this is clicked
        self.reset.config(state="normal")
        self.go.config(state="disabled")
        # call the function and if it fails make go clickable
        if self._app.runMAESTRO(self) == False:
            self.go.config(state="normal")

    def resetClick(self, master):
        # Deletes arrays containing masses and times
        del self._app._sInput.starTable
        del self._app._sInput.sourceMasses
        del self._app._timeInput.timeValues

        # Clears any text in entry fields
        SourceInput.massIn.delete(first=0,last=tk.END)
        SourceInput.fileIn.delete(first=0,last=tk.END)

        InputBoxes.sizeIn.delete(first=0,last=tk.END)
        InputBoxes.distanceIn.delete(first=0,last=tk.END)
        InputBoxes.fofvIn.delete(first=0,last=tk.END)

        self._app._fofv.clearAll()
        self._app._lCurve.clearLightCurve()
        self._app._lCurve.clearText()

        self._app.setUpMAESTRO(master)

    def writeOutput(self):
        starTable = self._app._sInput.starTable
        results = self._app._inputboxes.getInput()
        timeValues = self._app._timeInput.timeValues

        # Set the beamsize back to arcseconds to be stored
        results["beam"] = results["beam"]*60

        # writing file out to contain input parameters
        nameList = []
        dictList = []
        for key, value in results.items():
            nameList.append(key)
            dictList.append([value])

        inputs = Table(dictList,names=nameList)

        # write inputs of beamsize etc in to file
        inputs.write("MAESTROinputs.csv", format="csv", overwrite = True)

        # Create table from starTable
        t = Table(starTable, masked = True)

        # rename flux columns to include time at which this flux applies
        i=1
        while i <= len(timeValues):
            t.rename_column("flux" + str(i), "Flux" + str(i) + ": t = " + str(timeValues[i-1]))
            i +=1

        #Set order for table columns
        newOrder = ['mass','type','binary','eclipse','coldspot','flare','XCoord','YCoord','ZCoord']
        j=1
        while j <= len(timeValues):
            newOrder.append("Flux" + str(j) + ": t = " + str(timeValues[j-1]))
            j +=1

        newOrder = tuple(newOrder)
        data = t[newOrder]

        # Writes the completed table out to a file
        data.write("MAESTROtable.csv", format="csv", overwrite = True)
