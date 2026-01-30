"""
Usage:
    python3 music_report.py /path/to/music/files
"""

import argparse
import os
from collections import Counter, defaultdict

def is_mp3(path: str) -> bool:
    return path.lower().endswith(".mp3")

def walk_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            yield os.path.join(dirpath, f)

def main():
    ap = argparse.ArgumentParser(description="Summarize a music library by category and artist.")
    ap.add_argument("root", help="Library root (e.g., /Volumes/Drive/Library)")
    ap.add_argument("--top-artists", type=int, default=50, help="How many top artists to show (overall)")
    ap.add_argument("--top-cat-artists", type=int, default=100, help="How many category|artist rows to show")
    args = ap.parse_args()

    root = os.path.abspath(args.root)

    total = 0
    cat_counts = Counter()
    top_artists = Counter()
    cat_artist_counts = Counter()
    holidays_counts = Counter()

    for path in walk_files(root):
        if not is_mp3(path):
            continue

        total += 1

        rel = os.path.relpath(path, root)
        parts = rel.split(os.sep)
        if len(parts) < 2:
            # Not in expected structure; skip counting categories/artists
            continue

        category = parts[0]
        # Artist is the directory immediately above the file
        artist = parts[-2] if len(parts) >= 2 else "(unknown)"

        cat_counts[category] += 1
        top_artists[artist] += 1
        cat_artist_counts[f"{category}|{artist}"] += 1

        if category == "Holidays" and len(parts) >= 3:
            # Holidays/<Subcat>/Artist/track.mp3
            holidays_counts[parts[1]] += 1

    print("== Music Report ==")
    print(f"Root: {root}\n")
    print(f"Total MP3 files: {total}\n")

    print("-- MP3s per Category{} --")
    for cat, n in sorted(cat_counts.items(), key=lambda kv: kv[1], reverse=True):
        print(f"{n:7d}  {cat}")
    print()

    print("-- Top Artists overall{} --")
    for artist, n in top_artists.most_common(args.top_artists):
        print(f"{n:7d}  {artist}")
    print()

    print("-- Top Artists within each Category{} --")
    for key, n in sorted(cat_artist_counts.items(), key=lambda kv: kv[1], reverse=True)[:args.top_cat_artists]:
        print(f"{n:7d}  {key}")
    print()

    if "Holidays" in cat_counts and holidays_counts:
        print("-- Holidays sub-breakdown --")
        for sub, n in sorted(holidays_counts.items(), key=lambda kv: kv[1], reverse=True):
            print(f"{n:7d}  {sub}")
        print()

if __name__ == "__main__":
    main()

