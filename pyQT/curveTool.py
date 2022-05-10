import numpy as np
import matplotlib.pyplot as pl
import cv2


class curveTool:

    def __init__(self):
        print("ll")

    def SToneCurve(self, image, mask):
        look_up_table = np.zeros((256, 1), dtype='uint8')
        for i in range(256):
            look_up_table[i][0] = 255 * (np.sin(np.pi * (i / 255 - 1 / 2)) + 1) / 2
        lutImg = np.zeros_like(image)
        lut = cv2.LUT(image, look_up_table, lutImg)
        lutMask = np.where(mask.maskArray == True, lut, image)
        cv2.imwrite("edit.png", lutMask)

    def valueChange2(self, val1, val2, val3, mask, image):
        if self.checkIfNumber(self, val1) and self.checkIfNumber(self, val2) and self.checkIfNumber(self, val3):
            fig = pl.figure()
            self.x = np.arange(0, 255, 0.1)
            self.y = (float(val1) * self.x ** 3) + (float(val2) * self.x ** 2) + (float(val3) * self.x)
            pl.plot(self.x, self.y)
            fig.savefig('plot.png')
            pl.close(fig)
            editImage = np.clip(self.convertValue(self, image, val1, val2, val3), 0, 255)
            maskImage = np.where(mask.maskArray == True, editImage, image)
            cv2.imwrite("edit.png", maskImage)
            cv2.imwrite("noBlur.png", maskImage)

    def valueChange(self, val1, val2, val3, channel, mask, image):
        if self.checkIfNumber(self, val1) and self.checkIfNumber(self, val2) and self.checkIfNumber(self, val3):
            fig = pl.figure()
            self.x = np.arange(0, 255, 0.1)
            self.y = (float(val1) * self.x ** 3) + (float(val2) * self.x ** 2) + (float(val3) * self.x)
            pl.plot(self.x, self.y)
            fig.savefig('plot.png')
            pl.close(fig)
            newImage = image.copy()
            b, g, r = cv2.split(newImage)
            if channel == "Blue":
                b = np.clip(self.convertValue(self, b, val1, val2, val3), 0, 255)
            elif channel == "Green":
                g = np.clip(self.convertValue(self, g, val1, val2, val3), 0, 255)
            elif channel == "Red":
                r = np.clip(self.convertValue(self, r, val1, val2, val3), 0, 255)
            else:
                return
            print("test")
            editImage = cv2.merge((b, g, r))
            maskImage = np.where(mask.maskArray == True, editImage, image)
            cv2.imwrite("edit.png", maskImage)
            cv2.imwrite("noBlur.png", maskImage)

    def checkIfNumber(self, var):
        if var is None:
            return False
        try:
            var2 = float(var)
            return True
        except:
            return False

    def convertValue(self, value, val1, val2, val3):
        #out = value.copy()
        #with np.nditer(value, op_flags=['readwrite']) as it:
        #    for x in it:
        #        x[...] = (float(val1) * x ** 3) + (float(val2) * x ** 2) + (float(val3) * x)
        #return out
        look_up_table = np.zeros((256, 1), dtype='uint8')
        for i in range(256):
            look_up_table[i][0] = (float(val1) * i ** 3) + (float(val2) * i ** 2) + (float(val3) * i)
            lutImg = np.zeros_like(value)
            lut = cv2.LUT(value, look_up_table, lutImg)
        return lut
