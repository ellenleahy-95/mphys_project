
import tkinter as tk   # python3
from fieldOfView import FieldOfView
from lightCurve import LightCurve
from Title import Title
TITLE_FONT = ("Helvetica", 30, "bold")

class MAESTRO(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master, width=1080, height=800)

        title = Title(self, master)
        fofv = FieldOfView(self, master)
        lCurve = LightCurve(self, master)
