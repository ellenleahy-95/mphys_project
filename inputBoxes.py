#will add size, distance and FofV button

import tkinter as tk


class InputBoxes(object):


     def __init__(self, app, master):

         self._app = app

         # Create labels
         self.labelSize = tk.Label(master, text="Size (pc):")
         self.labelSize.place(relx=0.05,rely=0.75)
         self.labelDistance = tk.Label(master, text="Distance (pc):")
         self.labelDistance.place(relx=0.05,rely=0.8)
         self.labelFofV = tk.Label(master, text="Field of View (arcmin):")
         self.labelFofV.place(relx=0.05,rely=0.85)

         # Create entry fields
         self.sizeIn = tk.Entry(master)
         self.sizeIn.place(relx=0.19,rely=0.75)
         self.distanceIn = tk.Entry(master)
         self.distanceIn.place(relx=0.19,rely=0.8)
         self.fofvIn = tk.Entry(master)
         self.fofvIn.place(relx=0.19,rely=0.85)

     def getInput(self):
         size = self.sizeIn.get()
         self._app.strToFloat(size, "Size input error")

         distance = self.distanceIn.get()
         self._app.strToFloat(distance, "Distance input error")

         fieldOfView = self.fofvIn.get()
         self._app.strToFloat(fieldOfView, "Field of View input error")
