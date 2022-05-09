import numpy as np
from pyQT.maskSetting import maskSetting


class mask(maskSetting):

    def __init__(self):
        self.array = np.ndarray(shape=(3, 3, 3))
        maskSetting.red = 2
