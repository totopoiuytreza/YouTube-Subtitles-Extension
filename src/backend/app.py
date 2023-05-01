from flask import Flask, request, jsonify
from flask_cors import CORS
from whisper import load_model
import torch, os
from youtube import Youtube

app = Flask(__name__)
CORS(app)
devices = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = load_model("small", device=devices)
current_youtube = None
transcription = []

@app.route('/transcribe', methods=['POST'])
def transcribe():
    global transcription
    options = {"fp16": False, "task": "translate", "language": request.json['language']}
    youtube_url = 'https://www.youtube.com/watch?v=' + request.json['video_id']
    print(youtube_url)
    print("downloading...")
    yt = Youtube(youtube_url)
    print("downloaded")
    
    transcription = []
    number_of_segment = yt.get_number_of_segment()
    for i in range(number_of_segment):
        result = model.transcribe(os.path.join('src/data',f"segment{i+1}.wav"), **options)
        segment_text = yt.whisper_result_to_text(result)
        transcription.append(segment_text)
        print(segment_text)
    return jsonify({'text': transcription})
    


@app.route('/check_transcription', methods=['GET'])
def checktranscribe():
    global transcription
    return jsonify({'text': transcription})


if __name__ == '__main__':
    app.run(debug=True)


