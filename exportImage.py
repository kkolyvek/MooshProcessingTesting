"""
Moosh Systems 2021

Send processed video feed to streaming site of choice.
"""

import subprocess

def createPipe(site, width, height, vid_fps):
    """
    Creates pipe path to streaming site:
    "YOUTUBE" = YouTube.com
    "TWITCH" = Twitch.tv
    """
    # stream keys
    YOUTUBE = "rtmp://a.rtmp.youtube.com/live2/9tkm-ugb5-0s69-830y-7pfp"
    TWITCH = "rtmp://live.twitch.tv/app/live_59331422_RYR8lVnLME9o5QYriuSsQtchdleitF"
    # command and params for ffmpeg
    ffmpegCommand = ['ffmpeg',
                    '-y',
                    '-f', 'rawvideo',
                    '-vcodec', 'rawvideo',
                    '-pix_fmt', 'bgr24',
                    '-s', "{}x{}".format(width, height),
                    '-r', str(vid_fps),
                    '-i', '-',
                    '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p',
                    '-preset', 'ultrafast',
                    '-f', 'flv']

    if site == "YOUTUBE":
        ffmpegCommand = ' '.join(ffmpegCommand) + ' ' + YOUTUBE
        return subprocess.Popen(ffmpegCommand, stdin=subprocess.PIPE)
    elif site == "TWITCH":
        ffmpegCommand = ' '.join(ffmpegCommand) + ' ' + TWITCH
        return subprocess.Popen(ffmpegCommand, stdin=subprocess.PIPE)
    else:
        print("Error in stream upload - check ffmpeg parameters")

def imageOut(pipe, frame):
    """
    Sends frame image down pipe
    """
    pipe.stdin.write(frame.tobytes())

def destroyPipe(pipe):
    """
    Terminates subprocess
    """
    pipe.terminate()
