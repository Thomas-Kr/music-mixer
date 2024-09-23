from pedalboard import LowpassFilter, Pedalboard, Reverb, Delay, time_stretch
from pedalboard.io import AudioFile
from render_moviepy import render_video
from os.path import exists
from pytube import YouTube
from upload_video import upload_video_to_yt, argparse_all
from upload_thumbnail import upload_YT_thumbnail
from os import remove, listdir
from moviepy.editor import *

import logging

# Set up the logging configuration
logging.basicConfig(filename='errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def MP4ToMP3(mp4, mp3):
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()

def render_audio(file: str, outputFile: str, board: Pedalboard, timeStrecth: float = 1):
    with AudioFile(file) as f:
        with AudioFile(outputFile, 'w', f.samplerate, f.num_channels) as o:
            while f.tell() < f.frames:
                chunk = f.read(f.samplerate)
                effected = board(time_stretch(chunk, f.samplerate, timeStrecth), f.samplerate*timeStrecth, reset=False)
                o.write(effected)
                    
def clear_videos(path):
    for file in listdir(path):
        try:
            remove(path+file)
        except Exception as err: 
            print(f"Error occurred while removing {file}: {err}")
            logging.error(f"Error occurred while removing {file}: {err}")
            
if __name__ == "__main__":
    
    render_spedup = True
    render_slowed = True
    render_muffled = True

    clear = True
    connectYT = True

    muffled_board = Pedalboard([Reverb(room_size=0.25, wet_level=0.3, dry_level=0.3),
                                LowpassFilter(cutoff_frequency_hz=100), Delay(0.05)])
    spedup_board = Pedalboard([Reverb(room_size=0.25)])
    slowed_board = Pedalboard([Reverb(room_size=0.25)])

    video_url = input("Enter the link! ")
    song_name = input("Enter the song name! ")

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
        audio_stream = streams.get_audio_only()
        song_path = audio_stream.download()
        
        MP4ToMP3(song_path, 'song.mp3')
        print("Audio has been downloaded")
    except Exception as err:
        print(err)

    if render_muffled:
        output_audio = 'output_songs/muffled.mp3'
        if not exists(output_audio):
            try:
                render_audio('song.mp3', output_audio, muffled_board)
            except Exception as err:
                print(f"Error occurred while rendering muffled.mp3: {err}")
                logging.error(f"Error occurred while rendering muffled.mp3: {err}")
        
        output_video = "output_videos/muffled.mp4"
        if not exists(output_video):
            try:
                intro = "input_videos/muffled_videos/intro.mp4" 
                main_clip = "input_videos/muffled_videos/main_part.mp4" 
                render_video(intro, main_clip, output_audio, output_video)
            except Exception as err:
                print(f"Error occurred while rendering muffled.mp4: {err}")
                logging.error(f"Error occurred while rendering muffled.mp4: {err}")
                
    if render_spedup:
        output_audio = 'output_songs/spedup.mp3'
        if not exists(output_audio):
            try:
                render_audio('song.mp3', output_audio, spedup_board, 1.2)
            except Exception as err:
                print(f"Error occurred while rendering spedup.mp3: {err}")
                logging.error(f"Error occurred while rendering spedup.mp3: {err}")
        
        output_video = "output_videos/spedup.mp4"
        if not exists(output_video):
            try:
                main_clip = "input_videos/spedup_videos/main_part.mp4" 
                render_video(main_clip, main_clip, output_audio, output_video)
            except Exception as err:
                print(f"Error occurred while rendering spedup.mp4: {err}")
                logging.error(f"Error occurred while rendering spedup.mp4: {err}")
        
    if render_slowed:
        output_audio = 'output_songs/slowed.mp3'
        if not exists(output_audio):
            try:
                render_audio('song.mp3', output_audio, slowed_board, 0.8)
            except Exception as err:
                print(f"Error occurred while rendering slowed.mp3: {err}")
                logging.error(f"Error occurred while rendering slowed.mp3: {err}") 
            
        output_video = "output_videos/slowed.mp4"
        if not exists(output_video):
            try:
                main_clip = "input_videos/slowed_videos/main_part.mp4" 
                render_video(main_clip, main_clip, output_audio, output_video)
            except Exception as err:
                print(f"Error occurred while rendering slowed.mp4: {err}")
                logging.error(f"Error occurred while rendering slowed.mp4: {err}") 

    if render_slowed:
        video_slowed = "output_videos/slowed.mp4"
        title_slowed = f"{song_name} (slowed+reverbed)"
        keywords_slowed = "slowed, remix, sleeping, songs, lovers, cant sleep, edit, winter, broken, driving, relaxing, drinking, aesthetic, heartbroken, sad, cold, calm, free, music, bests, reverb, recent, midnight, christmas, copyright, main character, rap, cry"
        description_slowed = f"""Original Source - {video_url} 

Subscribe to my channel in order to listen more song like this! 
BTW, type me in the comments if you want me to remix some other song!

----Warning!---- 
I want to make it clear that all rights to the original songs belong to their true authors and copyright holders.My works are a creative reinterpretation and do not intend to infringe upon any copyrights. If you enjoyed this content, I recommend supporting the original artists by purchasing their music through legal channels. Thank you for watching! 

----Tags----
{keywords_slowed}"""

        try:
            videoID = upload_video_to_yt(video_slowed, title=title_slowed, description=description_slowed, tags=keywords_slowed, youtube=youtube)
            upload_YT_thumbnail(youtube, videoID, "thumbnails/slowed.jpg")
        except Exception as err:
            print(err)
            logging.error(f"Error occurred while uploading slowed song to Youtube: {err}") 

    if render_spedup:
        video_spedup = "output_videos/spedup.mp4"
        title_spedup = f"{song_name} (spedup+reverbed)"
        keywords_spedup = "speed up songs,sped up songs,sad sped up songs,sped up tiktok songs,tiktok sped up songs,speed up,slowed songs,slowed reverb songs,sped up,fast songs,mix songs,tiktok songs sped up,fifty fifty cupid twin version lyrics,fifty fifty cupid sped up lyrics,cupid fifty fifty sped up tiktok,fifty fifty cupid sped up tiktok,cupid twin version sped up lyrics,cupid twin version sped up tiktok,songs,chill songs,tiktok songs,cupid twin version sped up"
        description_spedup = f"""Original Source - {video_url} 

Subscribe to my channel in order to listen more song like this! 
BTW, type me in the comments if you want me to remix some other song!

----Warning!---- 
I want to make it clear that all rights to the original songs belong to their true authors and copyright holders.My works are a creative reinterpretation and do not intend to infringe upon any copyrights. If you enjoyed this content, I recommend supporting the original artists by purchasing their music through legal channels. Thank you for watching! 

----Tags----
{keywords_spedup}"""
        
        try:
            videoID = upload_video_to_yt(video_file=video_spedup, title=title_spedup, description=description_spedup, tags=keywords_spedup, youtube=youtube)
            upload_YT_thumbnail(youtube, videoID, "thumbnails/spedup.jpg")
        except Exception as err:
            print(f"Error occurred while uploading video to Youtube: {err}")
            logging.error(f"Error occurred while uploading sped up song to Youtube: {err}") 

    if render_muffled:
        video_muffled = "output_videos/muffled.mp4"
        title_muffled = f"{song_name} (muffled)"
        keywords_muffled = "trending,paul anka,paul ankah,music,slowed and reverb,slowed,electro pose,put your head on my shoulder,taehyung,relaxing,jungkook,red velvet,chill rain,rain music,chillbeats,old,study music,gaming music,sunset lover,the living tombstone,suga,put your head on my shoulder but it's raining,beats,elvis,relaxing music,2018 new music,you're,cant help falling in love,my ordinary life,presley,raining,but it's raining outside your apartment,pewdiepie"
        description_muffled = f"""Original Source - {video_url} 

Subscribe to my channel in order to listen more song like this! 
BTW, type me in the comments if you want me to remix some other song!

----Warning!---- 
I want to make it clear that all rights to the original songs belong to their true authors and copyright holders.My works are a creative reinterpretation and do not intend to infringe upon any copyrights. If you enjoyed this content, I recommend supporting the original artists by purchasing their music through legal channels. Thank you for watching! 

----Tags----
{keywords_muffled}"""
        
        try:
            videoID = upload_video_to_yt(video_muffled, title=title_muffled, description=description_muffled, tags=keywords_muffled, youtube=youtube)
            upload_YT_thumbnail(youtube, videoID, "thumbnails/muffled.jpg")
        except Exception as err:
            print(err)
            logging.error(f"Error occurred while uploading muffled song to Youtube: {err}")
            
    try:
        remove(f"song.mp3")
    except Exception as err:
        print(err)
        logging.error(f"Error occurred while removing {song_name}.mp3: {err}")

    if clear:
        clear_videos("output_songs/")
        clear_videos("output_videos/")

    print("Done!")