import numpy as np
from pyQT.MaskSettings import MaskSettings


class Mask:

    def __init__(self, array, img, name, maskClass):
        self.maskSettings = MaskSettings()
        self.maskName = name
        self.maskClass = maskClass
        self.maskImage = img
        self.maskArray = array
