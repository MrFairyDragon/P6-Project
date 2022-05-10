import cv2

from pyQT.maskSelection import MaskSelection
from pyQT.BrightnessSaturation import BrightnessSaturation

class MaskManager:

    def __init__(self):

        self.maskList, self.classList = MaskSelection().detectMasks()
        self.groupList = []

        self.selectedMask = self.maskList[0]
        self.brightnessSaturation = BrightnessSaturation()
        self.imageRecord = []

    def DrawCurrentImage(self):

        print("Draw current")
        for mask in self.maskList:

            groupSettings = []
            for cMask in self.classList:
                if cMask.maskList.__contains__(mask):
                    groupSettings.append(cMask.maskSettings)

            for gMask in self.groupList:
                if gMask.maskList.__contains__(mask):
                    groupSettings.append(gMask.maskSettings)
            print("nested loops done")

            totalBrightness = mask.maskSettings.brightness
            for settings in groupSettings:
                totalBrightness += settings.brightness
            print(str(mask.maskSettings.brightness) + " --> " + str(totalBrightness))

        #Loop through all individual masks (instances)
        #Nested loop through classes to check for changes there
        #Also nested loop through groups to check any that include this mask

        #Combine all the effects for each individual mask
        #Call a function on the mask class that returns the manipulated image?
        #Repeat until all masks have applied all their edits



    def instanceDropDownChange(self, index):
        print("Selected instance: " + str(index))
        self.selectedMask = self.maskList[index]
        self.groupList.append(self.maskList[index])

    def classDropDownChange(self, index):
        print("Selected class: " + str(index))
        self.selectedMask = self.classList[index]
        self.groupList.append(self.classList[index])

    def groupDropDownChange(self, index):
        print("Selected group: " + str(index))
        self.DrawCurrentImage()

    def brightnessChange(self, sliderValue):
        self.brightnessSaturation.brightnessChange(sliderValue, self.selectedMask)
        print(sliderValue)

    def getCurrentBrightness(self):
        return self.selectedMask.maskSettings.brightness

    def saturationChange(self, sliderValue):
        self.brightnessSaturation.saturationChange(sliderValue, self.selectedMask)
        print(sliderValue)


    def getImageRecord(self):
        return self.imageRecord