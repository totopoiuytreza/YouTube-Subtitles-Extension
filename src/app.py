from flask import Flask, request, jsonify
from whisper import load_model
import torch, os
from youtube import Youtube

app = Flask(__name__)
devices = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = load_model("small", device=devices)

options = {"fp16": False, "task": "translate"}

@app.route('/transcribe', methods=['POST'])
def transcribe():
    url = request.json['url']
    yt = Youtube(url)
    result = model.transcribe(os.path.join('data','audio.wav'), **options)
    text = yt.whisper_result_to_text(result)
    return jsonify(text=text)