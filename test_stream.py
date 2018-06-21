import os

YOUTUBE = "rtmp://a.rtmp.youtube.com/live2/"
FACEBOOK = "rtmp://live-api.facebook.com:80/rtmp/"
#YT_KEY = os.environ['YOUTUBE_KEY']
FB_KEY = os.environ['FACEBOOK_KEY']
stream_cmd = "raspivid -o - -t 0 -fps 30 -h 720 -w 1280 -b 4000000 -rot 270 -vs | /root/ffmpeg/ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 120 -strict experimental -f flv '" + FACEBOOK + FB_KEY + "'"
#stream_pipe = subprocess.Popen(stream_cmd, shell=True, stdin=subprocess.PIPE)
print(stream_cmd)
