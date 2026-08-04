########################### PhotoGramatory ###########################
#############   Make image consisting of many images #################
#########          Created by Arjith SR                   ############

import cv2
import math
import glob
import numpy as np
import os
import datetime

final_path = r"C:\Users\This PC\Desktop\Path\required.jpg"  # Full Path of required image
folder_path = r"C:\Users\This PC\Desktop\Path\*.jpg"        # Full Path of folder containing all images
output_directory = r"C:\Users\This PC\Desktop"              # Output folder

final_size = 70  # Sampling size of your required image (default = 50)
size = 100       # Sampling size your small images (default = 100)
small_size = 50  # Final resolution of small images that will be displayed (default = 50)

print("Created by Arjith SR")
value_pair = {}
print("Analysing The Folder")
for img_path in glob.iglob(folder_path):
    img = cv2.imread(img_path)
    img_y = len(img)
    img_x = len(img[0])
    if img_y > img_x:
        img_y = img_x
    elif img_y < img_x:
        img_x = img_y
    img = img[0:img_x, 0:img_y]
    img = cv2.resize(img, (size, size))
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    v = 0
    value = 0
    count = 0
    for j in range(len(grey)):
        for i in range(len(grey[0])):
            v = grey[j, i]
            value += int(v)**2
            count += 1
    avg_v = math.sqrt(value/count)
    value_pair.update({img_path: avg_v})

key = list(value_pair.keys())
value = list(value_pair.values())

print('Correcting your photo')

final_img = cv2.imread(final_path)
if len(final_img) > len(final_img[0]):
    final_img = cv2.resize(final_img, (final_size, round(final_size*(len(final_img)/len(final_img[0])))))
elif len(final_img) < len(final_img[0]):
    final_img = cv2.resize(final_img, (round(final_size*(len(final_img[0])/len(final_img))), final_size))
final_img = cv2.cvtColor(final_img, cv2.COLOR_BGR2GRAY)

rendered = []
req_v = 0
diff = 1000
final_diff = 1000
nearest_value = 0

print('Attaching them')
final_render = []
final_horizontal = []

for j in range(len(final_img)):

    for i in range(len(final_img[0])):
        req_v = final_img[j, i]
        final_diff = 1000
        for values in value:
            diff = math.sqrt((req_v - values)**2)
            if diff < final_diff:
                final_diff = diff
                nearest_value = values
        index = value.index(nearest_value)
        item = key[index]
        small_img = cv2.imread(item)
        small_img_y = len(small_img)
        small_img_x = len(small_img[0])
        if small_img_y > small_img_x:
            small_img_y = small_img_x
        elif small_img_y < small_img_x:
            small_img_x = small_img_y
        small_img = small_img[0:small_img_x, 0:small_img_y]
        small_img = cv2.resize(small_img, (small_size, small_size))
        small_img = cv2.cvtColor(small_img, cv2.COLOR_BGR2GRAY)
        if i == 0:
            final_horizontal = small_img
        else:
            final_horizontal = np.hstack((final_horizontal, small_img))

    if j == 0:
        final_render = final_horizontal
    else:
        final_render = np.vstack((final_render, final_horizontal))
    print("Doing my work ", round(j/len(final_img)*100), '%')

cv2.imshow('Render', final_render)
cv2.waitKey(0)
os.chdir(output_directory)
filename = 'Picture_made_of_Pictures_' +\
           str(datetime.datetime.now().second) + \
           str(datetime.datetime.now().microsecond) + '.jpg'
cv2.imwrite(filename, final_render)
print("Done! Your image has been saved to the specified folder")
print("Created by Arjith SR")
print("Github: https://github.com/arjith2328")
