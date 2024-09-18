import logging

import numpy as np

from os.path import exists
from pytube import YouTube
from upload_video import upload_video_to_yt, argparse_all
from os import remove, listdir
from moviepy.editor import *

# Set up the logging configuration
logging.basicConfig(filename='errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def MP4ToMP3(mp4, mp3):
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()
                    
def clear_media(path):
    for file in listdir(path):
        if file.endswith(".mp4") or file.endswith(".mp3"):
            try:
                remove(f"{path}\\{file}")
            except Exception as err: 
                print(f"Error occurred while removing {file}: {err}")
                logging.error(f"Error occurred while removing {file}: {err}")

def loop_song(audio_path, image_path, output_path="1_hour_song.mp4", target_duration_sec=3600):
    audio = AudioFileClip(audio_path)

    n_repeats = int(np.ceil(target_duration_sec / audio.duration))

    clips = []
    for _ in range(n_repeats):
        audio_instance = AudioFileClip(audio_path)
        clips.append(ImageClip(image_path).set_duration(audio_instance.duration).set_audio(audio_instance))

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, fps=24, bitrate='4000k')

if __name__ == "__main__":
    video_url = input("Enter the link! ")
    song_name = input("Enter the song name! ")

    clear = False
    connectYT = True

    output_video = "1_hour_song.mp4"

    if connectYT:
            try:
                youtube = argparse_all()
            except Exception as err:
                print(f"Error occurred while argparsing all: {err}")
                logging.error(f"Error occurred while argparsing all: {err}") 

    #Create Youtube Object
    yt = YouTube(video_url)

    #Download the audio
    try:
        streams = yt.streams
        best_stream = streams.get_audio_only()
        song_path = best_stream.download()
        MP4ToMP3(song_path, song_name+'.mp3')
        print("Audio has been downloaded")
    except Exception as err:
        print(err)

    if not exists(output_video):
        try:
            loop_song(f'{song_name}.mp3', 'background.png')
        except Exception as err:
            print(f"Error occurred while creating video: {err}")
            logging.error(f"Error occurred while creating video: {err}")

    if connectYT:
        video = output_video
        title = f"{song_name} ~ 1 hour"
        keywords = "slowed, remix, sleeping, songs, lovers, cant sleep, edit, winter, broken, driving, relaxing, drinking, aesthetic, heartbroken, sad, cold, calm, free, music, bests, reverb, recent, midnight, christmas, copyright, main character, rap, cry"
        description = f"""Original Source - {video_url} 

Subscribe to my channel in order to listen more song like this! 
BTW, type me in the comments if you want me to remix some other song!

----Warning!---- 
I want to make it clear that all rights to the original songs belong to their true authors and copyright holders.My works are a creative reinterpretation and do not intend to infringe upon any copyrights. If you enjoyed this content, I recommend supporting the original artists by purchasing their music through legal channels. Thank you for watching! 

----Tags----
{keywords}"""

        try:
            videoID = upload_video_to_yt(video, title=title, description=description, tags=keywords, youtube=youtube)
        except Exception as err:
            print(err)
            logging.error(f"Error occurred while uploading the song to Youtube: {err}") 