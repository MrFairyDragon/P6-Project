import sys
import numpy as np
import random
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QSlider, QTabWidget, QComboBox, QLineEdit, \
    QPushButton, QCheckBox, QFileDialog
from PyQt5.QtWidgets import QApplication

import cv2
from pyQT.MaskManager import MaskManager
from pyQT.maskSelection import MaskSelection
from pyQT.kernel import Kernel
from pyQT.curveTool import curveTool
from pyQT.BrightnessSaturation import BrightnessSaturation

class UI:

    #def load_image(self):
    #   path, _ = QFileDialog.getOpenFileName(None, "Load Image", "")
    # if path:
    #      self.load_file(path)
    #    self.pixmap =
    def save(self):
        cv2.imwrite("save.png", self.cvimage)

    #def showOutline(self):
     ##  kernel = np.ones((3, 3), np.uint8)
      #  print(len(self.maskManager.maskList))
      #  for i in self.maskManager.maskList:
      #      conv = i.maskImage.astype(np.uint8)
      #      outlines = cv2.morphologyEx(conv, cv2.MORPH_GRADIENT, kernel)
      #      outlines = np.where(outlines >= 1, 255, 0)
      #      outline += outlines
      #  outline = np.where(outline >= 1, outlines, np.tile(self.cvimage,(1,4))).astype(np.uint8)
      #  cv2.imshow('outline', outline)

    def TabSwitch(self, index):
        if index == 0:
            print("Switched to Mask tab")
        if index == 1:
            print("Switched to Saturation/Brightness tab")
            self.sliderBrightness.setSliderPosition(self.maskManager.getCurrentBrightness())
            self.sliderSaturation.setSliderPosition(self.maskManager.getCurrentSaturation())
        if index == 2:
            print("Switched to CurveTool tab")
        if index == 3:
            print("Switched to Kernel tab")

    def updateButton(self):
        self.mathpixmap = QPixmap('plot.png')
        self.labelmathpixmap.setPixmap(self.mathpixmap)
        self.window.update()

    def updateWindow(self):
        print("updating window")
        self.pixmap = QPixmap('edit.png')
        print("set to imagelabels")
        for i in self.imageLabel:
            i.setPixmap(self.pixmap)
        print("success")
        self.current_edit = cv2.imread("edit.png")
        self.cvimageNoBlur = cv2.imread('noBlur.png')
        self.window.update()
        print("updated window")

    def __init__(self):
        self.groupVerticalLayouts = []
        self.groupVerticalLabels = []
        self.groupVerticalButtons = []
        self.imageRecord = []
        cvmainimage = cv2.imread('img.jpg')
        cv2.imwrite('edit.png', cvmainimage)
        cv2.imwrite('noBlur.png', cvmainimage)
        self.cvimage = cv2.imread('edit.png')
        self.cvimageNoBlur = cv2.imread('noBlur.png')
        self.cvmask = cv2.imread('selected_mask.jpg')
        app = QApplication(sys.argv)
        self.maskSelection = MaskSelection()
        self.kernel = Kernel()
        self.curveTool = curveTool()
        self.brightnessSaturation = BrightnessSaturation()
        self.window = QWidget()
        saveFileButton = QPushButton()
        imgSettingLayout = [QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout()]
        settingLayout = [QVBoxLayout(), QVBoxLayout(), QVBoxLayout(), QVBoxLayout()]
        self.imageLabel = [QLabel(), QLabel(), QLabel(), QLabel()]
        self.pixmap = QPixmap('img.jpg')
        tabWindow = QTabWidget()
        tabMask = QWidget()
        tabSlider = QWidget()
        tabCurve = QWidget()
        tabKernel = QWidget()
        tabLayout = QVBoxLayout()

        self.maskManager = MaskManager(self.imageLabel)
        tabWindow.currentChanged.connect(self.TabSwitch)

        # Tab1
        labelInstance = QLabel("Instance Selection")
        labelInstance.setFixedWidth(200)
        dropdownInstance = QComboBox()
        for masks in self.maskManager.maskList:
            dropdownInstance.addItem(masks.maskName)
        dropdownInstance.activated.connect(self.maskManager.instanceDropDownChange)
        #dropdownInstance.activated.connect(self.updateList)

        labelClasses = QLabel("Classes")
        dropdownClasses = QComboBox()
        for maskClass in self.maskManager.classList:
            dropdownClasses.addItem(maskClass.groupName)
        dropdownClasses.activated.connect(self.maskManager.classDropDownChange)

        labelGroups = QLabel("Groups")
        dropdownGroups = QComboBox()
        dropdownGroups.addItem("item1")
        dropdownGroups.addItem("item2")
        dropdownGroups.activated.connect(self.maskManager.groupDropDownChange)

       # labelSelectedMasksList = QLabel("SelectedMasks")
        #labelList = QLabel("item1\nitem2")

        settingLayout[0].setAlignment(Qt.AlignmentFlag.AlignTop)
        settingLayout[0].addWidget(labelInstance)
        settingLayout[0].addWidget(dropdownInstance)
        settingLayout[0].addWidget(labelClasses)
        settingLayout[0].addWidget(dropdownClasses)
      #  settingLayout[0].addWidget(labelGroups)
       # settingLayout[0].addWidget(dropdownGroups)
        #settingLayout[0].addWidget(labelSelectedMasksList)
      #  settingLayout[0].addWidget(labelList)
        #settingLayout[0].addWidget(self.groupList)
       # addToListButton = QPushButton("Make Group")
       # saveFileButton.pressed.connect(self.save)
       # settingLayout[0].addWidget(addToListButton)
       # settingLayout[0].addWidget(saveFileButton)
        #maskOutlineButton = QPushButton("See outline for selected masks")
       # settingLayout[0].addWidget(maskOutlineButton)
       # maskOutlineButton.pressed.connect(self.showOutline)
        #settingLayout[0].addWidget(saveFileButton)
        #saveFileButton.pressed.connect(self.load_image)

        # Tab2
        labelBrightness = QLabel("Brightness")
        self.sliderBrightness = QSlider(Qt.Orientation.Horizontal)
        self.sliderBrightness.setMinimum(-255)
        self.sliderBrightness.setMaximum(255)
        self.sliderBrightness.setSliderPosition(0)

        labelSaturation = QLabel("Saturation")
        self.sliderSaturation = QSlider(Qt.Orientation.Horizontal)
        self.sliderSaturation.setMinimum(-255)
        self.sliderSaturation.setMaximum(255)
        self.sliderSaturation.setSliderPosition(0)
        settingLayout[1].setAlignment(Qt.AlignmentFlag.AlignTop)
        settingLayout[1].addWidget(labelBrightness)
        settingLayout[1].addWidget(self.sliderBrightness)
        settingLayout[1].addWidget(labelSaturation)
        settingLayout[1].addWidget(self.sliderSaturation)
        self.sliderBrightness.valueChanged.connect(self.maskManager.brightnessChange)
        self.sliderBrightness.sliderReleased.connect(self.maskManager.brightnessChangeForce)
        self.sliderSaturation.valueChanged.connect(self.maskManager.saturationChange)
        self.sliderSaturation.sliderReleased.connect(self.maskManager.saturationChangeForce)

        # Tab3
        colorChannelCurve = QComboBox()
        layoutValue = [QHBoxLayout(), QHBoxLayout(), QHBoxLayout()]
        labelValue = [None, None, None]
        lineEditValue = [None, None, None]
        for i in range(3):
            layoutValue[i] = QHBoxLayout()
            labelValue[i] = QLabel("Value " + str(i + 1))
            lineEditValue[i] = QLineEdit()
            layoutValue[i].addWidget(labelValue[i])
            layoutValue[i].addWidget(lineEditValue[i])
            settingLayout[2].addLayout(layoutValue[i])
        for i in range(3):
            lineEditValue[i].textChanged.connect(lambda: curveTool.valueChange(curveTool, lineEditValue[0].text(), lineEditValue[1].text(), lineEditValue[2].text(), colorChannelCurve.currentText(), self.maskManager.selectedMask, self.cvimageNoBlur))
            lineEditValue[i].textChanged.connect(self.updateWindow)
        settingLayout[2].setAlignment(Qt.AlignmentFlag.AlignTop)
        self.mathpixmap = QPixmap('plot.png')
        self.labelmathpixmap = QLabel()
        self.labelmathpixmap.setPixmap(self.mathpixmap)
        settingLayout[2].addWidget(self.labelmathpixmap)
        curveButton = QPushButton("Update")
        settingLayout[2].addWidget(curveButton)
        curveButton.clicked.connect(self.updateButton)
        settingLayout[2].addWidget(colorChannelCurve)
        colorChannelCurve.addItem("Green")
        colorChannelCurve.addItem("Blue")
        colorChannelCurve.addItem("Red")
        # Tab4
        kernel = Kernel()
        layoutValue1 = QHBoxLayout()
        labelValue1 = QLabel("Apply to Background")
        lineEditValue1 = QCheckBox()
        layoutValue1.addWidget(lineEditValue1)
        layoutValue1.addWidget(labelValue1)
        layoutValue1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        settingLayout[3].addLayout(layoutValue1)
        layoutValue2 = QHBoxLayout()
        labelValue2 = QLabel("Apply filter")
        lineEditValue2 = QCheckBox()
        layoutValue2.addWidget(lineEditValue2)
        layoutValue2.addWidget(labelValue2)
        layoutValue2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        settingLayout[3].addLayout(layoutValue2)
        settingLayout[3].setAlignment(Qt.AlignmentFlag.AlignTop)
        labelKernel = QLabel("Blur Intensity")
        sliderKernel = QSlider(Qt.Orientation.Horizontal)
        settingLayout[3].addWidget(labelKernel)
        settingLayout[3].addWidget(sliderKernel)
        sliderKernel.setMinimum(1)
        sliderKernel.setMaximum(10)
        sliderKernel.valueChanged.connect(lambda: kernel.filter_blur(self.cvimageNoBlur, self.maskManager.selectedMask, sliderKernel.value(), lineEditValue1.checkState(), lineEditValue2.checkState()))
        sliderKernel.valueChanged.connect(self.updateWindow)
        #lineEditValue1.stateChanged.connect(kernel.doBackground)
        #lineEditValue2.stateChanged.connect(kernel.doBlur)

        # Tabs
        tabWindow.addTab(tabMask, "Mask")
        tabWindow.addTab(tabSlider, "Adjustments")
        tabWindow.addTab(tabCurve, "CurveTool")
        tabWindow.addTab(tabKernel, "Blur")

        # Layout
        for i in range(len(imgSettingLayout)):
            imgSettingLayout[i].addWidget(self.imageLabel[i])
            imgSettingLayout[i].addLayout(settingLayout[i])

        tabLayout.addWidget(tabWindow)

        tabMask.layout = QVBoxLayout()
        tabMask.setLayout(imgSettingLayout[0])

        tabSlider.layout = QVBoxLayout()
        tabSlider.setLayout(imgSettingLayout[1])

        tabCurve.layout = QVBoxLayout()
        tabCurve.setLayout(imgSettingLayout[2])

        tabKernel.layout = QVBoxLayout()
        tabKernel.setLayout(imgSettingLayout[3])

        for i in self.imageLabel:
            i.setPixmap(self.pixmap)

        # Window manipulation
        self.window.setWindowTitle("PYQT")
        self.window.setGeometry(100, 100, 800, 500)
        self.window.setLayout(tabLayout)
        self.window.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.window.show()
        self.window.setFixedSize(self.window.size())
        sys.exit(app.exec_())


if __name__ == '__main__':
    ui = UI()

