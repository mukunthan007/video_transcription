import whisper
import os
import uuid
from datetime import timedelta
import pathlib
import torch
from memory_profiler import profile
from timeit import default_timer as timer


class WhisperPrediction:
    @profile
    def __init__(self) -> None:
        self.output_result = ""
        model_fp32 = whisper.load_model(name="base", device="cpu", in_memory=False)

        self.model = torch.quantization.quantize_dynamic(
            model_fp32, {torch.nn.Linear}, dtype=torch.qint8
        )

    def convert_sec_to_vtt(self, sec):
        td = timedelta(seconds=float(sec))
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = td.microseconds // 1000  # Convert microseconds to milliseconds
        formatted_time = "{:02}:{:02}:{:02}.{:03}".format(
            hours, minutes, seconds, milliseconds
        )
        return formatted_time

    def create_time_stamp(self, results, intial_chunk_value):
        current_chunk_string = ""
        segment_list = results["segments"]
        for count in range(len(results["segments"])):
            print("Type", type(segment_list[count]["start"]))
            current_chunk_string += (
                "\n"
                + str(count + 1)
                + "\n"
                + self.convert_sec_to_vtt(
                    segment_list[count]["start"] + intial_chunk_value
                )
                + " --> "
                + self.convert_sec_to_vtt(
                    segment_list[count]["end"] + intial_chunk_value
                )
                + "\n"
                + "- "
                + segment_list[count]["text"]
                + "\n"
            )
        return current_chunk_string

    def create_vtt_segments(self, results):
        file_path = file_path = os.path.join(
            os.getcwd(), "app", "video_uploads", str(uuid.uuid4()) + ".vtt"
        )

        file_object = open(file_path, "w+")
        file_object.write(results)

        file_object.close()
        return file_path

    @profile
    def transcribe_audio(self, files):
        final_speech_to_text = "WEBVTT\n"
        intial_chunk_value = 0
        start = timer()
        for file in files:
            result = self.model.transcribe(file, word_timestamps=True, fp16=False)
            print(result)
            final_speech_to_text += self.create_time_stamp(result, intial_chunk_value)
            pathlib.Path(file).unlink()
            self.output_result += result["text"]
            intial_chunk_value += 10
        end = timer()
        print("_______________________", end - start)
        del self.model.encoder
        del self.model.decoder
        torch.cuda.empty_cache()
        return self.create_vtt_segments(final_speech_to_text)
