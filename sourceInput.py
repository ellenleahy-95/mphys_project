import tkinter as tk

# TODO add in checks, is it a number etc.

class SourceInput(object):


     def __init__(self, app, master):
         self._app = app

         # array will hold source masses
         self.sourceMasses = []
         self.starTable = []

         self.labelMassInput = tk.Label(master, text="Mass:")
         self.labelMassInput.place(relx=0.05, rely=0.6)

         # Entry for mass
         self.massIn = tk.Entry(master, width=10)
         self.massIn.place(relx=0.1,rely=0.6)

         # Button calls massClick, saves and stores masses
         self.sButton = tk.Button(master, text="submit", command=self.massClick)
         self.sButton.place(relx=0.2, rely=0.6)

         # Label, entry and button for the file input
         self.labelFileInput = tk.Label(master, text="Mass file name:")
         self.labelFileInput.place(relx=0.05, rely=0.55)

         self.fileIn = tk.Entry(master, width=20)
         self.fileIn.place(relx=0.15, rely=0.55)

         self.fButton = tk.Button(master, text="submit", command=self.fileClick)
         self.fButton.place(relx=0.35, rely=0.55)

     def massClick(self):
         self.mass = self.massIn.get()
         self.addToSources(self.mass)
         #clears the entry field
         self.massIn.delete(first=0,last=1000)

     def fileClick(self):
         try:
             with open(self.fileIn.get()) as self.file:
                 for line in self.file:
                     if not line.startswith('#'):
                         self.addToSources(line.rstrip('\n'))
         except:
             print("Please enter a valid file name")
             exit()

     def addToSources(self, massInput):
         massInput = self._app.strToFloat(massInput)
         self.sourceMasses.append(massInput)


     def createTable(self):
         i = 0
         for mass in self.sourceMasses:
            tempArray = []
            tempArray.append(self.sourceMasses[i])
            tempArray.append(self.assignType(self.sourceMasses[i]))
            self.starTable.append(tempArray)
            i += 1
         print(self.starTable)
         return self.starTable

     def addToTable(self, star, variable):
         self.starTable[star].append(variable)
         print(self.starTable)

     def assignType(self, starMass):
        if starMass <= 2:
            return "T-Tauri"
        elif starMass > 2 and starMass <= 8:
            return "Medium"
        elif starMass > 8:
            return "Massive"
