from pyQT import ClassDict
from pyQT.MaskSettings import MaskSettings
import cv2
import numpy as np
import pyQT.ClassDict
from pyQT.Mask import Mask
from pyQT.MaskGroup import MaskGroup


class MaskSelection():

    def detectMasks(self):
        print("trying to detect masks")
        testImg = cv2.imread("img.jpg")
        self.mask_array = np.load('Image_mask.npy')
        self.class_array = np.load('class_array.npy')

        self.num_instances = self.mask_array.shape[0]
        self.mask_array = np.moveaxis(self.mask_array, 0, -1)
        #print(self.class_array)
        #print(self.num_instances)
        #print(len(self.mask_array))

        maskList = []
        classList = []
        uniqueClasses = []

        for i in range(self.num_instances):
            j = self.class_array[i] + 1
            #k = ClassDict.coco_dict[j]
            #print(ClassDict.coco_dict[j], "-", ClassDict.coco_dict[k] - 1)

            maskName = "" + str(i) + " - " + ClassDict.coco_dict[j]
            maskArray = self.mask_array[:, :, i:(i + 1)]
            maskImg = np.zeros_like(testImg)
            maskImg = np.where(maskArray == True, 255, maskImg)
            maskList.append(Mask(maskArray, maskImg, maskName, ClassDict.coco_dict[j]))
            #cv2.imshow("hey:" + str(i), maskImg)

            if ClassDict.coco_dict[j] not in uniqueClasses:
                uniqueClasses.append(ClassDict.coco_dict[j])

        for uClass in uniqueClasses:
            maskGroup = MaskGroup(uClass, uClass)
            for mask in maskList:
                if mask.maskClass == uClass:
                    maskGroup.addMask(mask)
                    #print("Added mask of class: " + mask.maskClass + " to group of class: " + uClass)
            classList.append(maskGroup)

        return maskList, classList

