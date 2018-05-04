import tkinter as tk   # python3
from tabulate import tabulate
GO_FONT = ("Helvetica", 20, "bold")

from inputBoxes import InputBoxes
from sourceInput import SourceInput
from timeInput import TimeInput
from fieldOfView import FieldOfView
from astropy.table import Table, Column
from astropy.io import ascii
import numpy as np



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
        self.reset.config(state="normal")
        self.go.config(state="disabled")
        if self._app.runMAESTRO(self) == False:
            self.go.config(state="normal")

    def resetClick(self, master):
        # Deletes arrays containing masses and times
        del self._app._sInput.starTable
        del self._app._sInput.sourceMasses
        del self._app._timeInput.timeValues
        # TODO: delete time input once we actually really have it
        # Clears any text in entry fields
        SourceInput.massIn.delete(first=0,last=1000)
        SourceInput.fileIn.delete(first=0,last=1000)

        InputBoxes.sizeIn.delete(first=0,last=1000)
        InputBoxes.distanceIn.delete(first=0,last=1000)
        InputBoxes.fofvIn.delete(first=0,last=1000)

        FieldOfView.clear(self._app._fofv)
        self._app._lCurve.clearLightCurve()
        self._app._lCurve.clearText()

        self._app.setUpMAESTRO(master)

        # TimeInput.fileIn.delete(first=0,last=1000)

    def writeOutput(self):
        starTable = self._app._sInput.starTable
        results = self._app._inputboxes.getInput()
        timeValues = self._app._timeInput.timeValues
        outputList = results.items()
        #output = Table(outputList)

        #Create table from starTable
        t = Table(starTable, masked = True)

        #rename flux columns to include time at which this flux applies
        i=1
        while i <= len(timeValues):
            t.rename_column('flux' + str(i), 'Flux' + str(i) + ': t = ' + str(timeValues[i-1]))
            #t['flux' + str(i)].description = timeValues[i]
            i +=1

        #Set order for table columns

        newOrder = ['mass','type','binary','herbstTI','eclipse','XCoord','YCoord','ZCoord']
        j=1
        while j <= len(timeValues):
            newOrder.append('Flux' + str(j) + ': t = ' + str(timeValues[j-1]))
            j +=1

        newOrder = tuple(newOrder)
        data = t[newOrder]

        #Writes the completed table out to a file
        data.write('table.csv', format='csv', overwrite = True)
        

        
        
