import os
import re
import sys

from tinytag import TinyTag


def list_files(directory):
    print('\n')
    print(directory)
    song_list = []
    move_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                song_list.append(file)
                file_path = os.path.join(root, file)
                tag = TinyTag.get(file_path)
                base_dir = "/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/"

                if tag.genre == 'Ambient':
                    move_path = base_dir + "Ambient/" + tag.artist + "/"
                elif tag.genre == 'Jazz':
                    move_path = base_dir + "Jazz and Blues/" + tag.artist + "/"
                elif tag.genre == 'Classical':
                    move_path = base_dir + "Classical/" + tag.artist + "/"
                elif tag.genre == 'Soundtrack':
                    try:
                        move_path = base_dir + "Soundtracks and Show Tunes/" + tag.album + "/"
                    except Exception as e:
                        print(e, file_path)
                        sys.exit()
                        move_path = base_dir + "Soundtracks and Show Tunes/" + tag.artist + "/"
                else:
                    first_letter = tag.artist[0].upper()
                    move_path = base_dir + "Alphabetical by Artist/" + first_letter + "/" + tag.artist + "/"

                move_file_path = file_path.replace(' ', '\ ')
                move_move_path = move_path.replace(' ', '\ ')
                # if the folder does not exist already, create a mkdir for it:
                if not os.path.isdir(move_path):
                    move_list.append(f"mkdir {move_move_path}\n")
                move = f"mv {move_file_path} {move_move_path}\n"
                move_list.append(move)

    list_path = os.path.join(root, 'song_list.txt')
    print(list_path)
    with open(list_path, "w") as file:
        file.write(f"{directory}\n\n")
        for song in song_list:
            print(song)
            file.write(f"{song}\n")

    mv_list_path = os.path.join(root, 'move_list.txt')
    print(mv_list_path)
    with open(mv_list_path, "w") as file:
        file.write(f"{directory}\n\n")
        for command in move_list:
            print(command)
            file.write(f"{command}\n")

def main():
    directories = ['/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/Playlists/California']
    # directories = ['/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/Playlists/Versailles/Manhattan 1979/Broadway', '/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/Playlists/Versailles/Manhattan 1979/Pop', '/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/Playlists/Versailles/Versailles 1779', '/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/Playlists/Water Music/ALL MERMAIDS', '/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/Playlists/Water Music/Epcot Living Seas', '/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/Playlists/Water Music/Mermaiding/Disco Mermaid', '/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/Playlists/Water Music/The Caretaker:Leyland Kirby']
    for d in directories:
        list_files(d)

if __name__ == "__main__":
    main()
