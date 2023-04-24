import os
import argparse
import soundfile as sf
import pyloudnorm as pyln
from tqdm import tqdm

music_path = '/Users/rmakhlin/Documents/QUIZ MUSIC/TEMPLATE'

parser = argparse.ArgumentParser(description="Normalises sound to target LUFS level for audio files in specified folder and its subfolders",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-lufs", type=float, help="target lufs level to match", default=-12.0, required=False)
parser.add_argument("-r", "--recursive", action="store_true", help="recursivly search subfolders for audiofiles to adjust", default=True)
parser.add_argument("audio_folder", help="audio files location")
args = parser.parse_args()
config = vars(args)

lufs = config['lufs']
recu = config['recursive']
audi = config['audio_folder']

def normalize(track_path):
    data, rate = sf.read(track_path)
    peak_normalized_audio = pyln.normalize.peak(data, -1.0)
    meter = pyln.Meter(rate)
    loudness = meter.integrated_loudness(data)
    loudness_normalized_audio = pyln.normalize.loudness(data, loudness, lufs)
    sf.write(track_path, loudness_normalized_audio, rate)

def process(files):
    pbar = tqdm(files)
    for audio in pbar:
        pbar.set_description(audio)
        normalize(audio)

def find_files(folder_path):
    audio_files = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) and item_path.endswith('.mp3'):
            audio_files.append(item_path)
        elif os.path.isdir(item_path) and recu:
            audio_files += find_files(item_path)
    return audio_files

if os.path.isdir(audi):
    print(f"Normalizing audio to {lufs}LUFS level")
    process(find_files(audi))
else:
    print(f"Path {audi} does not exists or is not a folder")
