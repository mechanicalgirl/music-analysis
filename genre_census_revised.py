#!/usr/bin/env python3
# python3 genre_census_revised.py
"""
Genre census for a music library.
Reads Artist + Genre tags (using TinyTag, or Mutagen as fallback),
- genre_histogram.tsv         (Genre → file count)

Usage:
    pip3 install tinytag
    python3 genre_census_revised.py
"""

import argparse
import os
import sys
from collections import Counter, defaultdict

from tinytag import TinyTag


def walk_music(directory):
    total_files = 0
    genre_counter = Counter()
    all_genres = []
    all_counters = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                tags = TinyTag.get(file_path)
                print_path = file_path.replace("/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary", "")
                print(f"Analyzing path {print_path}")

                total_files += 1
                genre = tags.genre
                if not genre in all_genres:
                    all_genres.append(genre)
                genre_counter[genre] += 1

    for g in all_genres:
        counter_tuple = (g, genre_counter[g])
        all_counters.append(counter_tuple)

    print(f"Total files: {total_files}")
    return all_counters

def main():
    directory_path = "/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary"
    # directory_path = "/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/Alphabetical by Artist"
    # directory_path = "/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary/Playlists"

    all_counters = walk_music(directory_path)
    counters = sorted(all_counters, key=lambda x: x[1], reverse=True)

    for c in counters:
        print(c)

    with open("genre_histogram.tsv", "w", encoding="utf-8") as f:
        for c in counters:
            f.write(f"{c[0]}\t{c[1]}\n")

    # print(f"[done] Scanned {total_files} files")
    print(f"[done] Wrote: genre_histogram.tsv")

if __name__ == "__main__":
    main()
