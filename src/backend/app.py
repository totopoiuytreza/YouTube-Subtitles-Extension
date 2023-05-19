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

@app.route('/test', methods=['POST'])
def test():
    return jsonify({'text': 'test'})

@app.route('/transcribeAll', methods=['POST'])
def transcribeAll():
    global transcription
    options = {"fp16": False, "task": "translate", "language": request.json['language']}
    youtube_url = 'https://www.youtube.com/watch?v=' + request.json['video_id']
    print("downloading...")
    #yt = Youtube(youtube_url)
    print("downloaded")
    transcription = []
    result = model.transcribe(os.path.join('src/data',f"audio.wav"), **options)
    #transcription.append(yt.whisper_result_to_text(result))
    #print(transcription)
    
    #generate_vtt_file(transcription)  # Generate the VTT file
    print(result['text'])
    
    return jsonify({'text': result['text']})
    
    

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

    generate_vtt_file(transcription)  # Generate the VTT file

    return jsonify({'text': transcription})

    
def generate_vtt_file(transcription):
    vtt_content = "WEBVTT\n\n"
    start_time = 0

    for index, text in enumerate(transcription):
        end_time = start_time + 5  # Assuming each segment is 5 seconds long
        vtt_content += f"{index + 1}\n"
        vtt_content += f"{format_time(start_time)} --> {format_time(end_time)}\n"
        vtt_content += f"{text}\n\n"
        start_time = end_time

    with open("subtitles.vtt", "w", encoding="utf-8") as vtt_file:
        vtt_file.write(vtt_content)


def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{int(minutes):02d}:{int(seconds):02d}.{milliseconds:03d}"



@app.route('/check_transcription', methods=['GET'])
def checktranscribe():
    global transcription
    return jsonify({'text': transcription})


if __name__ == '__main__':
    app.run(debug=True)


