#!/usr/bin/env python3

import os
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

    if os.path.exists(os.path.join(savePath, yt.title)):
        if verbose:
            print(f'             Already exists. Skipping.')
        return

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
    for i in range(0, len(list(p.videos))):
        if i >= num:
            break
        else:
            vid = p.videos[i]
            if verbose:
                print(f'Downloading:({i}) {vid.title}')

            if os.path.exists(os.path.join(savePath, yt.title)):
                if verbose:
                    print(f'             Already exists. Skipping.')
                continue

            if audio:
                vid.streams.filter(only_audio = True, file_extension = 'webm', abr =
                        '160kbps').first().download(savePath)
            else:
                vid.streams.filter(Progressive = True, file_extension =
                        'mp4').order_by('resolution').desc().first().download(savePath)


def downloadFromFile(fileName = None, audio = False, savePath = None, verbose = False):
    if fileName is None:
        print('No filename with URLs supplied. Exiting...')
        return

    # list of URLs
    urls = list()

    # parse files
    with open(fileName, 'r') as file:
        # by line
        for line in file:
            url = line.rstrip()

            # skip empty lines
            if url != '':
                urls.append(url)

    for i in urls:
        downloadVideo(i, audio, savePath, verbose)


# set up argparser
parser = argparse.ArgumentParser('Youtube downloader v.1.1')
parser.add_argument('-a', '--audio', metavar = '\b', action=argparse.BooleanOptionalAction, default = False, help = 'audio only')
parser.add_argument('-n', '--quantity', metavar = '\b', type=int, default = 0, help = 'number of videos to download from a playlist')
parser.add_argument('-u', '--url', metavar = '\b', default = None, help = 'youtube playlist or video url')
parser.add_argument('-s', '--save', metavar = '\b', default ='y2b-downloads', help = 'save path')
parser.add_argument('-f', '--file', metavar = '\b', default = None, help = 'file with youtube URLs (one per line)')
parser.add_argument('-v', '--verbose', metavar = '\b', action=argparse.BooleanOptionalAction,
        default = False, help = 'verbose output')

# parse args
args = parser.parse_args()

print("\n------------- PYTUBE DOWNLOADER -------------\n")

if args.file is None:
    if args.url is None:
        print('No URLs supplied! Exiting...')
    else:
        if args.quantity > 0:
            downloadFromPlaylist(args.url, args.audio, args.save, args.quantity, args.verbose)
        else:
            downloadVideo(args.url, args.audio, args.save, args.verbose)
else:
    downloadFromFile(args.file, args.audio, args.save, args.verbose)

print('\n------------------- DONE --------------------\n')




























