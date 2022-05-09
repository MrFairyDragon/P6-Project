import numpy as np
import matplotlib.pyplot as pl
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class curveTool:

    def __init__(self):
        print("ll")

    def valueChange(self, val1, val2, val3):
        if self.checkIfNumber(self, val1) and self.checkIfNumber(self, val2) and self.checkIfNumber(self, val3):
            fig = pl.figure()
            self.x = np.arange(0, 255, 0.1)
            self.y = (float(val1) * self.x ** 3) + (float(val2) * self.x ** 2) + (float(val3) * self.x)
            pl.plot(self.x, self.y)
            fig.savefig('plot.png')
            pl.close(fig)

    def checkIfNumber(self, var):
        if var is None:
            return False
        try:
            var2 = float(var)
            return True
        except:
            return False
