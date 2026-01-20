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
    directories = [
        '/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/Alphabetical by Artist/D/Day of the Dead',
        '/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/Ambient/The Man Machine - Mojo Celebrates The Electronic Revolution/'
    ]
    for d in directories:
        make_folders(d)


if __name__ == "__main__":
    main()
