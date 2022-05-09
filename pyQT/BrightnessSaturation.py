import cv2
import numpy as np
from PyQt5.QtGui import QPixmap


class BrightnessSaturation:

    def __init__(self):
        self.testImg = cv2.imread('img.jpg')
        self.outTestImg = self.testImg
        self.hsvImg = cv2.cvtColor(self.testImg, cv2.COLOR_BGR2HSV)
        self.baseHue, self.baseSat, self.baseValue = cv2.split(self.hsvImg)
        self.currHue = self.baseHue
        self.currSat = self.baseSat
        self.currValue = self.baseValue
        self.sliderHue = 0
        self.sliderSat = 0
        self.sliderValue = 0

    def brightnessChange(self, sliderNumber, mask):
        print(sliderNumber)
        self.sliderValue = sliderNumber
        mask.maskSettings.brightness = sliderNumber

        #ALL of this work below may be better handled in a different part of the code that is run whenever any update is detected?
        #Even if we have the current edited image this code completely redraws the current masked area and only updates brightness
        #So write a new overencompassing function that goes through each setting on each mask I guess?
        newValue = self.baseValue.copy()

        if sliderNumber > 0:
            limit = 255 - sliderNumber
            newValue[newValue > limit] = 255
            newValue[newValue <= limit] += sliderNumber
        else:
            limit = 0 + abs(sliderNumber)
            newValue[newValue < limit] = 0
            #This line of code cannot add negatives, so we force positive and subtract
            newValue[newValue >= limit] -= abs(sliderNumber)

        self.currValue = newValue
        after = cv2.merge((self.currHue, self.currSat, self.currValue))
        newImg = cv2.cvtColor(after, cv2.COLOR_HSV2BGR)

        maskImage = np.where(mask.maskArray == True, newImg, self.testImg)
        cv2.imwrite("edit.png", maskImage)


    def saturationChange(self, sliderNumber, mask):
        print(sliderNumber)
        self.sliderValue = sliderNumber
        mask.maskSettings.saturation = sliderNumber

        newSat = self.baseSat.copy()

        if sliderNumber > 0:
            limit = 255 - sliderNumber
            newSat[newSat > limit] = 255
            newSat[newSat <= limit] += sliderNumber
        else:
            limit = 0 + abs(sliderNumber)
            newSat[newSat < limit] = 0
            # This line of code cannot add negatives, so we force positive and subtract
            newSat[newSat >= limit] -= abs(sliderNumber)

        self.currSat = newSat
        after = cv2.merge((self.currHue, self.currSat, self.currValue))
        newImg = cv2.cvtColor(after, cv2.COLOR_HSV2BGR)

        maskImage = np.where(mask.maskArray == True, newImg, self.testImg)
        cv2.imwrite("edit.png", maskImage)