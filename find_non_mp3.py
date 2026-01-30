"""
Identify any files in the music library that are not MP3s

Usage:
    python3 find_non_mp3.py /path/to/music/files

"""

import os
import sys

def find_non_mp3(directory):
    allnon = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                print(file_path)
                allnon.append(file_path)
    return allnon

def main():
    directory = sys.argv[1]
    non = find_non_mp3(directory)

if __name__ == "__main__":
    main()
