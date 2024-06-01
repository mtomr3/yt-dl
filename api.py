"""
Examples:
	In [1]: from api import get_video, get_audio
	   ...: url = "https://www.youtube.com/watch?v=EMMCBKfDH28"
	   ...: get_video(url)
	   ...: get_audio(url)
"""

from utils import YoutubeDownloader, YoutubeMetadataProvider

def get_video(url):
	return YoutubeDownloader().get_video(url)

def get_audio(url, inmem=False):
	return YoutubeDownloader().get_audio(url, inmem=inmem)

def get_vid_data(url):
	return YoutubeMetadataProvider.get_data(url)

def get_title(url):
	return YoutubeMetadataProvider.get_title(url)

def get_thumbnail_url(url):
	return YoutubeMetadataProvider.get_thumbnail_url(url)
