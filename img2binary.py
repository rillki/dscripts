#!/usr/bin/env python3
import os
import sys
import cv2 as cv
import numpy as np

# default values
imgs_folder = ''
output_folder = ''

# get arguments
argv = sys.argv[1:]
if len(argv) < 2:
    print("\n#img2binary: img2binary.py [imgs_folder] [output_folder]\n")
    sys.exit()
else:
    imgs_folder = argv[0]
    output_folder = argv[1]

# find all images
imgs = [i for i in os.listdir(os.path.join(".", imgs_folder)) if '.jpg' in i or '.jpeg' in i or '.JPEG' in i or '.JPG' in i]

for i in imgs:
    # open image
    img = cv.imread(os.path.join('.', imgs_folder, i), cv.IMREAD_GRAYSCALE)

    # convert to binary
    thresh, img = cv.threshold(img, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

    # save image
    cv.imwrite(os.path.join('.', output_folder, i), img)

    # verbose output
    print(f"#imgresize: <{i}> converted!")







