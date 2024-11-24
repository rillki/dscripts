#!/bin/bash

SAVE_FOLDER="webm2mp3"
mkdir -p ${SAVE_FOLDER}

for FILE in *.webm; do
    echo -e "\nCONVERTING '${FILE}'\n";
    ffmpeg -i "${FILE}" -vn -ab 128k -ar 44100 "${SAVE_FOLDER}/${FILE%.webm}.mp3";
done;



