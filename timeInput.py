import tkinter as tk

# TODO add in checks, is it a number etc.

class TimeInput(object):


    def __init__(self, app, master):
         self._app = app

         # array will hold source masses
         self.timeValues = []

         # Label, entry and button for the file input
         self.labelFileInput = tk.Label(master, text="Time file name:")
         self.labelFileInput.place(relx=0.55, rely=0.55)

         self.fileIn = tk.Entry(master, width=20)
         self.fileIn.place(relx=0.65, rely=0.55)

         self.fButton = tk.Button(master, text="submit", command=self.fileClick)
         self.fButton.place(relx=0.85, rely=0.55)

    def fileClick(self):
        try:
            with open(self.fileIn.get()) as self.file:
                for line in self.file:
                    if not line.startswith('#'):
                        self._app.strToFloat(line.rstrip('\n'))
                        self.timeValues.append(line.rstrip('\n'))
        except:
            print("Please enter a valid file name")
            exit()
