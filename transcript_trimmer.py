# /// script
# requires-python="==3.9"
# dependencies = [
#   "numpy==1.26.4",
#   "openai-whisper==20250625",
#   "pydub==0.25.1",
#   "setuptools-rust==1.12.0",
# ]
# ///

from pydub import AudioSegment
import whisper

import os
import ssl
import sys
ssl._create_default_https_context = ssl._create_unverified_context

podcast_path  = sys.argv[1]
new_podcast_name = podcast_path.split('/')[-1].split('.')[0] + '_clean.mp3'

root_list = podcast_path.split('/')
del root_list[-1]
root_path = ('/').join(root_list)
new_podcast_path = os.path.join(root_path, new_podcast_name)

model = whisper.load_model("base")
result = model.transcribe(podcast_path, fp16=False)

all_segments = []

for segment in result['segments']:
    print(f"{segment['id']}: {segment['text']}")
    all_segments.append({'id': segment['id'], 'start': segment['start'], 'end': segment['end']})

segment_ids_to_remove = []
response = input("Enter segment ids to remove (e.g. 35-118, 200, 235, 281-299): ")
if response == 'exit':
    sys.exit()
for r in response.split(', '):
    rspl = r.split('-')
    if len(rspl) > 1:
        segment_ids_to_remove.extend(list(range(int(rspl[0]), int(rspl[1])+1)))
    else:
        segment_ids_to_remove.append(int(rspl[0]))
print(f"Removing segments {segment_ids_to_remove}")

x_segments = []
for s in segment_ids_to_remove:
    x_segments.append([(d['start'] * 1000, d['end'] * 1000) for d in all_segments if d.get('id') == s][0])

# Remove segments (reverse order so times don't shift)
audio = AudioSegment.from_mp3(podcast_path)
for start_ms, end_ms in reversed(x_segments):
    audio = audio[:start_ms] + audio[end_ms:]
audio.export(new_podcast_path, format="mp3")

new_result = model.transcribe(new_podcast_path, fp16=False)
for segment in new_result['segments']:
    print(segment['text'])

# uv run transcript_trimmer.py TheMoth.mp3

