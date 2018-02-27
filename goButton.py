import tkinter as tk   # python3
GO_FONT = ("Helvetica", 20, "bold")

class GoButton(object):

    def __init__(self, app, master):
        self._app = app
        self.go = tk.Button(master, text="GO!", font=GO_FONT, command=self.goClick)
        self.go.place(relx=0.8, rely=0.9)

    def goClick(self):
        self._app.runMAESTRO(self)
