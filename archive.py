import os
import shutil
import sys

from tinytag import TinyTag

def identify():
    ignore_genres = ['Soundtrack', 'Disney', 'Christmas', 'Jazz', 'Blues']
    archive_directory = "/Users/barbarashaurette/Music/5SongsDaily/ARCHIVE"
    volume_directory = "/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary"

    for root, dirs, files in os.walk(archive_directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                tag = TinyTag.get(file_path)

                artist_folder = get_artist_folder(tag.genre, tag.artist, tag.album)

                if not tag.genre in ignore_genres:
                    new_root = f"Alphabetical by Artist/{artist_folder[0]}"
                else:
                    if tag.genre in ['Jazz', 'Blues']:
                        new_root = 'Jazz and Blues'
                    elif tag.genre == 'Christmas':
                        new_root = 'Holidays/Christmas'
                    elif tag.genre == 'Halloween':
                        new_root = 'Holidays/Halloween'
                    elif tag.genre in ['Broadway', 'Soundtrack']:
                        new_root = 'Soundtracks and Show Tunes'
                    else:
                        new_root = tag.genre

                new_path = os.path.join(volume_directory, new_root, artist_folder, file)

                move = input(f"Move to {new_path}? (y/n): ")
                if move == 'y':
                    file_move(file_path, new_path)
                    original_image_path = file_path.replace('.mp3', '_300.jpg')
                    new_image_path = new_path.replace('.mp3', '_300.jpg')
                    if os.path.exists(original_image_path):
                        file_move(original_image_path, new_image_path)
                else:
                    pass

def get_artist_folder(genre_tag, artist_tag, album_tag):
    artist_folder = artist_tag
    if genre_tag in ['Broadway', 'Soundtrack', 'Disney']:
        artist_folder = album_tag
    if artist_folder.startswith('The'):
        artist_folder = artist_folder.replace('The ', '', 1) + ', The'
    return artist_folder

def file_move(old_path, new_path):
    try:
        shutil.move(old_path, new_path)
    except Exception as e:
        if 'No such file or directory' in str(e):
            print(f"\tCreate directory: {new_path.rsplit('/', 1)[0]}")
            os.mkdir(new_path.rsplit('/', 1)[0])
            try:
                shutil.move(old_path, new_path)
            except Exception as e:
                print(e)

def main():
    identify()
    ## TODO: add separate condition for jpg files

if __name__ == "__main__":
    main()

