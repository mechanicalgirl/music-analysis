import os
import requests
import sys

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError, ID3NoHeaderError, ID3, ID3NoHeaderError, TCON, TPE1
from tinytag import TinyTag

def add_artist_to_mp3(file_path, artist):
    try:
        # Load the MP3 file
        audio = MP3(file_path, ID3=ID3)
        # Check if ID3 tags exist, if not, create them
        if audio.tags is None:
            audio.add_tags()
        # Set the artist
        audio.tags.add(TPE1(encoding=3, text=artist))
        audio.save()
        print(f'Added artist "{artist}" to {file_path}')
    except ID3NoHeaderError:
        print(f'No ID3 header found in {file_path}.')
    except Exception as e:
        print(f'Error processing {file_path}: {e}')

def add_genre_to_mp3(file_path, genre):
    try:
        # Load the MP3 file
        audio = MP3(file_path, ID3=ID3)
        # Check if ID3 tags exist, if not, create them
        if audio.tags is None:
            audio.add_tags()
        # Set the genre
        audio.tags.add(TCON(encoding=3, text=genre))
        audio.save()
        print(f'Added genre "{genre}" to {file_path}')
    except ID3NoHeaderError:
        print(f'No ID3 header found in {file_path}.')
    except Exception as e:
        print(f'Error processing {file_path}: {e}')

def find_mp3_without_genre_or_artist(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                tag = TinyTag.get(file_path)

                print(f"{file_path}, Tag: {tag.genre}, Artist: {tag.artist}")
                if not tag.artist:
                    artist = input(f"Enter the artist for {file_path}: ")
                    print(f"Artist is {artist}")
                    add_artist_to_mp3(file_path, artist)
                else:
                    artist = tag.artist

                if tag.genre is None or tag.genre == '' or tag.genre == ' ' or tag.genre.lower() in ['other', 'unknown']:
                    genre = ""
                    # Search by artist to get genre
                    try:
                        artist = artist.replace(" ", "%20")
                    except Exception as e:
                        print(artist, e)
                    r = requests.get(f"https://www.theaudiodb.com/api/v1/json/123/search.php?s={artist}")
                    result = r.json()
                    print(f"RESULT for {artist}: {result}")
                    if result['artists']:
                        if result['artists'][0]['strGenre']:
                            genre = result['artists'][0]['strGenre']
                        else:
                            genre = input(f"Enter the genre for {file_path}: ")
                    else:
                        genre = input(f"Enter the genre for {file_path}: ")
                    print(f"Genre is {genre}")
                    add_genre_to_mp3(file_path, genre)

def main():
    directory_path = sys.argv[1]  # (example: "/path/to/music/files")
    find_mp3_without_genre_or_artist(directory_path)

if __name__ == "__main__":
    main()
