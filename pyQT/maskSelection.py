from pyQT import ClassDict
import cv2
import numpy as np
import random
from pyQT.Mask import Mask
import pyQT.MaskGroup


class MaskSelection():

    def __init__(self):
        self.mask_array = np.load('Image_mask.npy')
        self.class_array = np.load('class_array.npy')
        self.mask_array_instance = []
        self.num_instances = self.mask_array.shape[0]
        self.mask_array = np.moveaxis(self.mask_array, 0, -1)
        # print(self.class_array)
        # print(self.num_instances)
        # print(len(self.mask_array))

        self.maskList = []
        self.classList = []
        self.uniqueClasses = []


    def detectMasks(self):
        for i in range(self.num_instances):
            j = self.class_array[i] + 1
            #k = ClassDict.coco_dict[j]
            #print(ClassDict.coco_dict[j], "-", ClassDict.coco_dict[k] - 1)

            maskName = "" + str(i) + " - " + ClassDict.coco_dict[j]
            maskArray = self.mask_array[:, :, i:(i + 1)]
            maskImg = np.zeros_like(self.mask_array)
            maskImg = np.where(maskArray == True, 255, maskImg)
            self.maskList.append(Mask(maskArray, maskImg, maskName, ClassDict.coco_dict[j]))
            #cv2.imshow("hey:" + str(i), maskImg)

            if ClassDict.coco_dict[j] not in self.uniqueClasses:
                self.uniqueClasses.append(ClassDict.coco_dict[j])

        for uClass in self.uniqueClasses:
            maskGroup = pyQT.MaskGroup.MaskGroup(uClass, uClass)
            for mask in self.maskList:
                if mask.maskClass == uClass:
                    maskGroup.addMask(mask)
                    #print("Added mask of class: " + mask.maskClass + " to group of class: " + uClass)
            self.classList.append(maskGroup)

        return self.maskList, self.classList

    def make_outline_v1(self, image, k_size, maskList):
        outline = 0
        kernel = np.ones((k_size, k_size), np.uint8)
        for i in maskList:
            outlines = cv2.morphologyEx(i.maskImage, cv2.MORPH_GRADIENT, kernel)
            outlines = np.where(outlines >= 1,
                                (random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255)), 0)
            outline += outlines
        outline = np.where(outline >= 1, outline, image).astype(np.uint8)
        return outline


   # def make_outline_v2(self, mask, k_size, image):
    #    kernel = np.ones((k_size, k_size), np.uint8)
    #    output = np.zeros_like(mask)
    #    outline = 0
    #    for i in range(len(mask)):
    #        self.mask_array_instance.append(self.mask_array[:, :, i:(i + 1)])
    #        instance = np.where(self.mask_array_instance[i] == True, 255, output)
    #        outlines = cv2.morphologyEx(instance, cv2.MORPH_GRADIENT, kernel)
    #        outlines = np.where(outlines >= 254,
    #                            (random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255)), 0)
    #        outline += outlines
    #    outline = np.where(outline >= 1, outline, image)
    #    return outline

