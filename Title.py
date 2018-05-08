import tkinter as tk   # python3
TITLE_FONT = ("Helvetica", 30, "bold")

class Title(object):
    def __init__(self, app, master):
        self._app = app
        self.tempTitle = tk.Label(master, text="WELCOME TO MAESTRO", font=TITLE_FONT)
        self.tempTitle.place(relx=0.5, rely=0, anchor = tk.N)
