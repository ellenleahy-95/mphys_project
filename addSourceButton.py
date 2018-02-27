import tkinter as tk

#TODO add in checks, is it a number etc.

class AddSourceButton(object):
   

     def __init__(self, app, master):
         self._app = app
         
         #array will hold source masses
         self.sourceMasses = []

         self.label = tk.Label(master, text="Mass:")
         self.label.place(relx=0.05,rely=0.5)

         #Entry for mass
         self.massin = tk.Entry(master)
         self.massin.place(relx=0.1,rely=0.5)

         #Button calls massClick, saves and stores masses
         self.addSourceButton = tk.Button(master, text = "submit", command =self.massClick)
         self.addSourceButton.place(relx=0.25, rely=0.5)


     
     def massClick(self):
         self.mass = self.massin.get()
         self.makeAList()

     def makeAList(self):
         self.sourceMasses.append(self.mass)
         print(self.sourceMasses)




