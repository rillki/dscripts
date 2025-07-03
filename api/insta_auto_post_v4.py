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
dir_path = os.path.dirname(os.path.abspath(__file__))
auth_file = os.path.join(dir_path, '.insta_auth')
config_file = os.path.join(dir_path, '.insta_config')
log_header = '[ insta post ]'


def insta_upload_photo(image_path: str):
    # generating caption
    caption=None
    with open(image_path, 'rb') as file:
        image = Image(file)
        if image.has_exif:
            caption = os.path.basename(image_path).split('.')[0] + '.\n\n'
            caption += ' | '.join([
                f'{image.make} {image.model}',
                f'f{image.f_number}',
                f'{image.exposure_time} sec' if image.exposure_time >= 1 else f'1/{1/image.exposure_time} sec',
                f'{image.focal_length} mm',
                f'ISO {image.photographic_sensitivity}',
            ])
    caption += f'\n\n#photography #nature #naturephotography #landscape #landscapephotography #{str(image.make).lower()}'

    # log
    print(log_header, f'Captions generated: \n---\n{caption}\n---')

    # read authorization data
    print(log_header, 'Reading autherization data...')
    auth_data = None
    with open(auth_file, 'r') as f:
        auth_data = f.read().strip().split('\n')

    # upload image
    print(log_header, 'Trying to login...')
    bot = InstaClient()
    bot.login(username=auth_data[0], password=auth_data[1])
    time.sleep(0.1)
    bot.photo_upload(path=image_path, caption=caption)
    time.sleep(0.1)
    bot.logout()

    # log
    print(log_header, 'Image uploaded.')


if __name__ == '__main__':
    assert os.path.exists(auth_file), f'Autherization file does not exist <{auth_file}>!'

    # select image to upload
    image_path = None
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # check if config file exists
        if not os.path.exists(config_file):
            print(log_header, 'No image in queue.')
            print(log_header, 'Specify image manually first. Example: <XYZ.jpg> - XYZ is a number.')
            exit(0)

        # get next image in queue
        with open(config_file, 'r') as f:
            image_name = f.read().strip()
            image_path = os.path.join(dir_path, f'D{int(image_name[1:]) + 1}.JPG')

    # log
    print(log_header, f'Image selected: <{image_path}>')

    # check if image exists
    if not os.path.exists(image_path):
        print(log_header, f'Image does not exist: <{image_path}>')
        exit(0)


    # upload photo
    insta_upload_photo(image_path=image_path)

    # update config
    with open(config_file, 'w') as f:
        image_path = os.path.basename(image_path)
        f.write(image_path.split('.')[0])

    # log
    print(log_header, 'Done.')
