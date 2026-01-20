import os
import sys
import time

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError, ID3NoHeaderError, ID3, ID3NoHeaderError, TCON, TPE1
from tinytag import TinyTag

valid_genres = ['Rock', 'Soundtrack', 'Alternative', 'Christmas', 'Pop', 'Electronic', 'Folk', 'Disney', 'Indie', 'Jazz', 'Ambient', 'R&B', 'Punk', 'Country', 'Goth', 'Hip Hop', 'Dance', 'Blues', 'Classical', 'Mashup', 'Vocal', 'Industrial', 'Classic Rock', 'Indie Rock', 'Spoken Word', 'Disco', 'Metal', 'New Wave', 'Indie Pop', 'Halloween', 'World', 'Soul', 'Folk Pop', 'Experimental', 'House', 'Funk', 'Psychedelic Rock', 'Bluegrass', 'Synthpop', 'Progressive Rock', 'Grunge', 'Hard Rock', 'Exotica', 'Rap', 'Reggae', "Children's Music", 'French Pop', 'Lounge', 'Water Music', 'Rockabilly', 'Easy listening', 'Ska', 'Meditation', 'Lo-Fi', 'Post Punk', 'Acoustic', 'Comedy', 'Trip Hop', 'Dream Pop', 'Easy Listening', 'New Age', 'Garage Rock', 'Electroswing', 'Latin', 'Surf Rock', 'Celtic', 'Glam', 'Live', 'Space Age', 'Noise', 'Novelty', 'NerdCore', 'Protest', 'Choral', 'Southern Rock', 'Jam', 'Samba', 'Yacht Rock', 'Doo Wop', 'BritPop', 'Acappella', 'Barbershop', 'Soft Rock', 'Big Band', 'Swing', 'Zydeco', 'Baille Funk', 'Instrumental', 'Sports', 'Dark Cabaret', 'Emo', 'Gospel', 'Broadway', 'Honky Tonk', 'Flamenco', 'J-Pop', 'Bossa Nova', 'Polka', 'Cabaret', 'Christian', 'Swing Revival', 'Hawaiian', 'K-Pop', 'Ragtime', 'Marching Band', 'Advertisement', 'Calypso', 'Bhangra', 'Salsa', '50s', '60s', '70s', '80s', '90s']

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
        print_path = file_path.replace("/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary", "")
        print(f'Added genre "{genre}" to {print_path}')
    except ID3NoHeaderError:
        print(f'No ID3 header found in {file_path}.')
    except Exception as e:
        print(f'Error processing {file_path}: {e}')

def check_mp3_genre(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                print_path = file_path.replace("/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary", "")
                tag = TinyTag.get(file_path)

                print('\n')
                print(print_path)
                try:
                    song_string = f"Artist: {tag.artist}\n Title: {tag.title}\n Album: {tag.album}\n Genre: {tag.genre}"
                except Exception as e:
                    song_string = f"Artist: {tag.artist}, Title: {tag.title}, Genre: {tag.genre}"
                    print("No Album", e)
                print(song_string)

                """
                if tag.genre in valid_genres:
                    if tag.genre in ['Rock', 'Pop', 'Easy listening', 'Easy Listening', 'Live', 'Noise', 'Christian']:
                        proceed = input(f"Is the genre {tag.genre.upper()} ok for {print_path}? (n or enter for y): ")
                        if proceed == 'n':
                            genre = input(f"Enter a new genre for {print_path}: ")
                            print(f"New genre is {genre}")
                            add_genre_to_mp3(file_path, genre)
                else:
                    if tag.genre == 'Hip-Hop':
                        genre = 'Hip Hop'
                    else:
                        genre = input(f"{tag.genre} is not valid, enter a new one: ")
                    print(f"New genre is {genre}")
                    add_genre_to_mp3(file_path, genre)
                """                

                if tag.genre in valid_genres:
                    proceed = input(f"Is the genre {tag.genre.upper()} ok for {print_path}? (n or enter for y): ")
                    if proceed == 'n':
                        genre = input(f"Enter a new genre for {print_path}: ")
                        print(f"New genre is {genre}")
                        add_genre_to_mp3(file_path, genre)
                else:
                    genre = input(f"{tag.genre} is not valid, enter a new one: ")
                    print(f"New genre is {genre}")
                    add_genre_to_mp3(file_path, genre)


def find_specific_genre(directory):
    novelties = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                tag = TinyTag.get(file_path)

                # print(f"Artist: {tag.artist}, Title: {tag.title}, Genre: {tag.genre}")
                if tag.genre == 'Novelty':
                    print(f"Artist: {tag.artist}, Title: {tag.title}, Genre: {tag.genre}")
                    novelties.append(file_path)
    print(novelties)

def list_genres(directory):
    for root, dirs, files in os.walk(directory):
        files.sort()
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                tag = TinyTag.get(file_path)

                print('\n')
                song_string = f"Artist: {tag.artist}\n Title: {tag.title}\n Album: {tag.album}\n Genre: {tag.genre}"
                print(song_string)

def main():
    directory_path = "/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary"
    # directory_path = "/Users/barbarashaurette/Music/5SongsDaily/ARCHIVE"

    # check_mp3_genre(directory_path)
    find_specific_genre(directory_path)
    # list_genres(directory_path)

if __name__ == "__main__":
    main()
