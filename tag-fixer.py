#!/usr/bin/env python3
"""
mutagen-based music tag fixer

usage:
    python tagfixer.py /path/to/music --dry-run
    python tagfixer.py /path/to/music --auto --backup backup.json
"""

import argparse
import json
import re
from pathlib import Path
from typing import Optional, Tuple, Dict

from mutagen import File as MutagenFile
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4

# heuristics
# TRACKNUM_RE = re.compile(r'^\s*\d+\s*[-._\s]\s*')
TRACKNUM_RE = re.compile(r'^\d{1,2}[-.]\s*|\d+\s*-\s*')
BRACKET_RE = re.compile(r'[\[\(\{].*?[\]\)\}]')  # remove bracketed bits
UNDERSCORE_RE = re.compile(r'_+')

def parse_artist_from_path(path: Path, base: Path) -> Optional[str]:
    """
    heuristically pick an artist name from the path relative to base.
    common layout: base/Artist/Album/track.mp3
    fallback: use the first directory in the relative path
    """
    try:
        rel = path.relative_to(base)
    except Exception:
        rel = path
    parts = rel.parts[:-1]  # drop filename
    if not parts:
        return None
    # prefer first-level directory (Artist)
    return parts[0].strip()

def parse_title_from_filename(fname: str) -> str:
    name = Path(fname).stem
    # drop track numbers like "01 - " or "1. "
    name = TRACKNUM_RE.sub('', name)
    # remove bracketed phrases like "(live)" or "[Remix]"
    name = BRACKET_RE.sub('', name)
    # collapse underscores and extra whitespace
    name = UNDERSCORE_RE.sub(' ', name)
    name = re.sub(r'\s{2,}', ' ', name).strip()
    # optionally titlecase - many prefer original casing; keep as-is but strip
    return name

def read_tags(path: Path) -> Dict[str, str]:
    mf = MutagenFile(path)
    if mf is None:
        return {}
    tags = {}
    # handle common containers
    try:
        if path.suffix.lower() == '.mp3':
            tags_obj = EasyID3(path)
            for k in tags_obj.keys():
                tags[k] = ','.join(tags_obj.get(k, []))
        elif path.suffix.lower() == '.flac':
            f = FLAC(path)
            for k, v in f.tags.items():
                tags[k] = ','.join(v)
        elif path.suffix.lower() in ('.m4a', '.mp4', '.m4b'):
            f = MP4(path)
            # mp4 tags are keyed differently; use common keys where possible
            for k, v in f.tags.items():
                tags[k] = str(v)
        else:
            # generic fallback: list what's present
            for k, v in mf.tags.items() if mf.tags else []:
                tags[str(k)] = str(v)
    except Exception:
        # defensive: some files have malformed tags
        pass
    return tags

def write_tags(path: Path, artist: Optional[str], title: Optional[str]):
    suffix = path.suffix.lower()
    if suffix == '.mp3':
        tags = EasyID3()
        if artist:
            tags['artist'] = artist
        if title:
            tags['title'] = title
        tags.save(path)
    elif suffix == '.flac':
        f = FLAC(path)
        if f.tags is None:
            f.add_tags()
        if artist:
            f['artist'] = artist
        if title:
            f['title'] = title
        f.save()
    elif suffix in ('.m4a', '.mp4', '.m4b'):
        f = MP4(path)
        if artist:
            f.tags['\xa9ART'] = [artist]
        if title:
            f.tags['\xa9nam'] = [title]
        f.save()
    else:
        # best-effort: write minimal tags via MutagenFile if possible
        mf = MutagenFile(path, easy=True)
        if mf is not None:
            if artist:
                mf['artist'] = artist
            if title:
                mf['title'] = title
            mf.save()

def interactive_confirm(path: Path, current: Dict[str, str], suggested_artist: Optional[str],
                        suggested_title: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    print("\nfile:", path)
    print("current artist:", current.get('artist') or current.get('ARTIST') or '<none>')
    print("current title:", current.get('title') or current.get('TITLE') or '<none>')
    print("suggested artist:", suggested_artist)
    print("suggested title :", suggested_title)
    while True:
        resp = input("accept (y), accept both (a), edit (e), skip (s), accept and apply to folder (f): ").strip().lower()
        if resp in ('y', 'a'):
            if resp == 'y':
                return suggested_artist, suggested_title
            else:
                # same as y but explicit
                return suggested_artist, suggested_title
        if resp == 's':
            return None, None
        if resp == 'e':
            new_artist = input(f"artist [{suggested_artist or ''}]: ").strip() or suggested_artist
            new_title = input(f"title  [{suggested_title or ''}]: ").strip() or suggested_title
            return new_artist, new_title
        if resp == 'f':
            # apply to all tracks in same parent folder - implement higher-level logic in main
            return suggested_artist, suggested_title
        print("please enter one of y/a/e/s/f")

def is_supported_file(path: Path) -> bool:
    return path.suffix.lower() in ('.mp3', '.flac', '.m4a', '.mp4', '.m4b')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('base', type=Path, help="base folder for your music")
    p.add_argument('--dry-run', action='store_true', help="don't write anything, just show")
    p.add_argument('--auto', action='store_true', help="auto accept suggestions without prompting")
    p.add_argument('--backup', type=Path, default=None, help="json backup file for original tags")
    args = p.parse_args()

    base: Path = args.base.expanduser().resolve()
    backup = {}
    folder_artist_cache = {}

    for path in sorted(base.rglob('*')):
        if not path.is_file() or not is_supported_file(path):
            continue

        current_tags = read_tags(path)
        suggested_artist = current_tags.get('artist') or current_tags.get('ARTIST') or parse_artist_from_path(path, base)
        suggested_title = current_tags.get('title') or current_tags.get('TITLE') or parse_title_from_filename(path.name)

        # more heuristics: if filename contains "artist - title" pattern, respect that
        m = re.match(r'^(?P<artist>[^-–—]+)\s*[-–—]\s*(?P<title>.+)$', Path(path).stem)
        if m:
            suggested_artist = m.group('artist').strip()
            suggested_title = m.group('title').strip()

        # folder-level override
        folder_key = str(path.parent)
        if folder_key in folder_artist_cache:
            suggested_artist = folder_artist_cache[folder_key]

        # interactive or auto
        if args.auto:
            chosen_artist, chosen_title = suggested_artist, suggested_title
        else:
            chosen_artist, chosen_title = interactive_confirm(path, current_tags, suggested_artist, suggested_title)
            # if user chose folder apply, store in cache
            if chosen_artist and chosen_title:
                # note: interactive_confirm could be expanded to detect "apply to folder"
                pass

        # backup original tags
        backup[str(path)] = current_tags

        if chosen_artist is None and chosen_title is None:
            print("skipping", path)
            continue

        if args.dry_run:
            print("(dry-run) would set:", chosen_artist, "|", chosen_title)
            continue

        try:
            write_tags(path, chosen_artist, chosen_title)
            print("updated:", path)
        except Exception as exc:
            print("failed to write tags for", path, ":", exc)

    if args.backup:
        args.backup.parent.mkdir(parents=True, exist_ok=True)
        with open(args.backup, 'w', encoding='utf8') as fh:
            json.dump(backup, fh, ensure_ascii=False, indent=2)
        print("backup saved to", args.backup)

if __name__ == '__main__':
    main()

