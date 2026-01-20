import os
import re
import sys

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError, TPE1, TIT2
from tinytag import TinyTag

def add_artist_to_mp3(file_path, artist):
    try:
        audio = MP3(file_path, ID3=ID3)
        if audio.tags is None:
            audio.add_tags()
        audio.tags.add(TPE1(encoding=3, text=artist))
        audio.save()
        print(f'Added artist "{artist}" to {file_path}')
    except ID3NoHeaderError:
        print(f'No ID3 header found in {file_path}.')
    except Exception as e:
        print(f'Error processing {file_path}: {e}')

def add_title_to_mp3(file_path, title):
    try:
        audio = MP3(file_path, ID3=ID3)
        if audio.tags is None:
            audio.add_tags()
        audio.tags.add(TIT2(encoding=3, text=title))
        audio.save()
        print(f'Added title "{title}" to {file_path}')
    except ID3NoHeaderError:
        print(f'No ID3 header found in {file_path}.')
    except Exception as e:
        print(f'Error processing {file_path}: {e}')

def find_mp3_changes(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                tag = TinyTag.get(file_path)

                print_path = file_path.replace('/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/', '')
                print(f"{print_path}, Artist: {tag.artist}, Title: {tag.title}")

                if not tag.artist:
                    print('\n')
                    """
                    # for alphabetical artists
                    proposed_artist = print_path.split('/')[2].title()  # for alphabetical artists
                    proceed = input(f"Should the ARTIST be: {proposed_artist}? (y/n):")
                    if proceed == 'y':
                        artist = proposed_artist
                    else:
                        artist = input(f"Enter the ARTIST for {print_path}: ")
                    """
                    artist = input(f"Enter the ARTIST for {print_path}: ")
                    print(f"New artist is {artist}")
                    print('\n')
                    add_artist_to_mp3(file_path, artist)
                else:
                    artist = tag.artist

                if not tag.title:
                    print('\n')
                    proposed_title = print_path.split('/')[-1].split('.mp3')[0].title()
                    proceed = input(f"Should the TITLE be: {proposed_title}? (y/n):")
                    if proceed == 'y':
                        title = proposed_title
                    else:
                        title = input(f"Enter the TITLE for {print_path}: ")
                    print(f"New title is {title}")  
                    print('\n')
                    add_title_to_mp3(file_path, title)      
                else:
                    title = tag.title

def fix_song_titles(directory):
    TRACKNUM_PATTERN = r'^\d+[-.]\d*\s*|\d+\s*-\s*'
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                tag = TinyTag.get(file_path)

                print_path = file_path.replace('/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/', '')
                print(f"{print_path}, Artist: {tag.artist}, Title: {tag.title}")

                match = re.search(TRACKNUM_PATTERN, tag.title)
                if match:
                    print('\r')
                    cleaned_title = re.sub(TRACKNUM_PATTERN, '', tag.title)
                    okay = input(f"Use this TITLE?: {cleaned_title} (y/n):")
                    if okay == 'y':
                        title = cleaned_title
                    elif okay == 'n':
                        title = input(f"Enter new TITLE for {print_path}: ")
                    else:
                        break

                    print(f"New title is {title}")
                    add_title_to_mp3(file_path, title)
                    print('\r')

def fix_artist_tags(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                tag = TinyTag.get(file_path)

                print_path = file_path.replace('/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/', '')
                print(f"{print_path}, Artist: {tag.artist}, Title: {tag.title}")

                if '  ' in tag.artist:
                    print('\r')
                    print(f"---{tag.artist}---")
                    cleaned_artist = tag.artist.strip()
                    proceed = input(f"Use ARTIST name {cleaned_artist} (y/n)? ")
                    if proceed == 'y':
                        artist = cleaned_artist
                    else:
                        artist = input(f"Enter the ARTIST for {print_path}: ")
                        print(f"Fixed artist name is {artist}")
                    print('\r')
                    add_artist_to_mp3(file_path, artist)

def clean_file_name(root, file_name):
    new_name = file_name
    new_name = new_name.replace(' ', '').replace("'", '').replace('.', '').replace('&', 'and').replace(',', '')
    new_name = new_name.replace('/', '-').replace('"', '').replace(':', '-').replace('|', '-')
    # this omits anything in brackets, parens or curly braces from the file name, but leaves them in the title tag
    cleaned_name = new_name.replace('(', '-').replace(')', '')
    # cleaned_name = re.sub(r'\([^()]*\)', '', new_name)
    cleaned_name = re.sub(r"\[(.*?)\]", '', cleaned_name)
    # Remove any extra spaces that may result from the removal
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()
    new_file_name = f"{root}/{cleaned_name}.mp3"
    return new_file_name

def rename_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                print_path = file_path.replace('/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/', '')

                tag = TinyTag.get(file_path)
                if (' ' in file) or (tag.artist.lower().replace(' ', '') not in file.lower()):
                    current_file_name = file_path
                    new_file_name = clean_file_name(root, f"{tag.artist}-{tag.title}")

                    print('\n')
                    print(f"{print_path}, Artist: {tag.artist}, Title: {tag.title}")

                    if os.path.exists(new_file_name):
                        print(f"Cannot rename, {new_file_name} already exists, skipping")
                    else:
                        print_new_file_name = new_file_name.replace('/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/', '')
                        print(file, "\n\t->", print_new_file_name)
                        try:
                            os.rename(current_file_name, new_file_name)
                        except Exception as e:
                            print(e, new_name, tag.artist, tag.title)

                        """
                        proceed = input("OK to rename? (y/n):")
                        if proceed == 'y':
                        """

def main():
    directory = "/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/Alphabetical by Artist"

    # find_mp3_changes(directory)
    # fix_song_titles(directory)
    # fix_artist_tags(directory)
    rename_files(directory)  ## run after setting tags

if __name__ == "__main__":
    main()
