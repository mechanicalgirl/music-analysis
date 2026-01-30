"""
Simplified version of the genre census

What it does:

- Walks a music library and reads artist and genre tags
- Groups file counts by genre
- Produces a genre_histogram.tsv (genre ordered by file count)

Usage:
    python3 genre_census_revised.py /path/to/music/files
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
                print(f"Analyzing path {file_path}")

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
    directory = sys.argv[1]

    all_counters = walk_music(directory)
    counters = sorted(all_counters, key=lambda x: x[1], reverse=True)

    for c in counters:
        print(c)

    with open("genre_histogram.tsv", "w", encoding="utf-8") as f:
        for c in counters:
            f.write(f"{c[0]}\t{c[1]}\n")

    print(f"[done] Wrote: genre_histogram.tsv")

if __name__ == "__main__":
    main()
