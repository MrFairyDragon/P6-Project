from pyQT.maskSetting import maskSetting


class maskSelection():

    def __init__(self):
        self.maskList = []
        self.classList = []
        self.groupList = []
        self.getClassList()

    def groupDropDownChange(self, theGroup):
        print("Selected instance: " + theGroup)

    def instanceDropDownChange(self, theInstance):
        print("Selected instance: " + theInstance)

    def classDropDownChange(self, theClass):
        print("Selected class: " + theClass)

    def getClassList(self) -> []:
        print("test")