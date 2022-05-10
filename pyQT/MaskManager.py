import cv2

from pyQT.maskSelection import MaskSelection
from pyQT.BrightnessSaturation import BrightnessSaturation
from PyQt5.QtGui import QPixmap

import numpy as np
import timeit



class MaskManager:

    def __init__(self, imageLabels):

        self.baseImage = cv2.imread('img.jpg')
        self.currentImage = self.baseImage.copy()
        self.maskList, self.classList = MaskSelection().detectMasks()
        self.groupList = []

        self.selectedMask = self.maskList[0]
        self.selectedIsGroup = False
        self.brightnessSaturation = BrightnessSaturation()

        self.imageLabels = imageLabels

        self.drawTimer = timeit.default_timer()

    def DrawCurrentImage(self):

        drawingImg = self.baseImage.copy()
        for mask in self.maskList:

            groupSettings = []
            for cMask in self.classList:
                if cMask.maskList.__contains__(mask):
                    groupSettings.append(cMask.maskSettings)

            for gMask in self.groupList:
                if gMask.maskList.__contains__(mask):
                    groupSettings.append(gMask.maskSettings)

            totalBrightness = mask.maskSettings.brightness
            totalSaturation = mask.maskSettings.saturation

            for settings in groupSettings:
                totalBrightness += settings.brightness
                totalSaturation += settings.saturation

            drawingImg = self.brightnessSaturation.DrawBrightness(totalBrightness, drawingImg)
            drawingImg = self.brightnessSaturation.DrawSaturation(totalSaturation, drawingImg)

            drawingImg = np.where(self.selectedMask.maskArray == True, drawingImg, self.currentImage)

        cv2.imwrite('drawn.png', drawingImg)
        pixmap = QPixmap('drawn.png')
        for image in self.imageLabels:
            image.setPixmap(pixmap)
        self.currentImage = drawingImg

    # By only operating on the bounding box of the mask, this version gains a little speed
    def DrawMask(self, mask):
        drawingImg = self.baseImage.copy()[mask.minX:mask.maxX, mask.minY:mask.maxY]

        groupSettings = []
        for cMask in self.classList:
            if cMask.maskList.__contains__(mask):
                groupSettings.append(cMask.maskSettings)

        for gMask in self.groupList:
            if gMask.maskList.__contains__(mask):
                groupSettings.append(gMask.maskSettings)

        totalBrightness = mask.maskSettings.brightness
        totalSaturation = mask.maskSettings.saturation

        for settings in groupSettings:
            totalBrightness += settings.brightness
            totalSaturation += settings.saturation

        drawingImg = self.brightnessSaturation.DrawBrightness(totalBrightness, drawingImg)
        drawingImg = self.brightnessSaturation.DrawSaturation(totalSaturation, drawingImg)

        blankImg = self.baseImage.copy()
        blankImg[mask.minX:mask.maxX, mask.minY:mask.maxY] = drawingImg
        mergedImg = np.where(mask.maskArray == True, blankImg, self.currentImage)

        cv2.imwrite('drawn.png', mergedImg)
        pixmap = QPixmap('drawn.png')
        for imageLabel in self.imageLabels:
            imageLabel.setPixmap(pixmap)
        self.currentImage = mergedImg

    # This version is slightly slower than the new one
    def DrawMaskOLD(self, mask):
        drawingImg = self.baseImage.copy()

        groupSettings = []
        for cMask in self.classList:
            if cMask.maskList.__contains__(mask):
                groupSettings.append(cMask.maskSettings)

        for gMask in self.groupList:
            if gMask.maskList.__contains__(mask):
                groupSettings.append(gMask.maskSettings)

        totalBrightness = mask.maskSettings.brightness
        totalSaturation = mask.maskSettings.saturation

        for settings in groupSettings:
            totalBrightness += settings.brightness
            totalSaturation += settings.saturation

        drawingImg = self.brightnessSaturation.DrawBrightness(totalBrightness, drawingImg)
        drawingImg = self.brightnessSaturation.DrawSaturation(totalSaturation, drawingImg)

        mergedImg = np.where(mask.maskArray == True, drawingImg, self.currentImage)

        cv2.imwrite('drawn.png', mergedImg)
        pixmap = QPixmap('drawn.png')
        for UIimage in self.UIimageLabels:
            UIimage.setPixmap(pixmap)
        self.currentImage = mergedImg

    def DrawSelectedMask(self):
        if self.selectedIsGroup:
            for mask in self.selectedMask.maskList:
                self.DrawMask(mask)
        else:
            print("started drawing")
            self.DrawMask(self.selectedMask)
            print("completed drawing")

    def instanceDropDownChange(self, index):
        print("Selected instance: " + str(index))
        self.selectedMask = self.maskList[index]
        self.selectedIsGroup = False

    def classDropDownChange(self, index):
        print("Selected class: " + str(index))
        self.selectedMask = self.classList[index]
        self.selectedIsGroup = True

    def groupDropDownChange(self, index):
        print("Selected group: " + str(index))
        self.selectedIsGroup = True

    def brightnessChangeForce(self):
        self.DrawSelectedMask()

    def brightnessChange(self, sliderValue):
        self.selectedMask.maskSettings.brightness = sliderValue
        if timeit.default_timer() - self.drawTimer > .1:
            self.DrawSelectedMask()
            self.drawTimer = timeit.default_timer()

    def getCurrentBrightness(self):
        return self.selectedMask.maskSettings.brightness

    def saturationChangeForce(self):
        self.DrawSelectedMask()

    def saturationChange(self, sliderValue):
        self.selectedMask.maskSettings.saturation = sliderValue
        if timeit.default_timer() - self.drawTimer > .1:
            self.DrawSelectedMask()
            self.drawTimer = timeit.default_timer()

    def getCurrentSaturation(self):
        return self.selectedMask.maskSettings.saturation
