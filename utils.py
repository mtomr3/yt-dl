from typing import Dict, Any
import yt_dlp as yt_pkg



class YoutubeDownloader:

	def get_video(self, url):
		return self.get(url=url, opts=self.video_opts)

	def get_audio(self, url):
		return self.get(url=url, opts=self.audio_opts)

	def get(self, url: str, opts: Dict[str, Any]):
		with yt_pkg.YoutubeDL(opts) as ydl:
			ydl.download([url])

	@property
	def video_opts(self):
		return {
			**self.default_opts,
			"outtmpl": "./YT/video/%(title)s.%(ext)s",
			"format": "best[ext=mp4]",
		}

	@property
	def audio_opts(self):
		return {
			**self.default_opts,
			"outtmpl": "./YT/audio/%(title)s.%(ext)s",
		    'postprocessors': [{
		        'key': 'FFmpegExtractAudio',
		        'preferredcodec': 'mp3',
		        'preferredquality': '192',
		    }],
		}

	@property
	def default_opts(self):
		class MyLogger(object):
		    def debug(self, msg):
		        print("    debug:", msg)

		    def warning(self, msg):
		        print("  warn   :", msg)

		    def error(self, msg):
		        print("err      :", msg)

		def my_hook(d):
		    if d['status'] == 'finished':
		        print('Done downloading, now converting ...')

		return {
			# "outtmpl": "%(uploader)s%(title)s.%(ext)s",
			# "outtmpl": "%(title)s.%(ext)s",
			# "outtmpl": "./YT/%(title)s.%(ext)s",
			"logger": MyLogger(),
			"progress_hooks": [my_hook],
			"ffmpeg_location": "/usr/local/bin/ffmpeg",
		}



