# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pillow",
#     "tinytag",
# ]
# ///

# uv run song_rename.py
# https://github.com/tinytag/tinytag

import math
import os
from os import listdir
from os.path import isfile, join
import sys

from tinytag import TinyTag

inpath = "/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/Playlists/Christmas 2023/"

mp3files = [f for f in listdir(inpath) if isfile(join(inpath, f)) and f.endswith(".mp3")]
for mp3 in mp3files:
    tag: TinyTag = TinyTag.get(inpath+mp3)

    title = tag.title
    artist = tag.artist

    print(mp3, artist)

    if artist and not mp3.startswith(artist):
        new_filename = artist + "-" + mp3
        if new_filename.endswith(artist+".mp3"):
            print(new_filename, "ENDS WITH", artist)
            new_filename = new_filename[:-len(artist+".mp3")] +".mp3"
            new_filename = new_filename.replace(" - .mp3", ".mp3")
        print("NEW FILENAME", new_filename)
        os.rename(inpath+mp3, inpath+new_filename)
