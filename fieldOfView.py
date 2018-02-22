import tkinter as tk   # python3
import numpy as np
import os
from astropy.io import fits

class FieldOfView(object):

    def __init__(self, app, master):
        self._app = app
        self.fovCanvas = tk.Canvas(master, bg="blue", height=250, width=300)
        self.fovCanvas.place(relx=0.05, rely=0.1)

    def createFits():
        # This function will create the fits file which will be shown in the Field of field of view
        # The data will be calculated using source information input by the user

        # fake data until real data can be created
        data = np.arrange(100.0)
        hdu = fits.PrimaryHDU(data)
        hdu.writeto('fieldOfView.fits')
