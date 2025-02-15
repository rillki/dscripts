# module insta_auto_post

# system
import os
import sys
import time

# image properties
from exif import Image

# instagram
from instagrapi import Client as InstaClient

# setup globals
auth_file = '.insta_auth'
uploaded_folder = 'uploaded'
image_caption_folder = 'text'
log_header = '[ insta post ]'


def insta_upload_photo(image_path: str, image_text: str):
    # read image description
    image_caption = ''
    if os.path.exists(image_text):
        with open(image_text, 'r') as f:
            image_caption = f.read().strip()
    else: image_caption = os.path.basename(image_path).split('.')[0]
    print(image_caption)
    exit(0)
    # log
    print(log_header, f'Image caption loaded: \n---\n{image_caption}\n---')

    # read authorization data
    print(log_header, 'Reading autherization data...')
    auth_data = None
    with open(auth_file, 'r') as f:
        auth_data = f.read().strip().split('\n')

    # login
    print(log_header, 'Trying to login...')
    bot = InstaClient()
    bot.login(username=auth_data[0], password=auth_data[1])
    time.sleep(0.1)

    # upload
    print(log_header, 'Uploading image...')
    bot.photo_upload(path=image_path, caption=caption)
    time.sleep(0.1)
    bot.logout()

    # log
    print(log_header, 'Image uploaded.')


if __name__ == '__main__':
    assert os.path.exists(auth_file), f'Autherization file does not exist <{auth_file}>!'

    # find all images in directory
    images = list(
        filter(
            lambda x: os.path.splitext(x)[-1].lower() in ['.jpg', '.jpeg', '.png'],
            os.listdir(os.getcwd() if len(sys.argv) < 2 else sys.argv[1]),
        )
    )
    if not len(images):
        print(log_header, 'No image found!')
        exit(0)

    # select image for publication
    image_path = images[0]
    image_text = os.path.join(os.path.dirname(image_path), image_caption_folder, os.path.basename(image_path)) + '.txt'
    print(log_header, f'Image selected: <{image_path}>')

    # upload photo
    insta_upload_photo(image_path=image_path, image_text=image_text)

    # move image to published folder
    print(log_header, f'Moving image to <{os.path.join(uploaded_folder, image_path)}>')
    if not os.path.exists(uploaded_folder): os.mkdir(uploaded_folder)
    os.rename(image_path, os.path.join(uploaded_folder, image_path))

    # log
    print(log_header, 'Done.')
