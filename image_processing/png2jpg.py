#!/usr/bin/env python3
import os
import sys
import cv2 as cv

# default values
imgs_folder = ''
output_folder = ''

# get arguments
argv = sys.argv[1:]
if len(argv) < 2:
	print("\n#png2jpg: png2jpg.py [imgs_folder] [output_folder]\n")
	sys.exit()
else:
	imgs_folder = argv[0]
	output_folder = argv[1]

# find all images
imgs = [i for i in os.listdir(os.path.join(".", imgs_folder)) if '.png' in i]

for i in imgs:
	# open image
	img = cv.imread(os.path.join(".", imgs_folder, i))

	i_new = i.split(".")

	# save image
	cv.imwrite(os.path.join('.', output_folder, i_new[0] + '.jpg'), img, [int(cv.IMWRITE_JPEG_QUALITY), 100])

	# verbose output
	print(f"#imgresize: <{i}> converted!")


