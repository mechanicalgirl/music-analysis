#!/usr/bin/env python3
# python3 genre_census.py "/Volumes/My Passport for Mac/bshaurette.music.collection/MusicLibrary" --ext mp3 --with-buckets --guess-artist-from-path
"""
Genre census for a music library.
Reads Artist + Genre tags (using TinyTag, or Mutagen as fallback),
normalizes common genre names, and produces TSV reports:

- artists_majority_genre.tsv  (Artist → majority genre across their files)
- genre_histogram.tsv         (Genre → file count)
- bucket_histogram.tsv        (optional macro buckets → count of files)

Usage:
    pip3 install tinytag   # or: pip3 install mutagen
    python3 genre_census.py "/path/to/MusicLibrary/Alphabetical by Artist" \
        --ext mp3 --with-buckets --guess-artist-from-path
"""

import argparse
import os
import sys
from collections import Counter, defaultdict


def try_import_tag_readers():
    tag_lib = None
    reader = None
    try:
        from tinytag import TinyTag  # type: ignore
        tag_lib = "tinytag"

        def read_tags(path):
            try:
                t = TinyTag.get(path, ignore_errors=True)
                return (t.artist or "").strip(), (t.genre or "").strip()
            except Exception:
                return "", ""

        reader = read_tags
    except Exception:
        try:
            from mutagen import File as MFile  # type: ignore
            tag_lib = "mutagen"

            def read_tags(path):
                try:
                    f = MFile(path, easy=True)
                    if not f:
                        return "", ""
                    artist = ""
                    genre = ""
                    for key in ("artist", "ARTIST", "TPE1"):
                        if key in f:
                            v = f[key]
                            if isinstance(v, list):
                                v = v[0] if v else ""
                            artist = str(v).strip()
                            break
                    for key in ("genre", "GENRE", "TCON"):
                        if key in f:
                            v = f[key]
                            if isinstance(v, list):
                                v = v[0] if v else ""
                            genre = str(v).strip()
                            break
                    return artist, genre
                except Exception:
                    return "", ""

            reader = read_tags
        except Exception:
            pass
    return tag_lib, reader


def normalize_genre(g: str) -> str:
    g0 = g.strip()
    if not g0:
        return ""
    g1 = g0.lower()
    repl = {
        "alt rock": "alternative rock",
        "alternative": "alternative rock",
        "alternative/indie": "indie rock",
        "indie": "indie rock",
        "indie-rock": "indie rock",
        "indie rock": "indie rock",
        "synth pop": "synth-pop",
        "synthpop": "synth-pop",
        "hip hop": "hip-hop",
        "hiphop": "hip-hop",
        "electronica": "electronic",
        "edm": "electronic",
        "dance": "dance",
        "hard core": "hardcore",
        "post hardcore": "post-hardcore",
        "r&b": "rnb",
        "r&b/soul": "rnb",
        "soul": "soul",
        "classical": "classical",
        "soundtrack": "soundtrack",
        "ost": "soundtrack",
        "film score": "film/score",
        "score": "film/score",
        "world": "world/traditional",
        "folk": "folk",
        "blues": "blues",
        "jazz": "jazz",
        "ambient": "ambient",
        "new wave": "new wave",
        "punk": "punk",
        "pop punk": "pop-punk",
        "hard rock": "hard rock",
        "metal": "metal",
        "black metal": "black metal",
        "death metal": "death metal",
        "house": "house",
        "techno": "techno",
        "idm": "idm",
        "downtempo": "downtempo",
        "trip hop": "trip-hop",
        "trip-hop": "trip-hop",
        "shoegaze": "shoegaze",
        "dream pop": "dream pop",
        "post rock": "post-rock",
        "post-rock": "post-rock",
        "bluegrass": "bluegrass",
        "zydeco": "zydeco",
        "electro swing": "electroswing",
        "electro-swing": "electroswing",
    }
    if g1 in repl:
        return repl[g1]
    if "hip" in g1 and "hop" in g1:
        return "hip-hop"
    if "synth" in g1 and "pop" in g1:
        return "synth-pop"
    if "alt" in g1 and "rock" in g1:
        return "alternative rock"
    if "electro" in g1 and "swing" in g1:
        return "electroswing"
    return g0


def bucket_for(genre: str) -> str:
    g = genre.lower().strip()
    if not g:
        return "unknown"
    if "classical" in g:
        return "classical"
    if "soundtrack" in g or "score" in g:
        return "film/score"
    if "jazz" in g or "blues" in g:
        return "jazz/blues"
    if "world" in g or "cajun" in g or ("folk" in g and "indie" not in g):
        return "world/folk/traditional"
    if "hip-hop" in g or "rap" in g:
        return "hip-hop"
    if "metal" in g or "hardcore" in g:
        return "metal/hardcore"
    if any(k in g for k in ["house", "techno", "idm", "downtempo", "electronic", "trip-hop", "ambient", "synth"]):
        return "electronic"
    if any(k in g for k in ["indie", "alternative", "post-rock", "shoegaze", "dream pop", "punk", "new wave", "rock", "power pop", "garage"]):
        return "rock/alt"
    if "pop" in g:
        return "pop"
    return "other"


def walk_music(root, exts):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower().lstrip(".")
            if exts and ext not in exts:
                continue
            yield os.path.join(dirpath, fn)


def main():
    ap = argparse.ArgumentParser(description="Census genres in a music library (uses TinyTag or Mutagen).")
    ap.add_argument("root", help="Root folder (e.g., /Volumes/Drive/MusicLibrary/Alphabetical by Artist)")
    ap.add_argument("--ext", action="append", default=["mp3"], help="File extensions to include (default: mp3).")
    ap.add_argument("--with-buckets", action="store_true", help="Also emit macro bucket histogram.")
    ap.add_argument("--guess-artist-from-path", action="store_true", help="If Artist tag empty, fallback to parent folder name.")
    args = ap.parse_args()

    tag_lib, reader = try_import_tag_readers()
    if reader is None:
        print("Error: Could not import tinytag or mutagen.\nInstall one:\n  pip3 install tinytag\n  pip3 install mutagen", file=sys.stderr)
        sys.exit(1)
    print(f"[info] Using tag reader: {tag_lib}")

    total_files = 0
    genre_counter = Counter()
    artist_genre_counts = defaultdict(Counter)

    for path in walk_music(args.root, set([e.lower() for e in args.ext])):
        print(f"Analyzing path {path}")
        total_files += 1
        artist, genre = reader(path)
        if not artist and args.guess_artist_from_path:
            artist = os.path.basename(os.path.dirname(path)).strip()
        # norm_genre = normalize_genre(genre)
        key_genre = genre if genre else "Unknown"
        genre_counter[key_genre] += 1
        if artist:
            artist_genre_counts[artist][key_genre] += 1

    majority = {}
    for artist, gcounts in artist_genre_counts.items():
        best = max(gcounts.items(), key=lambda kv: kv[1])
        majority[artist] = best[0] if best else "Unknown"

    with open("artists_majority_genre.tsv", "w", encoding="utf-8") as f:
        for artist in sorted(majority, key=lambda x: x.lower()):
            f.write(f"{artist}\t{majority[artist]}\n")

    with open("genre_histogram.tsv", "w", encoding="utf-8") as f:
        for g, c in sorted(genre_counter.items(), key=lambda kv: kv[1], reverse=True):
            f.write(f"{g}\t{c}\n")

    if args.with_buckets:
        bucket_counts = Counter()
        for g, c in genre_counter.items():
            bucket_counts[bucket_for(g)] += c
        with open("bucket_histogram.tsv", "w", encoding="utf-8") as f:
            for b, c in sorted(bucket_counts.items(), key=lambda kv: kv[1], reverse=True):
                f.write(f"{b}\t{c}\n")

    print(f"[done] Scanned {total_files} files")
    print(f"[done] Wrote: artists_majority_genre.tsv, genre_histogram.tsv" + (", bucket_histogram.tsv" if args.with_buckets else ""))


if __name__ == "__main__":
    main()
