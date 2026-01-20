"""
curl the page source from a YouTube playlist, then parse it down and generate
audio import commands for every song on the page.
"""

import json
import os
import pprint
import stat
import sys

import requests
from bs4 import BeautifulSoup

def generate(playlistfile, artist, album, year, genre):
    with open(playlistfile, "r") as file:
        content = file.read()

    first_split = content.split('playlistVideoRenderer":{')
    for item in first_split:
        if item.startswith('"videoId"'):
            video_id = item.split('"videoId":"')[1].split('","')[0]
            video_title = item.split('"title":{"runs":[{"text":')[1].split('"')[1]
            command = f'uv run audio_import.py https://www.youtube.com/watch?v={video_id} "{artist}" "{video_title}" "{album}" "{year}" "{genre}"'
            print(command, '\n')
            with open('/Users/barbarashaurette/Music/5SongsDaily/imports.sh', "a") as f:
                f.write(command + '\n')
            os.chmod('/Users/barbarashaurette/Music/5SongsDaily/imports.sh', stat.S_IRWXU)
            # ./imports.sh

def main():
    # curl https://www.youtube.com/playlist?list=PLBKadB95sF475w3zaBpHJZtX0u7kjWAhh > playlist.txt
    # python3 playlist_parse.py "ARTIST" "ALBUM" "YEAR" "GENRE"
    artist = sys.argv[1]
    album = sys.argv[2]
    year = sys.argv[3]
    genre = sys.argv[4]
    playlistfile = "/Users/barbarashaurette/Music/analysis/playlist.txt"
    generate(playlistfile, artist, album, year, genre)

if __name__ == "__main__":
    main()
