import cv2
import numpy as np
from pyQT.ClassDict import *
import random

# Inputs from detectron
img = cv2.imread("img.jpg")  # image
mask_array = np.load('Image_mask.npy')
class_array = np.load('class_array.npy')


# variables
num_instances = mask_array.shape[0]
mask_array = np.moveaxis(mask_array, 0, -1)
mask_array_instance = []
print(random.randrange(1,20))

for i in range(num_instances):
    j = class_array[i] + 1
    k = coco_dict[j]
    print(coco_dict[j], "-", coco_dict[k] - 1)



def filter_mask(image, mask_color):
    output = np.zeros_like(image)
    for i in range(num_instances):
        mask_array_instance.append(mask_array[:, :, i:(i + 1)])
        output = np.where(mask_array_instance[i] == True, mask_color, output)
    return output


def make_outline_v1(mask, k_size):
    kernel = np.ones((k_size, k_size), np.uint8)
    outline = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)
    outline = np.where(outline == 255, 255, img)
    return outline

def make_outline_v2(mask,k_size):
    kernel = np.ones((k_size, k_size), np.uint8)
    output = np.zeros_like(mask)
    outline = 0
    for i in range(num_instances):
        mask_array_instance.append(mask_array[:, :, i:(i + 1)])
        instance = np.where(mask_array_instance[i] == True, 255, output)
        outlines = cv2.morphologyEx(instance, cv2.MORPH_GRADIENT, kernel)
        outlines = np.where(outlines >= 254, (random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255)), 0)
        outline += outlines
    outline = np.where(outline >= 1, outline, img)
    return outline

def select_mask(image, mask_color, class_instnace, instance):
    output = np.zeros_like(image)
    for i in range(num_instances):
        mask_array_instance.append(mask_array[:, :, i:(i + 1)])
        for j in range(len(class_instnace)):
            for k in range(len(instance)):
                if class_instnace[j] - 1 == class_array[i] or instance[k] == i:
                    output = np.where(mask_array_instance[i] == True, mask_color, output)
    return output


def filter_blur(image, mask, str, background=True):
    blur = cv2.blur(image, (str, str))
    if background:
        blur = np.where(mask == 0, blur, image)
    else:
        blur = np.where(mask == 255, blur, image)
    return blur

#parameters for selected masks
coco_class = [coco_dict['person']]
coco_class = [coco_dict['background']]
instance = [0, 1]

#masks filters
mask = filter_mask(img, 255) #all masks
selected_mask = select_mask(img, 255, coco_class, instance)
outline_v1 = make_outline_v1(mask, 3)
outline_v2 = make_outline_v2(mask, 3)

# Blur filter
imageblur = filter_blur(img, mask, 10, background=False)

show = False

if show:
    cv2.imshow('outline_v1', outline_v1)
    cv2.imshow('outline_v2',outline_v2)


    cv2.imshow('all_mask', mask)
    cv2.imshow('Blur', imageblur)
    cv2.imshow('selected_mask', selected_mask)

else:
    cv2.imwrite('outline_v1.jpg', outline_v1)
    cv2.imwrite('outline_v2.jpg', outline_v2)
    cv2.imwrite('all_mask.jpg', mask)
    cv2.imwrite('Blur.jpg', imageblur)
    cv2.imwrite('selected_mask.jpg', selected_mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
