from pytube import YouTube
import re, os
from pydub import AudioSegment

"""@app.route('/get_video_id', methods=['POST'])
def get_video_id():
    # Récupérer l'URL de la vidéo depuis la requête POST
    video_url = request.json['video_url']
    
    # Extraire l'ID de la vidéo
    youtube = Youtube(video_url)
    video_id = youtube.get_video_id()
    
    # Retourner l'ID de la vidéo en tant que réponse JSON
    return jsonify({'video_id': video_id})"""

class Youtube:

    def __init__(self, url):
        self.url = url
        self.video_id = url.split("=")[1]
        self.number_of_segment = 0
        if self.check_valid_url(self.url):
            self.yt = YouTube(self.url)
            self.get_audio_and_segments(30)
            self.start_time = 0
        else:
            raise Exception("Invalid URL")
        

    def check_valid_url(self, url):
        return re.search(r'((http(s)?:\/\/)?)(www\.)?((youtube\.com\/)|(youtu.be\/))[\S]+', url)

    def get_video_id(self):
        return self.video_id
        
    def get_video_duration(self):
        return self.yt.length
    
    def get_audio_from_video(self):
        video = self.yt.streams.filter(only_audio=True).first()
        video = video.download(filename=os.path.join("src/data", "audio.wav"))
        return video
    
    def separate_video_into_segments(self, segment_length):
    
        segment_length = segment_length * 1000
        audio = AudioSegment.from_file(os.path.join("src/data", "audio.wav"))
        segments = audio[::segment_length]
        
        for i, segment in enumerate(segments):
            segment.export(os.path.join("src/data", f"segment{i+1}.wav"), format="wav")
        self.number_of_segment = i+1

    def get_audio_and_segments(self, segment_length):
        self.get_audio_from_video()
        self.separate_video_into_segments(segment_length)
    
    def get_number_of_segment(self):
        return self.number_of_segment
        

    def whisper_result_to_text(self, result):
        text = []
        
        for i,s in enumerate(result['segments']):
            time_start = s['start']
            time_end = s['end']
            text.append(str(i+1))
            if self.start_time !=0:
                time_start = self.start_time + s['start']
            hours, minutes, seconds = int(time_start/3600), (time_start/60) % 60, (time_start) % 60
            timestamp_start = "%02d:%02d:%06.3f" % (hours, minutes, seconds)
            timestamp_start = timestamp_start.replace('.',',')     
            if self.start_time !=0:
                time_end = self.start_time + s['end']
            hours, minutes, seconds = int(time_end/3600), (time_end/60) % 60, (time_end) % 60
            timestamp_end = "%02d:%02d:%06.3f" % (hours, minutes, seconds)
            timestamp_end = timestamp_end.replace('.',',')        
            text.append(timestamp_start + " --> " + timestamp_end)

            text.append(s['text'].strip() + "\n")
        self.start_time = time_end
            
        return "\n".join(text)
    

    

    
    
