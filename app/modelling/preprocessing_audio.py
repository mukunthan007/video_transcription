import numpy as np
import ffmpeg
from ffmpeg import Error
import uuid
from flask import current_app
import pathlib
import os
from glob import glob
import re


class ffmpegProcessor:
    def extract_audio(self, filepath: str, sr: int = 16000):
        try:
            # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
            # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
            audio_file_name = str(uuid.uuid4())

            output_file_name = os.path.join(
                os.getcwd(),
                "app",
                "video_uploads",
                audio_file_name + ".wav",
            )

            output_audio_path = os.path.join(
                os.getcwd(),
                "app",
                "video_uploads",
                "chunk_files",
                audio_file_name + "_*.wav",
            )

            chunk_file_names = os.path.join(
                os.getcwd(),
                "app",
                "video_uploads",
                "chunk_files",
                audio_file_name + "_%03d" + ".wav",
            )
            input_file_name = os.path.join(
                os.getcwd(),
                "app",
                "video_uploads",
                filepath,
            )
            _, _ = (
                ffmpeg.input(input_file_name, threads=0)
                .output(output_file_name, format="wav", acodec="pcm_s16le", ac=1, ar=sr)
                .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True, input=None)
            )

            _, _ = (
                ffmpeg.input(output_file_name, threads=0)
                .output(
                    chunk_file_names,
                    f="segment",
                    codec="pcm_s16le",
                    segment_time=10,
                )
                .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True, input=None)
            )
            print("))", audio_file_name)
            segmented_files = glob(output_audio_path)
            sorted_list = sorted(
                segmented_files, key=lambda x: int(x.split("_")[-1].split(".")[0])
            )

        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e
        pathlib.Path(input_file_name).unlink()
        pathlib.Path(output_file_name).unlink()
        return sorted_list


class PreprocessinAudio:
    def seperate_video_to_audio(self, filepath):
        audio_buffer = ffmpegProcessor().extract_audio(filepath)
        print(audio_buffer)
        return audio_buffer
