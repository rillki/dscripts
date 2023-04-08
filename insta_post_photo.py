import os
import sys
import shutil
import argparse
from instabot import Bot
from PIL import Image
from PIL.ExifTags import TAGS

if os.path.exists('./config'):
    shutil.rmtree('./config', ignore_errors=True)

# set up args parser
parser = argparse.ArgumentParser('Instagram Photo Uploader v.1.0')
parser.add_argument('-u', '--username', metavar = '\b', type=str, help = 'your username')
parser.add_argument('-p', '--password', metavar = '\b', type=str, help = 'your password')
parser.add_argument('-i', '--image', metavar = '\b', type=str, help = 'path to image')
parser.add_argument('-v', '--verbose', metavar = '\b', action=argparse.BooleanOptionalAction, default = True, help = 'verbose output')
args = parser.parse_args()

# don't do anything if image does not exist
if not os.path.exists(args.image):
    print(f'<{args.image}> does not exist!')
    sys.exit()

# get image info
img = Image.open(args.image)
exif_data = img.getexif()

for tagid in exif_data:
    tag = TAGS.get(tagid, tagid)
    data = exif_data.get(tagid)

    if isinstance(data, bytes):
        data = data.decode()

    print(f'{tag:16}: {data}')

# print(img)

# bot = Bot()
# bot.login(username=args.username, password=args.password)










