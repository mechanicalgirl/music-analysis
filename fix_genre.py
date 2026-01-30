"""
Correct genre tags using the discogs API to identify genre by artist

Usage:
    python3 fix_genre.py /path/to/music/files discogs_token
"""

import os
import sys

import discogs_client
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError, ID3NoHeaderError, ID3, ID3NoHeaderError, TCON
from tinytag import TinyTag

valid_genres = ['Rock', 'Soundtrack', 'Alternative', 'Christmas', 'Pop', 'Electronic', 'Folk', 'Disney', 'Indie', 'Jazz', 'Ambient', 'R&B', 'Punk', 'Country', 'Goth', 'Hip Hop', 'Dance', 'Blues', 'Classical', 'Mashup', 'Vocal', 'Industrial', 'Classic Rock', 'Indie Rock', 'Spoken Word', 'Disco', 'Metal', 'New Wave', 'Hip-Hop', 'Indie Pop', 'Halloween', 'World', 'Soul', 'Folk Pop', 'Experimental', 'House', 'Funk', 'Psychedelic Rock', 'Bluegrass', 'Synthpop', 'Progressive Rock', 'Grunge', 'Hard Rock', 'Exotica', 'Rap', 'Reggae', "Children's Music", 'French Pop', 'Lounge', 'Water Music', 'Rockabilly', 'Easy listening', 'Ska', 'Meditation', 'Lo-Fi', 'Post Punk', 'Acoustic', 'Comedy', 'Trip Hop', 'Dream Pop', 'Easy Listening', 'New Age', 'Garage Rock', 'Electroswing', 'Latin', 'Surf Rock', 'Celtic', 'Glam', 'Live', 'Space Age', 'Noise', 'Novelty', 'NerdCore', 'Protest', 'Choral', 'Southern Rock', 'Jam', 'Samba', 'Yacht Rock', 'Doo Wop', 'BritPop', 'Acappella', 'Barbershop', 'Soft Rock', 'Big Band', 'Swing', 'Zydeco', 'Baille Funk', 'Instrumental', 'Sports', 'Dark Cabaret', 'Emo', 'Gospel', 'Broadway', 'Honky Tonk', 'Flamenco', 'J-Pop', 'Bossa Nova', 'Polka', 'Cabaret', 'Christian', 'Swing Revival', 'Hawaiian', 'K-Pop', 'Ragtime', 'Marching Band', 'Advertisement', 'Calypso', 'Bhangra', 'Salsa', '50s', '60s', '70s', '80s', '90s']

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
        print(f'Added genre "{genre}" to {file_path}')
    except ID3NoHeaderError:
        print(f'No ID3 header found in {file_path}.')
    except Exception as e:
        print(f'Error processing {file_path}: {e}')

def find_mp3_genre(directory, discogs):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                tag = TinyTag.get(file_path)

                print(f"{tag.title}, Artist: {tag.artist}, Tag: {tag.genre}")
                try:
                    results = discogs.search(tag.title, artist=tag.artist, type='release')
                    suggested_genres = results[0].genres
                    suggested_styles = results[0].styles
                    discog_suggestion = suggested_genres + suggested_styles
                    print(f"Discogs suggests using one of these: {discog_suggestion}")
                except Exception as e:
                    print(e)

                if tag.genre:
                    if tag.genre not in valid_genres:
                        genre = input(f"Enter the genre for {file_path}: ")
                        print(f"Changing genre to: {genre}")
                        replace_mp3_genre(file_path, genre)
                    else:
                        proceed = input(f"Is the genre {tag.genre.upper()} ok for {file_path}? (n or enter for y): ")
                        if proceed == 'n':
                            genre = input(f"Enter a new genre for {file_path}: ")
                            print(f"New genre is {genre}")
                            replace_mp3_genre(file_path, genre)
                            print(f"Adding genre: {genre}")
                else:
                    genre = input(f"Enter the genre for {file_path}: ")
                    print(f"Changing genre to: {genre}")
                    replace_mp3_genre(file_path, genre)


def change_mp3_genre(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                tag = TinyTag.get(file_path)

                print(f"{tag.title}, Artist: {tag.artist}, Tag: {tag.genre}")
                genre = input(f"Enter the new genre for {file_path}: ")
                print(f"Changing genre to: {genre}")
                replace_mp3_genre(file_path, genre)

def main():
    directory = sys.argv[1]
    discogs_token = sys.argv[2]
    d = discogs_client.Client('ExampleApplication/0.1', user_token=discogs_token)
    find_mp3_genre(directory, d)
    change_mp3_genre(directory)

if __name__ == "__main__":
    main()
