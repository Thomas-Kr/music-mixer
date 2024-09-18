from moviepy.editor import VideoFileClip, AudioFileClip, vfx, concatenate_videoclips

def render_video(final_video: str, main_clip: str, audio_clip: str, output_name: str):
    final_video = VideoFileClip(final_video)
    main_clip = VideoFileClip(main_clip)
    audio_clip = AudioFileClip(audio_clip)
    
    num_repeats = int((audio_clip.duration - final_video.duration)/ main_clip.duration)+1

    # Повторение main_clip
    main_clips = concatenate_videoclips([main_clip] * num_repeats)
    main_clips = main_clips.subclip(0, audio_clip.duration-final_video.duration)

    final_video = concatenate_videoclips([final_video, main_clips])

    final_video = final_video.set_audio(audio_clip)

    # Применение эффекта Fade In и Fade Out
    final_video = final_video.fx(vfx.fadein, duration=1).fx(vfx.fadeout, duration=1)

    final_video.write_videofile(output_name, fps=24, bitrate='4000k')

