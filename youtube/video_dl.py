from __future__ import unicode_literals
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def download_audio(video_id):
    SAVE_PATH = "data"
    video = "https://www.youtube.com/watch?v=" + video_id

    ydl_opts = {
        'format': 'bestaudio/best',
        'nocheckcertificate': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'outtmpl': SAVE_PATH + '/vid_%(id)s.%(ext)s'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video, download=False)
        id_ = info_dict.get("id", None)
        title = info_dict.get("title", None)
        ydl.download([video])
    
    return f"vid_{id_}.wav"
