import cv2
import numpy as np

class Kernel:

    def __init__(self):
        self.mask = None
        self.str = None
        self.image = None
        self.background = False

    def filter_blur(self, image, mask, str, background):
        blur = cv2.blur(image, (str, str))
        if background:
            blur = np.where(mask == 0, blur, image)
        else:
            blur = np.where(mask == 255, blur, image)
        cv2.imwrite('edit.png', blur)




