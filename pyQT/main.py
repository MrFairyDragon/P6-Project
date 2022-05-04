import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QSlider, QTabWidget, QComboBox, QLineEdit, \
    QCheckBox
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    # Widget Initialization
    application = QApplication(sys.argv)
    window = QWidget()
    imgSettingLayout = [QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout()]
    settingLayout = [QVBoxLayout(), QVBoxLayout(), QVBoxLayout(), QVBoxLayout()]
    imageLabel = [QLabel(), QLabel(), QLabel(), QLabel()]
    pixmap = QPixmap('Sigi_Banner.png')
    tabWindow = QTabWidget()
    tabMask = QWidget()
    tabSlider = QWidget()
    tabCurve = QWidget()
    tabKernel = QWidget()
    tabLayout = QVBoxLayout()

    # Tab1
    labelList = QLabel("item1\nitem2")
    labelInstance = QLabel("Instance Selection")
    labelInstance.setFixedWidth(200)
    dropdownInstance = QComboBox()
    labelClasses = QLabel("Classes")
    dropdownClasses = QComboBox()
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
    settingLayout[0].addWidget(labelSelectedMasksList)
    settingLayout[0].addWidget(labelList)

    # Tab2
    labelBrightness = QLabel("Brightness")
    sliderBrightness = QSlider(Qt.Orientation.Horizontal)
    labelSaturation = QLabel("Saturation")
    sliderSaturation = QSlider(Qt.Orientation.Horizontal)
    settingLayout[1].setAlignment(Qt.AlignmentFlag.AlignTop)
    settingLayout[1].addWidget(labelBrightness)
    settingLayout[1].addWidget(sliderBrightness)
    settingLayout[1].addWidget(labelSaturation)
    settingLayout[1].addWidget(sliderSaturation)

    # Tab3
    for i in range(3):
        layoutValue = QHBoxLayout()
        labelValue = QLabel("Value " + str(i + 1))
        lineEditValue = QLineEdit()
        layoutValue.addWidget(labelValue)
        layoutValue.addWidget(lineEditValue)
        settingLayout[2].addLayout(layoutValue)
    settingLayout[2].setAlignment(Qt.AlignmentFlag.AlignTop)

    # Tab4
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

    # layout.addWidget(slider)
    # layout.addWidget(textBox)

    # Event Function Calls
    # greetButton.clicked.connect(greet)
    # slider.valueChanged.connect(changeImage)

    # Window manipulation
    window.setWindowTitle("PYQT")
    window.setGeometry(100, 100, 800, 500)
    window.setLayout(tabLayout)
    window.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
    window.show()
    window.setFixedSize(window.size())
    sys.exit(application.exec_())