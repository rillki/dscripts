from PIL import Image
from PIL.ExifTags import TAGS

# open the image
image = Image.open("img.jpg")

# extracting the exif metadata
exifdata = image.getexif()

# looping through all the tags present in exifdata
for tagid in exifdata:
	
	# getting the tag name instead of tag id
	tagname = TAGS.get(tagid, tagid)

	# passing the tagid to get its respective value
	value = exifdata.get(tagid)

	# printing the final result
	print(f"{tagname:25}: {value}")

