from moviepy.editor import *
audioclip = AudioFileClip("beethovensymphony.mp3")
videoclip = VideoFileClip("video.mp4")
audioclip2 = audioclip.set_end(videoclip.end)
videoclip2 = videoclip.set_audio(audioclip2)
videoclip2.write_videofile("outputmovieclipped.mp4")
