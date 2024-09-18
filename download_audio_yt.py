from pytube import YouTube

def download_audio_yt(video_url, file_name: str = 'audio.mp3'):
    yt = YouTube(video_url) 
    streams = yt.streams
    best_stream = streams.get_audio_only()
    best_stream.download(filename=file_name)

    print("Audio has been downloaded")