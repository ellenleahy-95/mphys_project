import tkinter as tk
from tkinter import messagebox
import random
import numpy as np

GO_FONT = ("Helvetica", 20, "bold")

class SourceInput(object):


    def __init__(self, app, master):
        self._app = app

        # array will hold source masses
        self.sourceMasses = []
        self.starTable = []

        self.massDistOptions = ["Kroupa"]  #Store here the options for which form of IMF is to be used. 
        self.massDist = tk.StringVar(master)

        self.labelMassInput = tk.Label(master, text="Mass:")
        self.labelMassInput.place(relx=0.05, rely=0.125)

        # Entry for single mass
        SourceInput.massIn = tk.Entry(master, width=20)
        self.massIn.place(relx=0.16,rely=0.125)

        # Button calls massClick, saves and stores masses
        self.sButton = tk.Button(master, text="submit", command=self.massClick)
        self.sButton.place(relx=0.32, rely=0.125)

        # Label, entry and button for the file input
        self.labelFileInput = tk.Label(master, text="Mass file name:")
        self.labelFileInput.place(relx=0.05, rely=0.075)

        SourceInput.fileIn = tk.Entry(master, width=20)
        self.fileIn.place(relx=0.16, rely=0.075)

        self.fButton = tk.Button(master, text="submit", command=self.fileClick)
        self.fButton.place(relx=0.32, rely=0.075)

        #label for mass distribution options
        self.labelMassInput = tk.Label(master, text="Mass distribution:")
        self.labelMassInput.place(relx=0.05, rely=0.175)

        #mass distribution options
        self.massDistDropDown = tk.OptionMenu(master, self.massDist, *self.massDistOptions)
        self.massDistDropDown.config(width=10)
        self.massDistDropDown.place(relx=0.16, rely=0.175)

        #label for min mass
        self.labelMinMass = tk.Label(master, text="Min mass:")
        self.labelMinMass.place(relx=0.3, rely=0.175)

        # Entry for mass minumum for range
        SourceInput.minMass = tk.Entry(master, width=10)
        self.minMass.place(relx=0.37, rely=0.175)
        self.minMass.insert(0, 'min=0.01')
        self.minMass.config(fg = 'grey')
        minClick = lambda event: self.onEntryClick(event, "min=0.01", self.minMass)
        self.minMass.bind('<FocusIn>', minClick)
        minOut = lambda event: self.onFocusOut(event, "min=0.01", self.minMass)
        self.minMass.bind('<FocusOut>', minOut)

        #Label for max mass
        self.labelMaxMass = tk.Label(master, text="Max mass:")
        self.labelMaxMass.place(relx=0.3, rely=0.225)

        # Entry for mass maximum for range
        SourceInput.maxMass = tk.Entry(master, width=10)
        self.maxMass.place(relx=0.37, rely=0.225)
        self.maxMass.insert(0, 'max=120')
        self.maxMass.config(fg = 'grey')
        maxClick = lambda event: self.onEntryClick(event, "max=120", self.maxMass)
        self.maxMass.bind('<FocusIn>', maxClick)
        maxOut = lambda event: self.onFocusOut(event, "max=120", self.maxMass)
        self.maxMass.bind('<FocusOut>', maxOut)


        #Label for number of stars
        self.labelStarNumber = tk.Label(master, text="Number of stars:")
        self.labelStarNumber.place(relx=0.46, rely=0.175)

        # Entry for number of stars
        SourceInput.starNumber = tk.Entry(master, width=10)
        self.starNumber.place(relx=0.56, rely=0.175)

        self.massDistButton = tk.Button(master, text="submit", command=self.distributeMass)
        self.massDistButton.place(relx=0.7, rely=0.175)


    def onEntryClick(self, event, text, box):
        """function that gets called whenever entry is clicked"""
        if box.get() == text:
            box.delete(0, "end") # delete all the text in the entry
            box.insert(0, '') #Insert blank for user input
            box.config(fg = 'black')

    def onFocusOut(self, event, text, box):
        if box.get() == '':
            box.insert(0, text)
            box.config(fg = 'grey')

    def massClick(self):
        self.mass = self.massIn.get()
        self.addToSources(self.mass, "mass input error")
        #clears the entry field
        self.massIn.delete(first=0,last=1000)

    def fileClick(self):
        try:
            with open(self.fileIn.get()) as self.file:
                i = 0
                for line in self.file:
                    i += 1
                    if not line.startswith('#'):
                        self.addToSources(line.rstrip('\n'), "Invalid entry on line " + str(i) +  ". \nAll other values were successfully added")

        except:
            result = tk.messagebox.showwarning("Invalid Entry", "Please enter a valid file name")
        self.fileIn.delete(first=0,last=1000)

    def distributeMass(self):
        massDist = self.getMassDistribution()
        minValue = self.getMinMass()
        maxValue = self.getMaxMass()
        number = self.getStarNumber()
        if minValue == False or maxValue == False or number == False:
            return False
        self.minMass.config(fg = 'grey')
        self.maxMass.config(fg = 'grey')
        self.starNumber.config(fg = 'grey')
        self.kroupaDist(minValue, maxValue, number)

    def getMinMass(self):
        minValue = self._app.strToFloat(self.minMass.get(), "Please enter a valid min mass")
        if isinstance(minValue, float) == False:
            self.minMass.delete(first=0, last=tk.END)
            return False
        elif minValue < 0.01:
            self.minMass.delete(first=0, last=tk.END)
            tk.messagebox.showwarning("Invalid Entry", "Please enter a min mass > 0.01")
            return False
        else:
            return minValue

    def getMaxMass(self):
        maxValue = self._app.strToFloat(self.maxMass.get(), "Please enter a valid max mass")
        if isinstance(maxValue, float) == False:
            self.maxMass.delete(first=0, last=tk.END)
            return False
        elif maxValue > 120:
            self.maxMass.delete(first=0, last=tk.END)
            tk.messagebox.showwarning("Invalid Entry", "Please enter a max mass < 120")
            return False
        else:
            return maxValue

    def getStarNumber(self):
        number = self._app.strToFloat(self.starNumber.get(), "Please enter a valid number of stars")
        if isinstance(number, float) == False:
            self.starNumber.delete(first=0, last=tk.END)
            return False
        else:
            return number

    def setKroupaVals(self):
        self.probs = []
        self.probs.append(0.37)
        self.probs.append(0.48)
        self.probs.append(0.089)
        self.probs.append(0.057)
        self.probs.append(0.004)

        self.range = []
        self.vLowRange = (0.01, 0.08)
        self.range.append(self.vLowRange)
        self.lowRange = (0.08, 0.5)
        self.range.append(self.lowRange)
        self.mediumRange = (0.5, 1)
        self.range.append(self.mediumRange)
        self.highRange = (1, 8)
        self.range.append(self.highRange)
        self.vHighRange = (8, 120)
        self.range.append(self.vHighRange)

    def setDistProb(self, minVal, maxVal):
        bins = []
        myValues = [minVal, maxVal]
        myBins = [self.range[0][1], self.range[1][1], self.range[2][1], self.range[3][1], self.range[4][1]]
        bins = np.digitize(myValues, myBins)
        if bins[0] != 0 or bins[1] != 4:
            i = 0
            j = 0
            while i < len(self.probs):
                if i < bins[0] or i > bins[1]:
                    del self.probs[i-j]
                    j += 1
                i += 1
            k = 0
            newProbs = []
            while k < len(self.probs):
                prob = self.probs[k]/sum(self.probs)
                newProbs.append(prob)
                k += 1
            self.probs = newProbs
        return bins[0], bins[1]

    def kroupaDist(self, minVal, maxVal, number):
        self.setKroupaVals()
        minBox, maxBox = self.setDistProb(minVal, maxVal)
        if maxBox == 5:
            maxBox = 4
        i = minBox
        j = 0
        count = 0
        while i <= maxBox:
            stars = round(self.probs[j]*number)
            count += self.setMasses(stars, self.range[i], minVal, maxVal)
            i += 1
            j += 1
        if count < number:
            warningMessage = "You entered a mass value not at the edge of a range. Please note only " + str(count) + " stars were used. Cick cancel to reenter."
            if messagebox.askokcancel("Warning", warningMessage) == False:
                self.sourceMasses = []
                self.range = []
                self.probs = []
                self.maxMass.delete(0, tk.END)
                self.maxMass.config(fg = 'black')
                self.minMass.delete(0, tk.END)
                self.minMass.config(fg = 'black')
                self.starNumber.delete(0, tk.END)
                self.starNumber.config(fg = 'black')


    def setMasses(self, stars, massRange, minMass, maxMass):
        i = 0
        count = 0
        while i < stars:
            mass = random.uniform(massRange[0], massRange[1])
            if mass >= minMass and mass <= maxMass:
                self.addToSources(mass, "Please enter a valid mass")
                count += 1
            i += 1
        return count

    def getMassDistribution(self):
        distribution = self.massDist.get()
        return distribution

    def addToSources(self, massInput, message):
        #This will only add the mass to your array if it is a float
        mass = self._app.strToFloat(massInput, message)
        if mass:
            self.sourceMasses.append(mass)

    def createTable(self):
         i = 0
         for mass in self.sourceMasses:
            tempDict = {}
            tempDict["mass"] = self.sourceMasses[i]
            tempDict["type"] = self.assignType(self.sourceMasses[i])
            self.starTable.append(tempDict)
            i += 1
         return self.starTable

    def addToTable(self, star, variableName, variable):
        self.starTable[star][variableName] = variable

    def assignType(self, starMass):
        if starMass <= 2:
            return "T-Tauri"
        elif starMass > 2 and starMass <= 8:
            return "Intermediate"
        elif starMass > 8:
            return "Massive"
