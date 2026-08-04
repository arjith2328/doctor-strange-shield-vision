
########################### PhotoGramatory ###########################
#############   Make image consisting of many images #################
#########          Created by Arjith SR                   ############

import cv2
import math
import glob
import numpy as np
import os
import sys
import datetime

final_path = r"C:\Users\This PC\Desktop\required.jpg"    # Full Path of required image
folder_path = r"C:\Users\This PC\Desktop\Pictures\*jpg"  # Full Path of folder containing all images
output_directory = r"C:\Users\This PC\Desktop"           # Output folder

final_size = 60  # Sampling size of your required image (default = 50)
size = 70       # Sampling size your small images (default = 100)
small_size = 50  # Final resolution of small images that will be displayed (default = 50)

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
value_pair = {}
print("Created by Arjith SR")
print("Analysing The Folder")
paths = glob.glob(folder_path)
paths = paths[:40]
for i, img_path in enumerate(paths):
    img = cv2.imread(img_path)
    img_y = len(img)
    img_x = len(img[0])
    if img_y > img_x:
        img_y = img_x
    elif img_y < img_x:
        img_x = img_y
    img = img[0:img_x, 0:img_y]
    img = cv2.resize(img, (size, size))
    img = img.reshape((img.shape[0]*img.shape[1]), 3)
    count = len(img)
    colour = img.sum(axis=0)
    avg_c = colour/count
    avg_c = avg_c.astype(int)
    value_pair.update({img_path: avg_c})
    progress(i, len(paths))

key = list(value_pair.keys())
value = list(value_pair.values())

print('Correcting your photo')

final_img = cv2.imread(final_path)
if len(final_img) > len(final_img[0]):
    final_img = cv2.resize(final_img, (final_size, round(final_size*(len(final_img)/len(final_img[0])))))
elif len(final_img) < len(final_img[0]):
    final_img = cv2.resize(final_img, (round(final_size*(len(final_img[0])/len(final_img))), final_size))

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
        req_v = final_img[j][i]
        final_diff = 1000
        index = 0
        for idx, values in enumerate(value):
            diff = req_v - values
            diff = diff**2
            diff = np.sum(diff)
            diff = math.sqrt(diff)
            if diff < final_diff:
                final_diff = diff
                nearest_value = values
                index = idx
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
    progress(j, len(final_img))
    # print("Doing my work ", round(j/len(final_img)*100), '%')

cv2.imshow('Render', final_render)
cv2.waitKey(0)
os.chdir(output_directory)
filename = 'Picture_made_of_Pictures_' +\
           str(datetime.datetime.now().second) + \
           str(datetime.datetime.now().microsecond) + '.jpg'
cv2.imwrite(filename, final_render)
print('Image Successfully saved at the specified folder')

print("Created by Arjith SR")
print("Github: https://github.com/arjith2328")
