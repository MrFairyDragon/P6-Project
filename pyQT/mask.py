import cv2
import numpy as np
from pyQT.MaskSettings import MaskSettings


class Mask:

    def __init__(self, array, img, name, maskClass):
        self.maskSettings = MaskSettings()
        self.maskName = name
        self.maskClass = maskClass
        self.maskImage = img
        self.maskArray = array


        where = np.where(img)
        x1, y1, z1 = np.amin(where, axis=1)
        x2, y2, z2 = np.amax(where, axis=1)

        self.minX = x1
        self.minY = y1
        self.maxX = x2
        self.maxY = y2

        self.boundedImage = img[self.minX:self.maxX, self.minY:self.maxY]
        #cv2.imshow(name, self.boundedImage)
