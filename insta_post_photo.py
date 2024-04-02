# module insta_post_photo

import os
import sys
import time
import shutil
import argparse
from instagrapi import Client as InstaClient


if __name__ == '__main__':
    bot = InstaClient()
    bot.login(username='username', password='password')
    time.sleep(0.1)
    bot.photo_upload(path='img.jpg', caption='api test')
    time.sleep(0.1)
    bot.logout()


# set up args parser
# parser = argparse.ArgumentParser('Instagram Photo Uploader v.1.0')
# parser.add_argument('-u', '--username', metavar = '\b', type=str, help = 'your username')
# parser.add_argument('-p', '--password', metavar = '\b', type=str, help = 'your password')
# parser.add_argument('-i', '--image', metavar = '\b', type=str, help = 'path to image')
# parser.add_argument('-v', '--verbose', metavar = '\b', action=argparse.BooleanOptionalAction, default = True, help = 'verbose output')
# args = parser.parse_args()

# # don't do anything if image does not exist
# if not os.path.exists(args.image):
#     print(f'<{args.image}> does not exist!')
#     sys.exit()

# bot = Bot()
# bot.login(username=args.username, password=args.password)










