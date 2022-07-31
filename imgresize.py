#!/usr/bin/env python3
import os
import sys
import cv2 as cv

# default values
imgs_folder = ''
output_folder = ''
width = 640
height = 640
inter = cv.INTER_AREA

# get arguments
argv = sys.argv[1:]
if len(argv) < 2:
    print("\n#imgresize: imgresize.py [imgs_folder] [output_folder] {width} {height} up/down\n")
    print("\n#imgresize: imgresize.py ../data ../data/tmp 1280 1080 up\n")
    sys.exit()
elif len(argv) == 2:
    imgs_folder = argv[0]
    output_folder = argv[1]
elif len(argv) == 3:
    imgs_folder = argv[0]
    output_folder = argv[1]
    width = argv[2]
elif len(argv) == 4:
    imgs_folder = argv[0]
    output_folder = argv[1]
    width = argv[2]
    height = argv[3]
else:
    imgs_folder = argv[0]
    output_folder = argv[1]
    width = argv[2]
    height = argv[3]
    inter = cv.INTER_LINEAR if argv[4] == 'up' else inter

# find all images
imgs = [i for i in os.listdir(os.path.join(".", imgs_folder)) if '.jpg' in i or '.jpeg' in i or '.JPEG' in i or '.JPG' in i]

newSize = (int(width), int(height))
for i in imgs:
    # open image
    img = cv.imread(os.path.join(".", imgs_folder, i))

    # resize image
    img = cv.resize(img, newSize, interpolation = inter)

    # save image
    cv.imwrite(os.path.join(".", output_folder, i), img)
    
    # verbose output
    print(f"#imgresize: <{i}> converted!")
    
#print(os.path.join(".", imgs_folder, imgs[0]))

