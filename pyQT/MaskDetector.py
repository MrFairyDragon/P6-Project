import cv2
import numpy as np
from ClassDict import *

# Functions


img = cv2.imread("input.jpg")  # image
mask_array = np.load('Image_mask.npy')
class_array = np.load('class_array.npy')

num_instances = mask_array.shape[0]
mask_array = np.moveaxis(mask_array, 0, -1)
mask_array_instance = []
output = np.zeros_like(img)
print (class_array)


for i in range(num_instances):
    j = class_array[i]+1
    k = coco_dict[j]
    print(coco_dict[j],"-",coco_dict[k] -1)


def list_class(array):
    pass
    return new_array


def filter_mask(image, mask_color):
    output = np.zeros_like(image)
    for i in range(num_instances):
        mask_array_instance.append(mask_array[:, :, i:(i + 1)])
        output = np.where(mask_array_instance[i] == True, mask_color, output)
    return output

def select_mask(image, mask_color,class_instnace,instance):
    output = np.zeros_like(image)
    for i in range(num_instances):
        mask_array_instance.append(mask_array[:, :, i:(i + 1)])
        for j in range(len(class_instnace)):
            for k in range(len(instance)):
                if class_instnace[j] -1== class_array[i] or instance[k] == i:

                    output = np.where(mask_array_instance[i] == True, mask_color, output)
    return output

def filter_blur(image, mask, str, background=True):
    blur = cv2.blur(image, (str, str))
    if background:
        blur = np.where(mask == 0, blur, image)
    else:
        blur = np.where(mask == 255, blur, image)
    return blur

mask = filter_mask(img, 255)

coco_class = [coco_dict['person'],coco_dict['umbrella']]
instance = [1,4]
all_masks = select_mask(img,255,coco_class ,instance)

imageblur = filter_blur(img, all_masks, 10, background = False)


cv2.imshow('mask', mask)
cv2.imshow('Blur', imageblur)
cv2.imshow('selected mask', all_masks)

cv2.waitKey(0)
cv2.destroyAllWindows()
