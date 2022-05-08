import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QSlider, QTabWidget, QComboBox, QLineEdit, \
    QCheckBox
from PyQt5.QtWidgets import QApplication
from pyQT.MaskManager import MaskManager
from pyQT.Kernel import Kernel
from pyQT.CurveTool import CurveTool
from pyQT.BrightnessSaturation import BrightnessSaturation

class UImain:

    def SetupUI(self):
        application = QApplication(sys.argv)
        window = QWidget()
        imgSettingLayout = [QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout()]
        settingLayout = [QVBoxLayout(), QVBoxLayout(), QVBoxLayout(), QVBoxLayout()]
        imageLabel = [QLabel(), QLabel(), QLabel(), QLabel()]
        pixmap = QPixmap('img.jpg')
        tabWindow = QTabWidget()
        tabLayout = QVBoxLayout()
        tabMask = QWidget()
        tabSlider = QWidget()
        tabCurve = QWidget()
        tabKernel = QWidget()

        self.maskManager = MaskManager()
        tabWindow.currentChanged.connect(self.TabSwitch)

        # Tab1
        labelInstance = QLabel("Instance Selection")
        labelInstance.setFixedWidth(200)
        dropdownInstance = QComboBox()
        for mask in self.maskManager.maskList:
            dropdownInstance.addItem(mask.maskName)
        dropdownInstance.activated.connect(self.maskManager.instanceDropDownChange)

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

        labelSelectedMasksList = QLabel("SelectedMasks")
        labelList = QLabel("item1\nitem2")

        settingLayout[0].setAlignment(Qt.AlignmentFlag.AlignTop)
        settingLayout[0].addWidget(labelInstance)
        settingLayout[0].addWidget(dropdownInstance)
        settingLayout[0].addWidget(labelClasses)
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
        sliderSaturation.valueChanged.connect(self.maskManager.saturationChange)

        # Tab3
        curveTool = CurveTool()
        for i in range(3):
            layoutValue = QHBoxLayout()
            labelValue = QLabel("Value " + str(i + 1))
            lineEditValue = QLineEdit()
            layoutValue.addWidget(labelValue)
            layoutValue.addWidget(lineEditValue)
            lineEditValue.textChanged.connect(curveTool.valueChange)
            settingLayout[2].addLayout(layoutValue)
        settingLayout[2].setAlignment(Qt.AlignmentFlag.AlignTop)

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
        sliderKernel.valueChanged.connect(kernel.intensityChange)
        lineEditValue1.stateChanged.connect(kernel.doBackground)
        lineEditValue2.stateChanged.connect(kernel.doBlur)

        # Tabs
        tabWindow.addTab(tabMask, "Mask")
        tabWindow.addTab(tabSlider, "Adjustments")
        tabWindow.addTab(tabCurve, "CurveTool")
        tabWindow.addTab(tabKernel, "Kernels")

        # Layout
        for i in range(len(imgSettingLayout)):
            imgSettingLayout[i].addWidget(imageLabel[i])
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

        for i in imageLabel:
            i.setPixmap(pixmap)

        # Window manipulation
        window.setWindowTitle("PYQT")
        window.setGeometry(100, 100, 800, 500)
        window.setLayout(tabLayout)
        window.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        window.show()
        window.setFixedSize(window.size())
        sys.exit(application.exec_())

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

if __name__ == '__main__':
    UImain().SetupUI()