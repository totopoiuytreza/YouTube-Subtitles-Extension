import whisper
import torch
import os
from youtube import Youtube

devices = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") 
model = whisper.load_model("small", device=devices)
yt = Youtube("https://www.youtube.com/watch?v=CqeACWm74xI")
options = {"fp16": False, "task": "translate"}
result = model.transcribe(os.path.join('data','audio.wav'), **options)
print(yt.whisper_result_to_text(result))