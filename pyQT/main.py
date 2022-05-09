import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QSlider, QTabWidget, QComboBox, QLineEdit, \
    QPushButton, QCheckBox
from PyQt5.QtWidgets import QApplication

import cv2
from pyQT.MaskManager import MaskManager
from pyQT.maskSelection import MaskSelection
from pyQT.kernel import Kernel
from pyQT.curveTool import curveTool
from pyQT.BrightnessSaturation import BrightnessSaturation

class UI:

    def TabSwitch(self, index):
        if index == 0:
            print("Switched to Mask tab")
        if index == 1:
            print("Switched to Saturation/Brightness tab")
            self.sliderBrightness.setSliderPosition(self.maskManager.getCurrentBrightness())
        if index == 2:
            print("Switched to CurveTool tab")
        if index == 3:
            print("Switched to Kernel tab")

    def updateButton(self):
        self.mathpixmap = QPixmap('plot.png')
        self.labelmathpixmap.setPixmap(self.mathpixmap)
        self.window.update()

    def updateWindow(self):
        self.pixmap = QPixmap('edit.png')
        for i in self.imageLabel:
            i.setPixmap(self.pixmap)
        self.cvimage = cv2.imread('edit.png')
        self.cvmask = cv2.imread('selected_mask.jpg')
        self.window.update()

    def __init__(self):
        cvmainimage = cv2.imread('img.jpg')
        cv2.imwrite('edit.png', cvmainimage)
        self.cvimage = cv2.imread('edit.png')
        self.cvmask = cv2.imread('selected_mask.jpg')
        app = QApplication(sys.argv)
        self.maskSelection = MaskSelection()
        self.kernel = Kernel()
        self.curveTool = curveTool()
        self.brigtnessSaturation = BrightnessSaturation()
        self.window = QWidget()
        imgSettingLayout = [QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout()]
        settingLayout = [QVBoxLayout(), QVBoxLayout(), QVBoxLayout(), QVBoxLayout()]
        self.imageLabel = [QLabel(), QLabel(), QLabel(), QLabel()]
        pixmap = QPixmap('img.jpg')
        tabWindow = QTabWidget()
        tabMask = QWidget()
        tabSlider = QWidget()
        tabCurve = QWidget()
        tabKernel = QWidget()
        tabLayout = QVBoxLayout()

        self.maskManager = MaskManager()
        tabWindow.currentChanged.connect(self.TabSwitch)

        # Tab1
        labelList = QLabel("item1\nitem2")
        labelInstance = QLabel("Instance Selection")
        labelInstance.setFixedWidth(200)
        dropdownInstance = QComboBox()
        labelClasses = QLabel("Classes")
        dropdownClasses = QComboBox()
        labelGroups = QLabel("Groups")
        dropdownGroups = QComboBox()
        dropdownGroups.addItem("item1")
        dropdownGroups.addItem("item2")
        labelSelectedMasksList = QLabel("SelectedMasks")
        settingLayout[0].setAlignment(Qt.AlignmentFlag.AlignTop)
        settingLayout[0].addWidget(labelInstance)
        dropdownInstance.addItem("item1")
        dropdownInstance.addItem("item2")
        settingLayout[0].addWidget(dropdownInstance)
        settingLayout[0].addWidget(labelClasses)
        dropdownClasses.addItem("item1")
        dropdownClasses.addItem("item2")
        settingLayout[0].addWidget(dropdownClasses)
        settingLayout[0].addWidget(labelGroups)
        settingLayout[0].addWidget(dropdownGroups)
        settingLayout[0].addWidget(labelSelectedMasksList)
        settingLayout[0].addWidget(labelList)

        # Tab2
        labelBrightness = QLabel("Brightness")
        self.sliderBrightness = QSlider(Qt.Orientation.Horizontal)
        self.sliderBrightness.setMinimum(-255)
        self.sliderBrightness.setMaximum(255)
        self.sliderBrightness.setSliderPosition(0)

        labelSaturation = QLabel("Saturation")
        sliderSaturation = QSlider(Qt.Orientation.Horizontal)
        sliderSaturation.setMinimum(-255)
        sliderSaturation.setMaximum(255)
        sliderSaturation.setSliderPosition(0)
        settingLayout[1].setAlignment(Qt.AlignmentFlag.AlignTop)
        settingLayout[1].addWidget(labelBrightness)
        settingLayout[1].addWidget(self.sliderBrightness)
        settingLayout[1].addWidget(labelSaturation)
        settingLayout[1].addWidget(sliderSaturation)

        self.sliderBrightness.valueChanged.connect(self.maskManager.brightnessChange)
        self.sliderBrightness.valueChanged.connect(self.updateWindow)
        sliderSaturation.valueChanged.connect(self.maskManager.saturationChange)
        sliderSaturation.valueChanged.connect(self.updateWindow)

        # Tab3
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
            lineEditValue[i].textChanged.connect(lambda: curveTool.valueChange(curveTool, lineEditValue[0].text(), lineEditValue[1].text(), lineEditValue[2].text()))
        settingLayout[2].setAlignment(Qt.AlignmentFlag.AlignTop)
        self.mathpixmap = QPixmap('plot.png')
        self.labelmathpixmap = QLabel()
        self.labelmathpixmap.setPixmap(self.mathpixmap)
        settingLayout[2].addWidget(self.labelmathpixmap)
        curveButton = QPushButton("Update")
        settingLayout[2].addWidget(curveButton)
        curveButton.clicked.connect(self.updateButton)

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
        labelKernel = QLabel("Kernel Intensity")
        sliderKernel = QSlider(Qt.Orientation.Horizontal)
        settingLayout[3].addWidget(labelKernel)
        settingLayout[3].addWidget(sliderKernel)
        sliderKernel.setMinimum(1)
        sliderKernel.setMaximum(10)
        sliderKernel.valueChanged.connect(lambda: kernel.filter_blur(self.cvimage, self.cvmask, sliderKernel.value(), lineEditValue2.checkState()))
        sliderKernel.valueChanged.connect(self.updateWindow)
        #lineEditValue1.stateChanged.connect(kernel.doBackground)
        #lineEditValue2.stateChanged.connect(kernel.doBlur)

        # Tabs
        tabWindow.addTab(tabMask, "Mask")
        tabWindow.addTab(tabSlider, "Adjustments")
        tabWindow.addTab(tabCurve, "CurveTool")
        tabWindow.addTab(tabKernel, "Kernels")

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
            i.setPixmap(pixmap)

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

