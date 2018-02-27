import tkinter as tk   # python3
import numpy as np
import os
from astropy.io import fits

class FieldOfView(object):

    def __init__(self, app, master):
        self._app = app
        self.fovCanvas = tk.Canvas(master, bg="blue", height=250, width=300)
        self.fovCanvas.place(relx=0.05, rely=0.1)

    def createFits(self):
        # This function will create the fits file which will be shown in the Field of field of view
        # The data will be calculated using source information input by the user

        # fake data until real data can be created
        data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], np.int32)
        hdu = fits.PrimaryHDU(data)

        hdu.writeto('test.fits', overwrite=True)
