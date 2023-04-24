import whisper
import torch
import os
from youtube import Youtube
import threading

def transcribe(model, options, file_path):
    result = model.transcribe(file_path, **options)
    return result

def print_text(yt, result):
    text = yt.whisper_result_to_text(result)
    print(text)

devices = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = whisper.load_model("small", device=devices)
yt = Youtube("https://www.youtube.com/watch?v=CqeACWm74xI")
options = {"fp16": False, "task": "translate"}

