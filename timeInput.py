import tkinter as tk

# TODO add in checks, is it a number etc.

class TimeInput(object):


    def __init__(self, app, master):
        """On set up this will create an entry field for the user to submit a file of times, and an array to hold time values"""
        self._app = app

        # array will hold time values
        self.timeValues = []

        # Label, entry and button for the file input
        self.labelFileInput = tk.Label(master, text="Time file name:")
        self.labelFileInput.place(relx=0.46, rely=0.3)

        self.fileIn = tk.Entry(master, width=20)
        self.fileIn.place(relx=0.6, rely=0.3)

        # on click calls fileclick, this reads in time file in
        self.fButton = tk.Button(master, text="submit", command=self.fileClick) 
        self.fButton.place(relx=0.76, rely=0.3)


    def fileClick(self):
        """Reads in time file and stores a list sorted in to numerical order in timeValues"""
        try:
            with open(self.fileIn.get()) as self.file:
                i = 0
                for line in self.file:
                    i += 1
                    if not line.startswith('#'):
                        # Adds times to array, showing this error message for invalid entries
                        self.addTime(line.rstrip('\n'), "Invalid entry on line " + str(i) +  ". \nAll other values were successfully added")
            self.timeValues.sort() #Sorts the values in to ascending order
            self.fileIn.config(state="disabled")
            self.fButton.config(state="disabled")
        except:
            result = tk.messagebox.showwarning("Invalid Entry", "Please enter a valid file name")
            self.fileIn.delete(first=0,last=1000)

    def addTime(self, timeInput, message):
        """This will only add the mass to your array if it is a float, if an invalid entry is there """
        time = self._app.strToFloat(timeInput, message)
        if time:
            self.timeValues.append(time)
