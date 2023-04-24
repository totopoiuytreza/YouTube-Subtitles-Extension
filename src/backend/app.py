from flask import Flask, request, jsonify
from flask_cors import CORS
from whisper import load_model
import torch, os
from youtube import Youtube

app = Flask(__name__)
CORS(app)
devices = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = load_model("small", device=devices)
options = {"fp16": False, "task": "translate"}

@app.route('/transcribe', methods=['POST'])
def transcribe():
    options = {"fp16": False, "task": "translate"}
    youtube_url = 'https://www.youtube.com/watch?v=' + request.json['video_id']
    yt = Youtube(youtube_url)
    text = []
    
    number_of_segment = yt.get_number_of_segments()
    for i in range(number_of_segment):
        result = model.transcribe(os.path.join('./data',f"segment{i+1}.wav"), **options)
        segment_text = yt.whisper_result_to_text(result)
        text.append(segment_text)
        print(segment_text)
    
    return jsonify({'text': text})