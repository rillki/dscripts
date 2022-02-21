import sys
import argparse
from pytube import YouTube
from pytube import Playlist

# download video
def downloadVideo(url = None, audio = False, savePath = None, verbose = False):
    if url is None:
        print('No URL supplied. Exiting...')
        return

    yt = YouTube(url)
    if verbose:
        print(f'Downloading: {yt.title}')

    if audio:
        yt.streams.filter(only_audio = True, file_extension = 'webm', abr =
                '160kbps').first().download(savePath)
    else:
        yt.streams.filter(progressive = True, file_extension =
                'mp4').order_by('resolution').desc().first().download(savePath)

# download videos from a playlist
def downloadFromPlaylist(url = None, audio = False, savePath = None, num = 0, verbose = False):
    if url is None:
        print('No URL supplied. Exiting...')
        return
    
    p = Playlist(url)
    for i in range(0, len(p.videos)):
        if i > num:
            break
        else:
            vid = p.videos[i]
            if verbose:
                print(f'Downloading: {vid.title}')

            if audio:
                vid.streams.filter(only_audio = True, file_extension = 'webm', abr =
                        '160kbps').first().download(savePath)
            else:
                vid.streams.filter(Progressive = True, file_extension =
                        'mp4').order_by('resolution').desc().first().download(savePath)

# set up argparser
parser = argparse.ArgumentParser('Youtube downloader v.1.0')
parser.add_argument('-a', '--audio', metavar = '\b', action=argparse.BooleanOptionalAction, default = False, help = 'audio only')
parser.add_argument('-n', '--quantity', metavar = '\b', type=int, default = 0, help = 'number of videos to download from a playlist')
parser.add_argument('-u', '--url', metavar = '\b', type = ascii, default = None, help = 'youtube playlist or video url')
parser.add_argument('-s', '--save', metavar = '\b', type = ascii, default = 'y2b-downloads', help = 'save path')
parser.add_argument('-v', '--verbose', metavar = '\b', action=argparse.BooleanOptionalAction,
        default = False, help = 'verbose output')

# parse args
args = parser.parse_args()

if args.url is None:
    print('No URL supplied! Exiting...')
    sys.exit()

if args.quantity > 0:
    downloadFromPlaylist(args.url, args.audio, args.save, args.quantity, args.verbose)
else:
    downloadVideo(args.url, args.audio, args.save, args.verbose)

print('DONE\n')




























