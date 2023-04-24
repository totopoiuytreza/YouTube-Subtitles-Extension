from pytube import YouTube
import re, os
from pydub import AudioSegment

class Youtube:

    def __init__(self, url):
        self.url = url
        self.number_of_segment = 0
        if self.check_valid_url(self.url):
            self.yt = YouTube(self.url)
            self.get_audio_and_segments(30)
            self.start_time = 0
        else:
            raise Exception("Invalid URL")
        

    def check_valid_url(self, url):
        return re.search(r'((http(s)?:\/\/)?)(www\.)?((youtube\.com\/)|(youtu.be\/))[\S]+', url)

    def get_video_duration(self):
        return self.yt.length
    
    def get_audio_from_video(self):
        video = self.yt.streams.filter(only_audio=True).first()
        number_of_segment = video.download(filename=os.path.join("../data", "audio.wav"))
        return number_of_segment
    
    def separate_video_into_segments(self, segment_length):
    
        segment_length = segment_length * 1000
        audio = AudioSegment.from_file(os.path.join("../data", "audio.wav"))
        segments = audio[::segment_length]
        
        for i, segment in enumerate(segments):
            segment.export(os.path.join("../data", f"segment{i+1}.wav"), format="wav")
        self.number_of_segment = i+1

    def get_audio_and_segments(self, segment_length):
        self.get_audio_from_video()
        self.separate_video_into_segments(segment_length)
    
    def get_number_of_segment(self):
        return self.number_of_segment
        

    def whisper_result_to_text(self, result):
        text = []
        for i,s in enumerate(result['segments']):
            text.append(str(i+1))
            time_start = s['start']
            if self.start_time !=0:
                time_start = self.start_time + s['start']
            hours, minutes, seconds = int(time_start/3600), (time_start/60) % 60, (time_start) % 60
            timestamp_start = "%02d:%02d:%06.3f" % (hours, minutes, seconds)
            timestamp_start = timestamp_start.replace('.',',')     
            time_end = s['end']
            if self.start_time !=0:
                time_end = self.start_time + s['end']
            hours, minutes, seconds = int(time_end/3600), (time_end/60) % 60, (time_end) % 60
            timestamp_end = "%02d:%02d:%06.3f" % (hours, minutes, seconds)
            timestamp_end = timestamp_end.replace('.',',')        
            text.append(timestamp_start + " --> " + timestamp_end)

            text.append(s['text'].strip() + "\n")
        self.start_time = time_end
            
        return "\n".join(text)
    

    

    
    
