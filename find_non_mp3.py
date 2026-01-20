import os
import sys

def find_non_mp3(directory):
    allnon = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                print_path = file_path.replace("/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary", "")
                if file == '.DS_Store' or file.endswith('.zip') or file.endswith('.jpg') or file.endswith('.pdf') or file.endswith('.png') or file.endswith('.txt'):
                    pass
                else:
                    print(file_path)
                    allnon.append(print_path)
    # print(allnon)

def main():
    directory_path = "/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary"
    find_non_mp3(directory_path)

if __name__ == "__main__":
    main()
