import os
from tinytag import TinyTag

def find_mp3_without_genre(directory):
    # Iterate over all subdirectories and files
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is an MP3
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                tag = TinyTag.get(file_path)
                
                # Check if genre metadata is missing
                if tag.genre is None:
                    print(file_path)

find_mp3_without_genre("/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/Alphabetical by Artist")

