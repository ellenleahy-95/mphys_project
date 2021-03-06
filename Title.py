import tkinter as tk   # python3
TITLE_FONT = ("Helvetica", 30, "bold")

class Title(object):
    def __init__(self, app, master):
        """Writes the title centred at the top of the gui, and authors names in the bottom right"""
        self._app = app
        self.tempTitle = tk.Label(master, text="WELCOME TO MAESTRO", font=TITLE_FONT)
        self.tempTitle.place(relx=0.5, rely=0, anchor = tk.N)


        self.names = tk.Label(master, text="Written by Ellen Leahy and Joe Stickley")
        self.names.place(relx=0.7, rely=0.95,)
