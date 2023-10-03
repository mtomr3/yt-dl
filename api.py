"""
Examples:
	In [1]: from api import get_video, get_audio
	   ...: url = "https://www.youtube.com/watch?v=EMMCBKfDH28"
	   ...: get_video(url)
	   ...: get_audio(url)
"""

from utils import YoutubeDownloader

def get_video(url):
	return YoutubeDownloader().get_video(url)

def get_audio(url):
	return YoutubeDownloader().get_audio(url)


