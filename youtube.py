from pytube import YouTube
import re, os

class Youtube:

    def __init__(self, url):
        self.url = url
        if self.check_valid_url(self.url):
            self.yt = YouTube(self.url)
            self.get_audio_from_video()
        else:
            raise Exception("Invalid URL")
        

    def check_valid_url(self, url):
        return re.search(r'((http(s)?:\/\/)?)(www\.)?((youtube\.com\/)|(youtu.be\/))[\S]+', url)

    def get_video_duration(self):
        return self.yt.length

    def get_audio_from_video(self):
        return self.yt.streams.filter(only_audio=True).first().download(filename=os.path.join("data", "audio.mp3"))
    
    def whisper_result_to_text(self, result):
        text = []
        for i,s in enumerate(result['segments']):
            text.append(str(i+1))

            time_start = s['start']
            hours, minutes, seconds = int(time_start/3600), (time_start/60) % 60, (time_start) % 60
            timestamp_start = "%02d:%02d:%06.3f" % (hours, minutes, seconds)
            timestamp_start = timestamp_start.replace('.',',')     
            time_end = s['end']
            hours, minutes, seconds = int(time_end/3600), (time_end/60) % 60, (time_end) % 60
            timestamp_end = "%02d:%02d:%06.3f" % (hours, minutes, seconds)
            timestamp_end = timestamp_end.replace('.',',')        
            text.append(timestamp_start + " --> " + timestamp_end)

            text.append(s['text'].strip() + "\n")
            
        return "\n".join(text)
    

    

    
    
