
import tkinter as tk   # python3
from fieldOfView import FieldOfView
from lightCurve import LightCurve
from Title import Title
from sourceDistribution import SourceDistribution

class MAESTRO(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, width=1080, height=700)

        Title(self, master)
        FieldOfView(self, master)
        LightCurve(self, master)
        SourceDistribution(self, master)

if __name__ == "__main__":
    app = MAESTRO()
    app.pack()
    app.mainloop()
