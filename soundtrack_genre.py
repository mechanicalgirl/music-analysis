import os
import sys

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError, ID3NoHeaderError, ID3, ID3NoHeaderError, TCON
from tinytag import TinyTag

soundtracks = []


def replace_mp3_genre(file_path, genre):
    try:
        # Load the MP3 file
        audio = MP3(file_path, ID3=ID3)
        # Check if ID3 tags exist, if not, create them
        if audio.tags is None:
            audio.add_tags()
        # Set the genre
        audio.tags.add(TCON(encoding=3, text=genre))
        audio.save()
        print_path = file_path.replace("/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary", "")
        print(f'Added genre "{genre}" to {print_path}')
    except ID3NoHeaderError:
        print(f'No ID3 header found in {file_path}.')
    except Exception as e:
        print(f'Error processing {file_path}: {e}')

def soundtrack_genre(directory):
    st = []
    retag = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                if file_path in songs:

                    tag = TinyTag.get(file_path)
                    print(f"Artist: {tag.artist}, Title: {tag.title}, Genre: {tag.genre}, Album: {tag.album}")

                    keep = input(f"Should this still be a soundtrack? (y/n): ")
                    if keep == 'y':
                        print_path = file_path.replace("/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary", "")
                        st.append((print_path, tag.album))
                    else:
                        genre = input(f"Enter new genre for {file_path}: ")
                        print(f"Adding genre: {genre}")
                        retag.append((print_path, tag.album))
                        replace_mp3_genre(file_path, genre)

    print("MOVE TO SOUNDTRACKS", st)
    print("RETAGS", retag)

def main():
    directory = "/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/Alphabetical by Artist"
    soundtrack_genre(directory)

if __name__ == "__main__":
    main()
