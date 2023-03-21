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

# Start a separate thread for transcribing
transcribe_thread = threading.Thread(target=transcribe, args=(model, options, os.path.join('data','audio.wav')))
transcribe_thread.start()

# Wait for the transcription thread to finish and get the result
transcribe_thread.join()
result = transcribe_thread

# Start a separate thread for printing
print_thread = threading.Thread(target=print_text, args=(yt, result))
print_thread.start()

# Wait for the printing thread to finish before exiting
print_thread.join()
