#will add size, distance and FofV button

import tkinter as tk


class InputBoxes(object):


     def __init__(self, app, master):
         
         self._app = app


         #Create labels
         self.label = tk.Label(master, text="Size:")
         self.label.place(relx=0.05,rely=0.8)
         self.label = tk.Label(master, text="Distance:")
         self.label.place(relx=0.05,rely=0.82)
         self.label = tk.Label(master, text="Field of View:")
         self.label.place(relx=0.05,rely=0.84)

         #Create entry fields
         self.sizein = tk.Entry(master)
         self.sizein.place(relx=0.15,rely=0.8)
         self.distanceIn = tk.Entry(master)
         self.distanceIn.place(relx=0.15,rely=0.82)
         self.fofvin = tk.Entry(master)
         self.fofvin.place(relx=0.15,rely=0.84)

     def getInput(self):
         size = self.sizein.get()
         self._app.strToFloat(size)

         distance = self.distanceIn.get()
         self._app.strToFloat(distance)

         fieldOfView = self.fofvin.get()
         self._app.strToFloat(fieldOfView)

         

         print("Size = %s \n Distance = %s \n Field of View = %s" % (size, distance, fieldOfView))



         #Button calls massClick, saves and stores masses
         #self.SourceButton = tk.Button(master, text = "submit", command =self.massClick)
         #self.SourceButton.place(relx=0.25, rely=0.5)



   #  def massClick(self):
   #      self.mass = self.massin.get()
   #      self.makeAList()

  #   def makeAList(self):
   #      self.sourceMasses.append(self.mass)
    #     print(self.sourceMasses)
