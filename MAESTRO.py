
import tkinter as tk   # python3
from fieldOfView import FieldOfView
from lightCurve import LightCurve
from Title import Title

class MAESTRO(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, width=1080, height=700)

        title = Title(self, master)
        fofv = FieldOfView(self, master)
        lCurve = LightCurve(self, master)
        fofv.createFits()

if __name__ == "__main__":
    app = MAESTRO()
    app.pack()
    app.mainloop()
