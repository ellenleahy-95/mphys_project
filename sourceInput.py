import tkinter as tk



GO_FONT = ("Helvetica", 20, "bold")

class SourceInput(object):


    def __init__(self, app, master):
        self._app = app

        # array will hold source masses
        SourceInput.sourceMasses = []

        self.labelMassInput = tk.Label(master, text="Mass:")
        self.labelMassInput.place(relx=0.05, rely=0.6)

        # Entry for mass
        SourceInput.massIn = tk.Entry(master, width=10)
        self.massIn.place(relx=0.1,rely=0.6)

        # Button calls massClick, saves and stores masses
        self.sButton = tk.Button(master, text="submit", command=self.massClick)
        self.sButton.place(relx=0.2, rely=0.6)

        # Label, entry and button for the file input
        self.labelFileInput = tk.Label(master, text="Mass file name:")
        self.labelFileInput.place(relx=0.05, rely=0.55)

        SourceInput.fileIn = tk.Entry(master, width=20)
        self.fileIn.place(relx=0.15, rely=0.55)

        self.fButton = tk.Button(master, text="submit", command=self.fileClick)
        self.fButton.place(relx=0.35, rely=0.55)

        self.sButton = tk.Button(master, text="Clear", command=self.clearMasses)
        self.sButton.place(relx=0.45, rely=0.55)
        

 

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

    def addToSources(self, massInput, message):
        #This will only add the mass to your array if it is a float
        if self._app.strToFloat(massInput, message):
            self.sourceMasses.append(massInput)


    def clearMasses(self):
        self.sourceMasses.clear()


