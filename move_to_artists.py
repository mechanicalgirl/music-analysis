"""
Move music files to artist-based folders

- Walks a music library and reads artist tags on each mp3
- Creates a folder based on the artist name if one does not exist
- Moves the file to the artist-based folder

Note: This script is intended to move files that are grouped by something other than artist, such as compilation albums or soundtracks. You probably don't want it iterating over your entire library, so I suggest passing in a file path to the specific compilation folder.

Usage:
    python3 move_to_artists.py /path/to/music/compilation
"""

import os
import shutil
import sys

from tinytag import TinyTag

def make_folders(directory):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.lower().endswith('.mp3'):
                file_path = os.path.join(root, file_name)
                tag = TinyTag.get(file_path)
                print(f"Artist: {tag.artist}, Title: {tag.title}")
                make_path = os.path.join(root, tag.artist)
                print(f"Make this path: {make_path}")
                if not os.path.exists(make_path):
                    os.makedirs(make_path)
                print(f"Move this file into it: {file_path}")
                new_file_path = os.path.join(make_path, file_name)
                os.rename(file_path, new_file_path)
                print('/n')

def main():
    directory = sys.argv[1]
    make_folders(directory)

if __name__ == "__main__":
    main()
