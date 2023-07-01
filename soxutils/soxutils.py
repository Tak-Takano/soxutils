from functools import cache
from pathlib import Path
import sox
from multiprocessing import Pool
from tqdm import tqdm
import argparse


class Converter:
    def __init__(self, dist_dir, sample_rate, bit_depth):
        self.dist_dir = Path(dist_dir)
        self.tfm = sox.Transformer()
        self.tfm.convert(samplerate=sample_rate, bitdepth=bit_depth)

    def __call__(self, wav_path):
        wav_path = Path(wav_path)
        wav_name = wav_path.name

        if not self.dist_dir.exists():
            self.dist_dir.mkdir(parents=True, exist_ok=True)

        out_path = self.dist_dir / wav_name
        if out_path.exists():
            out_path.unlink()
        
        self.tfm.build(str(wav_path), str(out_path))


def convert(input_dir, output_dir, sample_rate=16000, bit_depth=16, *args, **kwargs):
    input_files = []
    input_dir = Path(input_dir)
    input_files.extend(input_dir.glob("*.wav"))

    converter = Converter(output_dir, sample_rate, bit_depth)

    # プロセス数を指定する
    with Pool(processes=16) as p:
        with tqdm(total=len(input_files)) as t:
            for _ in p.imap_unordered(converter, input_files):
                t.update(1)


def soxdir():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", "-i", required=True)
    parser.add_argument("--output_dir", "-o", required=True)
    parser.add_argument("--sample_rate", "-r", default=16000, type=int)
    parser.add_argument("--bit_depth", "-b", default=16, type=int)

    args = parser.parse_args()

    convert(**vars(args))


if __name__ == "__main__":
    soxdir()
