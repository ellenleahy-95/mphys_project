import tkinter as tk

# TODO add in checks, is it a number etc.

class TimeInput(object):


    def __init__(self, app, master):
        self._app = app

        # array will hold source masses
        self.timeValues = []

        # Label, entry and button for the file input
        self.labelFileInput = tk.Label(master, text="Time file name:")
        self.labelFileInput.place(relx=0.46, rely=0.3)

        self.fileIn = tk.Entry(master, width=20)
        self.fileIn.place(relx=0.6, rely=0.3)

        self.fButton = tk.Button(master, text="submit", command=self.fileClick)
        self.fButton.place(relx=0.76, rely=0.3)

        # self.sButton = tk.Button(master, text="Clear", command=self.clearTimes)
        # self.sButton.place(relx=0.95, rely=0.55)

    def fileClick(self):
        try:
            with open(self.fileIn.get()) as self.file:
                i = 0
                for line in self.file:
                    i += 1
                    if not line.startswith('#'):
                        self.addTime(line.rstrip('\n'), "Invalid entry on line " + str(i) +  ". \nAll other values were successfully added")
            self.timeValues.sort()
            self.fileIn.config(state="disabled")
            self.fButton.config(state="disabled")
        except:
            result = tk.messagebox.showwarning("Invalid Entry", "Please enter a valid file name")
            self.fileIn.delete(first=0,last=1000)

    def addTime(self, timeInput, message):
        #This will only add the mass to your array if it is a float
        time = self._app.strToFloat(timeInput, message)
        if time:
            self.timeValues.append(time)
