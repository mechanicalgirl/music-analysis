"""
Identify duplicate music files based on artist, title and file length

What it does:

- Iterates over a collection of music files
- Identifies duplicate files
- Stores the list of duplicates in a local file
- Iterates over the list of duplicates and gives the user the option to delete one or the other

Usage:
    python3 find_duplicates.py /path/to/music/files
"""

import os
import hashlib
import sys

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError, TPE1, TIT2
from tinytag import TinyTag


def get_file_hash(file_tuple):
    hash_md5 = hashlib.md5(file_tuple)
    print(hash_md5.hexdigest())
    return hash_md5.hexdigest()

def find_duplicate_files(directory):
    file_hash_dict = {}
    duplicate_files = []

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.lower().endswith('.mp3'):
                file_path = os.path.join(root, file_name)
                tag = TinyTag.get(file_path)
                audio = MP3(file_path, ID3=ID3)
                print(f"Artist: {tag.artist}, Title: {tag.title}, Length: {int(audio.info.length)}")

                file_tuple = (tag.artist, tag.title, int(audio.info.length))
                file_hash = get_file_hash(str(file_tuple).encode())

                if file_hash in file_hash_dict:
                    duplicate_files.append((file_path, file_hash_dict[file_hash]))
                else:
                    file_hash_dict[file_hash] = file_path
    return duplicate_files

def fix_duplicates(directory, duplicates):
    deletes = []
    if duplicates:
        for line in duplicates:
            ft = eval(line.strip())
            file_1 = directory + ft[0]
            file_2 = directory + ft[1]
            try:
                audio_1 = MP3(file_1, ID3=ID3)
                audio_2 = MP3(file_2, ID3=ID3)
                tag_1 = TinyTag.get(file_1)
                tag_2 = TinyTag.get(file_1)
                print(f"File 1: Artist: {tag_1.artist}, Song: {tag_1.title}, Genre: {tag_1.genre}, Length: {int(audio_1.info.length)} {ft[0]} ")
                print(f"File 2: Artist: {tag_2.artist}, Song: {tag_2.title}, Genre: {tag_2.genre}, Length: {int(audio_2.info.length)} {ft[1]} ")
                which_delete = input("Delete 1, 2, or neither?")
                if which_delete == '1':
                    deletes.append(file_1)
                elif which_delete == '2':
                    deletes.append(file_2)
                else:
                    pass
                print(deletes)
                print('\n')
            except Exception as e:
                print(e)
                pass

def main():
    directory = sys.argv[1]
    duplicates = find_duplicate_files(directory)
    if duplicates:
        print("Duplicate files found:")
        for file1, file2 in duplicates:
            print(f"File 1: {file1}")
            print(f"File 2: {file2}")
            print("-" * 30)
    fix_duplicates(directory, duplicates)

if __name__ == "__main__":
    main()
