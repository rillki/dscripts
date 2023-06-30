#!/usr/bin/bash

for var in $@;
do
    youtube-dl -x --audio-format mp3 -o "%(title)s.%(ext)s" $var
done


