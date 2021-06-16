import youtube_dl
import os

s="https://www.youtube.com/watch?v=gi1aPNWJCqI"
d="D:\Videos"

def download_vid(filepath, link):
    link_video=[link]
    ydl_opts = {'format': 'best[height<=720]',
                'outtmpl': os.path.join(filepath, '%(title)s'),
                'sleep_interval': 30,
                'max_sleep_interval': 40
                }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(link_video)

download_vid(d,s)